class BaseConfig:
    # 邮箱配置
    # MAIL_USE_TLS = False
    # MAIL_USE_SSL = True
    MAIL_USERNAME = "xxx"
    MAIL_SERVER = "xxx.xxx.xxx.xxx"
    MAIL_PORT = 25
    MAIL_PASSWORD = ""

    SECRET_KEY = ''
    EMAIL_BODY_REGISTER = """
    邮件主体
        """
    EMAIL_BODY_RESET_PASSWD = """
    邮件主体
    """
    BODY_SELECT = {
        "reset": {"subject": "subject", "body": EMAIL_BODY_RESET_PASSWD},
        "register": {"subject": "subject", "body": EMAIL_BODY_REGISTER}
        }
