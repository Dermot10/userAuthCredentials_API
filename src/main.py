from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from .schemas import SystemUser, UserAuthDetails, UserCreate, UserInDB, Token, UserOut
from .deps import get_db, get_current_user
from .utils import (
    verify_password, get_password_hash,
    create_access_token, create_refresh_token
)
import psycopg2
from typing import List
from . import crud
from sqlalchemy.orm import Session


app = FastAPI()


@app.get('/')
def index():
    return {"message": "Welcome to the home page"}


@app.get('/user/{user_id}/', response_model=List[UserInDB])
async def get_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_id(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status=404, detail="Artist not found in database")
    return db_user


@app.get('/user/{username}/', response_model=List[UserInDB])
async def get_user(username: str, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, username=username)
    if db_user is None:
        raise HTTPException(status=404, detail="User not found in database")
    return db_user


@app.get('/users/', response_model=List[UserInDB])
async def get_users(skip: int = 0, limit=100, db: Session = Depends(get_db)):
    user = crud.get_user(db, skip=skip, limit=limit)
    return user


@app.get('/current/', summary="Return data of logged in user", response_model=UserOut)
async def get_current(user: SystemUser = Depends(get_current_user)):
    return user


@ app.post('/signup/', status_code=201, summary="Create a new user")
async def create_user(user: UserCreate,  db: Session = Depends(get_db)):
    new_user = {
        "username": user.username,
        "email": user.email,
        "fullname": user.fullname,
        "password": get_password_hash(user.password),
    }

    db_user = crud.create_user(db=db, user=user)
    if db_user:
        return {f"Success": {db_user}}
    raise HTTPException(status_code=400, detail="User already exists")


@app.post('/login', summary="Create access and refresh tokens for user", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user(db, form_data.username)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    hashed_pass = user.password
    if not verify_password(form_data.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password"
        )

    return {
        "access_token": create_access_token(user.email),
        "refresh_token": create_refresh_token(user.email),
    }
