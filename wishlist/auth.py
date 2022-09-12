import os

from fastapi import Depends, HTTPException, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import decode
from jwt.exceptions import PyJWTError

from wishlist.exc import NotFound
from wishlist.models import User
from wishlist.orm import DEFAULT_SESSION_FACTORY


def verify_jwt(token: str) -> bool:

    try:
        return bool(decode(token, os.environ["JWT_SECRET"], algorithms=["HS256"]))
    except PyJWTError:
        return False


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials:

        credentials = await super().__call__(request)

        if credentials is None:
            raise HTTPException(status_code=403, detail="Invalid credentials")

        if credentials.scheme != "Bearer":
            raise HTTPException(status_code=403, detail="Invalid authentication scheme")

        if not verify_jwt(credentials.credentials):
            raise HTTPException(status_code=403, detail="Invalid token")

        return credentials


def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(JWTBearer())):

    user = decode(
        credentials.credentials, os.environ["JWT_SECRET"], algorithms=["HS256"]
    )

    with DEFAULT_SESSION_FACTORY() as session:
        _user = session.query(User).get(user["user_id"])

        if _user is None:
            raise NotFound(id_=user["user_id"])

        return _user
