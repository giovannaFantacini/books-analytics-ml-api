import datetime
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from src.auth.authentication import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    ACCESS_TOKEN_EXPIRE_MINUTES,
    REFRESH_TOKEN_EXPIRE_MINUTES,
)

router = APIRouter(prefix="/api/v1/auth", tags=["Auth"])

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    ok = authenticate_user(form_data.username, form_data.password)
    if not ok:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    access_token_expires = datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    refresh_token_expires = datetime.timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)

    access_token = create_access_token(
        data={"sub": form_data.username},
        expires_delta=access_token_expires,
    )
    refresh_token = create_refresh_token(
        data={"sub": form_data.username},
        expires_delta=refresh_token_expires,
    )

    return {"access_token": access_token, "refresh_token": refresh_token, "token_type": "bearer"}
