from models import db
from models.device import Device
from models.category import Category
from utils.exceptions import NotFoundException, BadRequestException


def get_all():
    devices = Device.query.all()
    return [
        {
            "id": str(d.id),
            "name": d.name,
            "model": d.model or "",
            "categoryId": str(d.category_id),
            "categoryName": d.category.name if d.category else "",
        }
        for d in devices
    ]


def get_by_id(device_id):
    dev = db.session.get(Device, device_id)
    if not dev:
        raise NotFoundException("设备不存在")
    return {
        "id": str(dev.id),
        "name": dev.name,
        "model": dev.model or "",
        "categoryId": str(dev.category_id),
        "categoryName": dev.category.name if dev.category else "",
    }


def create(data):
    name = data.get("name", "")
    if not name:
        raise BadRequestException("参数校验失败：设备名称不能为空")

    category_id = data.get("categoryId")
    category = db.session.get(Category, int(category_id)) if category_id else None
    if not category:
        raise BadRequestException("参数校验失败：所属分类不存在")

    dev = Device(
        name=name,
        model=data.get("model", ""),
        category_id=int(category_id),
    )
    db.session.add(dev)
    db.session.commit()
    return {
        "id": str(dev.id),
        "name": dev.name,
        "model": dev.model or "",
        "categoryId": str(dev.category_id),
        "categoryName": dev.category.name,
    }


def update(device_id, data):
    dev = db.session.get(Device, device_id)
    if not dev:
        raise NotFoundException("设备不存在")

    name = data.get("name", dev.name)
    if not name:
        raise BadRequestException("参数校验失败：设备名称不能为空")

    category_id = data.get("categoryId")
    if category_id:
        category = db.session.get(Category, int(category_id))
        if not category:
            raise BadRequestException("参数校验失败：所属分类不存在")
        dev.category_id = int(category_id)

    dev.name = name
    dev.model = data.get("model", dev.model)
    db.session.commit()
    return {
        "id": str(dev.id),
        "name": dev.name,
        "model": dev.model or "",
        "categoryId": str(dev.category_id),
        "categoryName": dev.category.name if dev.category else "",
    }


def delete(device_id):
    dev = db.session.get(Device, device_id)
    if not dev:
        raise NotFoundException("设备不存在")
    db.session.delete(dev)
    db.session.commit()
