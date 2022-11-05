from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.schemas import Token, UserBase, UserCreate, UserUpdate, User, TagBase, TagUpdate
from app.database import get_db
from app.utils import (
    authenticate_user, 
    create_access_token, 
    get_user_by_name, 
    create_user,
    update_username,
    get_current_user,
    get_current_active_user,
    create_tag,
    update_tag,
    delete_tag,
    get_tag_by_name
)
from config import ACCESS_TOKEN_EXPIRE_MINUTES


router = APIRouter(
    prefix="/users",
    tags=["users"],
    responses={404: {"description": "Not found"}},
)


@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect usrname or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/register/", response_model=UserBase)
async def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_name(db=db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return create_user(db=db, user=user)


@router.get("/me/", response_model=User)
async def read_users_me(create_user: User = Depends(get_current_active_user)):
    return create_user


@router.put("/me/username-update/{username}", response_model=UserBase)
async def update_user_username(username: str, user: UserUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if username != current_user.username:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return update_username(db=db, username=username, user=user)



@router.post("/create-tag/", response_model=TagBase)
async def create_new_tag(tag: TagBase, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    return create_tag(db=db, tag=tag, user=current_user)


@router.put("/update-tag/{tag_id}", response_model=TagBase)
async def update_tag_title(tag_id: int, tag: TagUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    if not tag_id in current_user.tags:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return update_tag(db=db, tag_id=tag_id, tag=tag)


@router.delete("/delete-tag/{title}")
async def tag_delete(title: str, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    tag = get_tag_by_name(db=db, title=title)
    if not tag.id in current_user.tags:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return delete_tag(db=db, title=title)