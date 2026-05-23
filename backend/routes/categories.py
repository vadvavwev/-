from flask import Blueprint, request
from middleware.auth_middleware import login_required
from utils.response import success
import services.category_service as service

categories_bp = Blueprint("categories", __name__)


@categories_bp.route("/api/categories", methods=["GET"])
@login_required
def get_all():
    result = service.get_all()
    return success(data={"categories": result})


@categories_bp.route("/api/categories/<int:category_id>", methods=["GET"])
@login_required
def get_by_id(category_id):
    result = service.get_by_id(category_id)
    return success(data=result)


@categories_bp.route("/api/categories", methods=["POST"])
@login_required
def create():
    data = request.get_json(silent=True) or {}
    result = service.create(data)
    return success(data=result, message="添加成功")


@categories_bp.route("/api/categories/<int:category_id>", methods=["PUT"])
@login_required
def update(category_id):
    data = request.get_json(silent=True) or {}
    result = service.update(category_id, data)
    return success(data=result, message="修改成功")


@categories_bp.route("/api/categories/<int:category_id>", methods=["DELETE"])
@login_required
def delete(category_id):
    service.delete(category_id)
    return success(message="删除成功")


@categories_bp.route("/api/categories/<int:category_id>/devices", methods=["GET"])
@login_required
def get_devices(category_id):
    result = service.get_devices(category_id)
    return success(data={"devices": result})
