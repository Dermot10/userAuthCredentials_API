from typing import Union, Any
from datetime import datetime
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from .utils import (
    ALGORITHM, authjwt_secret_key)
from jose import jwt
from pydantic import ValidationError
from .schemas import TokenPayload, SystemUser
from .database import SessionLocal, engine
from . import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login", scheme_name="JWT")
models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_current_user(token: str = Depends(oauth2_scheme)) -> SystemUser:
    try:
        payload = jwt.decode(
            token, authjwt_secret_key, algorithm=[ALGORITHM]
        )
        token_data = TokenPayload(**payload)

        if datetime.fromtimestamp(token_data.exp) < datetime.now():
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
    except (jwt.JWSError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    # Avoid Circular import
    from .main import users_db
    user: Union[dict[str, Any], None] = users_db.get(token_data.sub, None)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )

    return SystemUser(**user)
