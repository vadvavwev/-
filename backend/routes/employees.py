from flask import Blueprint, request
from middleware.auth_middleware import login_required
from utils.response import success
import services.employee_service as service

employees_bp = Blueprint("employees", __name__)


@employees_bp.route("/api/employees", methods=["GET"])
@login_required
def get_all():
    result = service.get_all()
    return success(data={"employees": result})


@employees_bp.route("/api/employees/<int:employee_id>", methods=["GET"])
@login_required
def get_by_id(employee_id):
    result = service.get_by_id(employee_id)
    return success(data=result)


@employees_bp.route("/api/employees", methods=["POST"])
@login_required
def create():
    data = request.get_json(silent=True) or {}
    result = service.create(data)
    return success(data=result, message="添加成功")


@employees_bp.route("/api/employees/<int:employee_id>", methods=["PUT"])
@login_required
def update(employee_id):
    data = request.get_json(silent=True) or {}
    result = service.update(employee_id, data)
    return success(data=result, message="修改成功")


@employees_bp.route("/api/employees/<int:employee_id>", methods=["DELETE"])
@login_required
def delete(employee_id):
    service.delete(employee_id)
    return success(message="删除成功")
