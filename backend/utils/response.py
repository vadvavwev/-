from flask import jsonify


def success(data=None, message="成功"):
    return jsonify({"code": 200, "message": message, "data": data}), 200


def error(code=500, message="系统异常，请稍后重试", data=None):
    return jsonify({"code": code, "message": message, "data": data}), code
