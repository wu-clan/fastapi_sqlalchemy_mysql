#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from backend.app.common.log import log
from backend.app.core.conf import settings
from backend.app.utils.generate_string import get_uuid

_only_one = get_uuid()

SEND_RESET_PASSWORD_TEXT = f'您的重置密码验证码为：{_only_one}\n为了不影响您正常使用，请在{int(settings.COOKIES_MAX_AGE / 60)}分钟内完成密码重置'


def send_email_verification_code(send_to, code, text=SEND_RESET_PASSWORD_TEXT):
    """
    发送电子邮件验证码
    :param send_to: 收件人
    :param code: 验证码
    :param text: 邮件文本内容
    :return:
    """
    _text = text.replace(_only_one, code)
    message = MIMEMultipart()
    subject = settings.EMAIL_DESCRIPTION
    content = MIMEText(_text, _charset="utf-8")
    message['from'] = settings.EMAIL_USER
    message['subject'] = subject
    message.attach(content)

    # 登录smtp服务器并发送邮件
    try:
        smtp = smtplib.SMTP()
        smtp.connect(settings.EMAIL_SERVER)
        smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        smtp.sendmail(message['from'], send_to, message.as_string())
    except Exception as e:
        log.error('邮件发送失败 {}', e)
    smtp.quit()


if __name__ == '__main__':
    try:
        send_email_verification_code('xxx@qq.com', 'test')
    except Exception as e:
        print('fail')
        raise e
    print('success')
