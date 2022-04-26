#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from typing import Any, Optional

from fastapi import HTTPException, Request, status
from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError, ValidationError
from fastapi.responses import JSONResponse
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


class Response400(ResponseBase):
    code: int = 400
    msg: Optional[Any] = Field(default='Bad Request')


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
说明：自定义响应状态码
"""


class Response40001(ResponseBase):
    code: int = 40001
    msg: Optional[Any] = Field(default='Request Validation Error')


"""
说明: 自定义异常
"""


class AuthorizationError(Exception):
    def __init__(self, err: str = 'Permission denied'):
        self.err = err


class TokenError(Exception):
    def __init__(self, err: str = 'Token is invalid'):
        self.err = err


"""
说明: 全局异常捕获
"""


def register_exception(app):
    @app.exception_handler(AuthorizationError)
    def authorization_error(request: Request, exc: AuthorizationError):
        """
        用户权限异常
        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(Response401(msg=exc.err))
        )

    @app.exception_handler(TokenError)
    def token_error(request: Request, exc: TokenError):
        """
        Token异常
        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=jsonable_encoder(Response401(msg=exc.err))
        )

    @app.exception_handler(HTTPException)
    def http_exception_handler(request: Request, exc: HTTPException):
        """
        全局HTTP异常处理
        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=exc.status_code,
            content=jsonable_encoder(Response400(code=exc.status_code, msg=exc.detail)),
            headers=exc.headers
        )

    @app.exception_handler(Exception)
    def all_exception_handler(request: Request, exc: Exception):
        """
        全局异常处理
        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content=jsonable_encoder(Response500(msg=exc.args))
        )

    @app.exception_handler(ValidationError)
    def validation_error(request: Request, exc: ValidationError):
        """
        全局请求数据验证异常处理, 此异常处理主要用于Pydantic类中的数据验证
        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(Response40001(msg=exc.errors(), data=exc.json()))
        )

    @app.exception_handler(RequestValidationError)
    def request_validation_error(request: Request, exc: RequestValidationError):
        """
        全局请求数据验证异常处理
        :param request:
        :param exc:
        :return:
        """
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(Response40001(msg=exc.errors(), data=exc.body))
        )
