import jwt

from typing import Annotated
from fastapi import Depends, HTTPException
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPAuthorizationCredentials

from config import secret_key, algorithm, access_token_minutes, refresh_token_days
from schema.jwt import TokenResponse
from bearer import bearer_scheme


# TWORZENIE TOKENU JWT
def create_jwt(id: int, nickname: str, type: str, expires: timedelta):
    expires += datetime.now(timezone.utc)
    payload = { "sub": str(id), "nickname": nickname, "type": type, "exp": expires}
    encoded_jwt = jwt.encode(payload, secret_key, algorithm)
    return TokenResponse(access_token=encoded_jwt, token_type="bearer")


# TWORZENIE TOKENU DOSTEPU JWT
def create_acces_jwt(id: int, nickname: str):
    return create_jwt(id, nickname, 'access', timedelta(minutes=int(access_token_minutes)))


# PRZEDLUZENIE TOKENU JWT
def create_refresh_jwt(id: int):
    return create_jwt(id, 'refresh', timedelta(days=refresh_token_days))


# ODSZYFROWANIE TOKENU JWT
def decode_validate_jwt(token: str, expected_type: str):
    try:
        payload = jwt.decode(token, secret_key, algorithm)
        sub: str | None = payload.get("sub")
        nickname: str | None = payload.get("nickname")
        type: str | None = payload.get("type")

        if sub is None or type != expected_type:
            raise HTTPException(status_code=401, detail="Nieprawidłowy lub wygasły token")

        return { "id": int(sub), "nickname": nickname }

    except (InvalidTokenError, ValueError):
        raise HTTPException(status_code=401, detail="Nieprawidłowy lub wygasły token")


def get_id_from_token(credentials: Annotated[HTTPAuthorizationCredentials, Depends(bearer_scheme)]):
    token = credentials.credentials
    result = decode_validate_jwt(token, 'access')

    return int(result.get("id"))