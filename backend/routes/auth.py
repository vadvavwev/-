from flask import Blueprint, request
from werkzeug.security import check_password_hash
from models.user import AdminUser
from middleware.auth_middleware import generate_token
from utils.response import success, error
from utils.exceptions import BadRequestException, UnauthorizedException

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True)
    if not data:
        raise BadRequestException("参数校验失败：请求体不能为空")

    username = data.get("username", "")
    password = data.get("password", "")

    if not username or not password:
        raise BadRequestException("参数校验失败：用户名和密码不能为空")

    user = AdminUser.query.filter_by(username=username).first()
    if not user or not check_password_hash(user.password_hash, password):
        raise UnauthorizedException("用户名或密码错误")

    token = generate_token(user.id, user.role)
    return success(
        data={
            "token": token,
            "user": {"id": str(user.id), "username": user.username, "role": user.role},
        },
        message="登录成功",
    )
