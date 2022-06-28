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


def send_verification_code_email(send_to, code, text=SEND_RESET_PASSWORD_TEXT):
    """
    发送电子邮件验证码

    :param send_to: 收件人
    :param code: 验证码
    :param text: 邮件文本内容
    :return:
    """
    _text = text.replace(_only_one, code)
    message = MIMEMultipart()
    message['subject'] = settings.EMAIL_DESCRIPTION
    message['from'] = settings.EMAIL_USER
    message.attach(MIMEText(_text, _charset="utf-8"))

    # 登录smtp服务器并发送邮件
    try:
        if settings.EMAIL_SSL:
            smtp = smtplib.SMTP_SSL(host=settings.EMAIL_SERVER, port=settings.EMAIL_PORT)
        else:
            smtp = smtplib.SMTP(host=settings.EMAIL_SERVER, port=settings.EMAIL_PORT)
        smtp.login(settings.EMAIL_USER, settings.EMAIL_PASSWORD)
        smtp.sendmail(message['from'], send_to, message.as_string())
        smtp.quit()
    except Exception as e:
        log.error('邮件发送失败 {}', e)
        raise Exception('邮件发送失败 {}'.format(e))
