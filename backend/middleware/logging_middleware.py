import time
import logging
import os
from logging.handlers import RotatingFileHandler
from flask import request, g
from config import Config


def setup_logging(app):
    log_dir = os.path.dirname(Config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    file_handler = RotatingFileHandler(
        Config.LOG_FILE,
        maxBytes=Config.LOG_MAX_BYTES,
        backupCount=Config.LOG_BACKUP_COUNT,
        encoding="utf-8",
    )
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(formatter)

    app.logger.addHandler(file_handler)
    app.logger.addHandler(console_handler)
    app.logger.setLevel(logging.DEBUG)


def register_logging_middleware(app):
    @app.before_request
    def before_request():
        g.start_time = time.time()

    @app.after_request
    def after_request(response):
        elapsed = int((time.time() - g.get("start_time", time.time())) * 1000)
        client_ip = request.headers.get("X-Forwarded-For", request.remote_addr)

        log_msg = (
            f"{request.method:7s} | {request.path:30s} | IP: {client_ip:15s} | "
            f"Status: {response.status_code} | {elapsed:5d}ms"
        )

        if response.status_code >= 500:
            app.logger.error(log_msg)
        elif response.status_code >= 400:
            app.logger.warning(log_msg)
        else:
            app.logger.info(log_msg)

        return response
