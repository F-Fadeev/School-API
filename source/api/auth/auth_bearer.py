from fastapi import Request, HTTPException, status
from fastapi.security import HTTPBearer
from fastapi.security.utils import get_authorization_scheme_param

from .auth_handler import decode_jwt


class JWTBearer(HTTPBearer):
    def __call__(self, request: Request) -> str | None:
        authorization = request.headers.get('Authorization')
        scheme, credentials = get_authorization_scheme_param(authorization)
        if not (authorization and scheme and credentials):
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN, detail='Not authenticated',
                )
            return None
        if scheme.lower() != 'bearer':
            if self.auto_error:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail='Invalid authentication credentials',
                )
            return None
        if not decode_jwt(credentials):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail='Invalid authorization code')
        return credentials
