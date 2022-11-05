from datetime import timedelta

from fastapi import Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

# from app.main import app
from app.schemas import Token, UserBase, UserCreate, User, TagBase
from app.database import get_db
from app.utils import (
    authenticate_user, 
    create_access_token, 
    get_user_by_name, 
    create_user, 
    get_current_active_user,
    create_tag,
)
from config import ACCESS_TOKEN_EXPIRE_MINUTES
# from app.crud import get_user_by_name, create_user


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


@router.post("/create-tag/", response_model=TagBase)
async def create_new_tag(tag: TagBase, db: Session = Depends(get_db)):
    # if not get_current_active_user():
    #       raise HTTPException(status_code=status.HTTP_403_FORBIDDEN)
    return create_tag(db=db, tag=tag)
