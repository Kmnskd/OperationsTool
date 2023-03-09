from flask_mail import Message
from init_handler.init_mail import mail
from configs.config import BaseConfig


def send_mail(action, recipients, *args):
    info = BaseConfig.BODY_SELECT.get(action)
    subject = info.get("subject")
    body = info.get("body")

    try:
        msg = Message(subject, sender=BaseConfig.MAIL_USERNAME, recipients=[recipients])
        msg.html = body.format(args[0], args[1])
        mail.send(msg)
    except Exception as e:
        print('邮箱发送出错了', e)
        raise e
