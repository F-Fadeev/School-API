import time

import jwt
from jwt import PyJWTError

from config import settings

JWT_SECRET = settings.JWT_SECRET
JWT_ALGORITHM = settings.JWT_ALGORITHM


def sign_jwt() -> dict[str, str]:
    token_expire = 600
    payload = {
        'expires': time.time() + token_expire,
    }
    token = jwt.encode(payload, key=JWT_SECRET, algorithm=JWT_ALGORITHM)
    return {'access_token': token,
            'token_type': 'bearer',
            'expires': token_expire,
            }


def decode_jwt(token: str) -> bool:
    try:
        decoded_token = jwt.decode(token, key=JWT_SECRET, algorithms=[JWT_ALGORITHM])
    except PyJWTError:
        return False
    return decoded_token['expires'] >= time.time()
