import re
from models import db
from models.employee import Employee
from utils.exceptions import NotFoundException, BadRequestException


def validate_employee_data(name, age, email):
    errors = []

    if not name or len(name) < 1 or len(name) > 20:
        errors.append("姓名长度必须在1-20字符之间")
    if not isinstance(age, int) or age < 18 or age > 60:
        errors.append("年龄必须在18-60之间")
    if not re.match(r"^[^\s@]+@[^\s@]+\.[^\s@]+$", email):
        errors.append("邮箱格式不正确")

    if errors:
        raise BadRequestException("参数校验失败：" + "；".join(errors))


def get_all():
    employees = Employee.query.order_by(Employee.created_at.desc()).all()
    return [
        {
            "id": str(e.id),
            "name": e.name,
            "age": e.age,
            "email": e.email,
            "createdAt": e.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
        }
        for e in employees
    ]


def get_by_id(employee_id):
    emp = db.session.get(Employee, employee_id)
    if not emp:
        raise NotFoundException("员工不存在")
    return {
        "id": str(emp.id),
        "name": emp.name,
        "age": emp.age,
        "email": emp.email,
        "createdAt": emp.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def create(data):
    validate_employee_data(data["name"], data["age"], data["email"])
    emp = Employee(name=data["name"], age=data["age"], email=data["email"])
    db.session.add(emp)
    db.session.commit()
    return {
        "id": str(emp.id),
        "name": emp.name,
        "age": emp.age,
        "email": emp.email,
        "createdAt": emp.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def update(employee_id, data):
    emp = db.session.get(Employee, employee_id)
    if not emp:
        raise NotFoundException("员工不存在")

    name = data.get("name", emp.name)
    age = data.get("age", emp.age)
    email = data.get("email", emp.email)
    validate_employee_data(name, age, email)

    emp.name = name
    emp.age = age
    emp.email = email
    db.session.commit()
    return {
        "id": str(emp.id),
        "name": emp.name,
        "age": emp.age,
        "email": emp.email,
        "createdAt": emp.created_at.strftime("%Y-%m-%dT%H:%M:%S"),
    }


def delete(employee_id):
    emp = db.session.get(Employee, employee_id)
    if not emp:
        raise NotFoundException("员工不存在")
    db.session.delete(emp)
    db.session.commit()
