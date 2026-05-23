from .response import error


class AppException(Exception):
    def __init__(self, code=500, message="系统异常，请稍后重试"):
        self.code = code
        self.message = message
        super().__init__(message)


class BadRequestException(AppException):
    def __init__(self, message="参数校验失败"):
        super().__init__(400, message)


class UnauthorizedException(AppException):
    def __init__(self, message="未授权访问，请先登录"):
        super().__init__(401, message)


class ForbiddenException(AppException):
    def __init__(self, message="权限不足，无法执行此操作"):
        super().__init__(403, message)


class NotFoundException(AppException):
    def __init__(self, message="资源不存在"):
        super().__init__(404, message)


class BusinessConflictException(AppException):
    def __init__(self, message="业务冲突"):
        super().__init__(409, message)


def register_error_handlers(app):
    @app.errorhandler(AppException)
    def handle_app_exception(e):
        return error(e.code, e.message)

    @app.errorhandler(400)
    def handle_400(e):
        return error(400, "参数校验失败")

    @app.errorhandler(401)
    def handle_401(e):
        return error(401, "未授权访问，请先登录")

    @app.errorhandler(403)
    def handle_403(e):
        return error(403, "权限不足，无法执行此操作")

    @app.errorhandler(404)
    def handle_404(e):
        return error(404, "接口不存在")

    @app.errorhandler(405)
    def handle_405(e):
        return error(405, "请求方法不允许")

    @app.errorhandler(500)
    def handle_500(e):
        app.logger.error(f"Internal server error: {e}")
        return error(500, "系统异常，请稍后重试")
