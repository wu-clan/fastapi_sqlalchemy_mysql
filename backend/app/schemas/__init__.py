#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Optional

from fastapi import HTTPException, status
from pydantic import BaseModel, Field

"""
说明：统一响应状态码
"""


class ResponseBase(BaseModel):
    data: Optional[Any] = None


class Response200(ResponseBase):
    code: int = 200
    msg: Optional[Any] = Field(default='Success')


class Response301(ResponseBase):
    code: int = 301
    msg: Optional[Any] = Field(default='Moved Permanently')


class Response401(ResponseBase):
    code: int = 401
    msg: Optional[Any] = Field(default='Unauthorized')


class Response403(ResponseBase):
    code: int = 403
    msg: Optional[Any] = Field(default='Forbidden')


class Response404(ResponseBase):
    code: int = 404
    msg: Optional[Any] = Field(default='Not Found')


class Response500(ResponseBase):
    code: int = 500
    msg: Optional[Any] = Field(default='Internal Server Error')


class Response502(ResponseBase):
    code: int = 502
    msg: Optional[Any] = Field(default='Bad Gateway')


"""
说明：统一错误响应
"""


class AuthorizationError(HTTPException):
    def __init__(self):
        super(AuthorizationError, self).__init__(
            status.HTTP_401_UNAUTHORIZED, detail='Permission denied', headers={"WWW-Authenticate": "Bearer"}
        )


class TokenError(HTTPException):
    def __init__(self):
        super(TokenError, self).__init__(
            status.HTTP_401_UNAUTHORIZED, detail='Token Verification Failed', headers={"WWW-Authenticate": "Bearer"}
        )
