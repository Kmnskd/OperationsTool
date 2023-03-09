from flask import Flask
from .init_mail import init_mail


def init_plugs(app: Flask) -> None:
    init_mail(app)
