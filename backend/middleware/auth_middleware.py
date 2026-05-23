from functools import wraps
import jwt
from flask import request
from config import Config


def generate_token(user_id, role="admin"):
    payload = {
        "sub": user_id,
        "role": role,
    }
    token = jwt.encode(payload, Config.JWT_SECRET, algorithm="HS256")
    return token


def verify_token(token):
    try:
        payload = jwt.decode(token, Config.JWT_SECRET, algorithms=["HS256"])
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def login_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        from utils.exceptions import UnauthorizedException

        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            raise UnauthorizedException("未授权访问，请先登录")

        token = auth_header.split(" ", 1)[1]
        payload = verify_token(token)
        if payload is None:
            raise UnauthorizedException("令牌无效或已过期，请重新登录")

        request.current_user = payload
        return f(*args, **kwargs)

    return decorated
