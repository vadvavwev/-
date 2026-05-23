from flask import Blueprint, request
from middleware.auth_middleware import login_required
from utils.response import success
import services.device_service as service

devices_bp = Blueprint("devices", __name__)


@devices_bp.route("/api/devices", methods=["GET"])
@login_required
def get_all():
    result = service.get_all()
    return success(data={"devices": result})


@devices_bp.route("/api/devices/<int:device_id>", methods=["GET"])
@login_required
def get_by_id(device_id):
    result = service.get_by_id(device_id)
    return success(data=result)


@devices_bp.route("/api/devices", methods=["POST"])
@login_required
def create():
    data = request.get_json(silent=True) or {}
    result = service.create(data)
    return success(data=result, message="添加成功")


@devices_bp.route("/api/devices/<int:device_id>", methods=["PUT"])
@login_required
def update(device_id):
    data = request.get_json(silent=True) or {}
    result = service.update(device_id, data)
    return success(data=result, message="修改成功")


@devices_bp.route("/api/devices/<int:device_id>", methods=["DELETE"])
@login_required
def delete(device_id):
    service.delete(device_id)
    return success(message="删除成功")
