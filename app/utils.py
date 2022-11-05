from datetime import timedelta, datetime

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from typing import Union
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas import UserInDB, TokenData, UserCreate, TagBase, TagUpdate, UserUpdate
from app.models import User, Tag

from config_local import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES


pwd_context = CryptContext(schemes=['bcrypt'], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user_by_name(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def create_user(db: Session, user: UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_username(db: Session, username: str, user: UserUpdate):
    db_user = get_user_by_name(db=db, username=username)
    db_user.username = user.username
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db, username: str):
    if username in db:
        user_dict = db[username]
        return UserInDB(**user_dict)


def authenticate_user(db: Session, username: str, password: str):
    user = get_user_by_name(db=db, username=username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_tag(db: Session, tag: TagBase, user: User):
    db_tag = Tag(title=tag.title, user_id=user.id)
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def get_tag_by_name(db:Session, title: str):
    return db.query(Tag).filter(Tag.title == title).first()


def update_tag(db: Session, tag_id: id, tag: TagUpdate):
    db_tag = db.query(Tag).filter(Tag.id == tag_id).first()
    db_tag.title = tag.title
    db.add(db_tag)
    db.commit()
    db.refresh(db_tag)
    return db_tag


def delete_tag(db: Session, title: str):
    db_tag = db.query(Tag).filter(Tag.title == title).first()
    db.delete(db_tag)
    db.commit()
    return {"message": f"Successfully deleted tag {title}"}


def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({'exp': expire})
    encodet_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encodet_jwt


async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate crendentails",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_name(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user