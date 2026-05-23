from models import db
from models.category import Category
from models.device import Device
from utils.exceptions import NotFoundException, BadRequestException, BusinessConflictException


def get_all():
    categories = Category.query.all()
    return [
        {
            "id": str(c.id),
            "name": c.name,
            "deviceCount": Device.query.filter_by(category_id=c.id).count(),
        }
        for c in categories
    ]


def get_by_id(category_id):
    cat = db.session.get(Category, category_id)
    if not cat:
        raise NotFoundException("分类不存在")
    return {
        "id": str(cat.id),
        "name": cat.name,
        "deviceCount": Device.query.filter_by(category_id=cat.id).count(),
    }


def create(data):
    name = data.get("name", "")
    if not name or len(name) < 1 or len(name) > 20:
        raise BadRequestException("参数校验失败：分类名称长度必须在1-20字符之间")

    cat = Category(name=name)
    db.session.add(cat)
    db.session.commit()
    return {"id": str(cat.id), "name": cat.name, "deviceCount": 0}


def update(category_id, data):
    cat = db.session.get(Category, category_id)
    if not cat:
        raise NotFoundException("分类不存在")

    name = data.get("name", "")
    if not name or len(name) < 1 or len(name) > 20:
        raise BadRequestException("参数校验失败：分类名称长度必须在1-20字符之间")

    cat.name = name
    db.session.commit()
    return {
        "id": str(cat.id),
        "name": cat.name,
        "deviceCount": Device.query.filter_by(category_id=cat.id).count(),
    }


def delete(category_id):
    cat = db.session.get(Category, category_id)
    if not cat:
        raise NotFoundException("分类不存在")

    device_count = Device.query.filter_by(category_id=category_id).count()
    if device_count > 0:
        raise BusinessConflictException("分类下存在设备，无法删除")

    db.session.delete(cat)
    db.session.commit()


def get_devices(category_id):
    cat = db.session.get(Category, category_id)
    if not cat:
        raise NotFoundException("分类不存在")

    devices = Device.query.filter_by(category_id=category_id).all()
    return [
        {
            "id": str(d.id),
            "name": d.name,
            "model": d.model or "",
            "categoryId": str(d.category_id),
            "categoryName": cat.name,
        }
        for d in devices
    ]
