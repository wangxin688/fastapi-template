import traceback

from fastapi.exceptions import RequestValidationError
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from pydantic import ValidationError

from app.utils.error_code import ERR_NUM_1, ERR_NUM_4001, ERR_NUM_4003, ERR_NUM_4011
from app.utils.exceptions import (
    PermissionDenyError,
    RefreshTokenInvalidExpiredError,
    TokenInvalidExpiredError,
)
from app.utils.loggers import app_logger as logger


# TODO: update logging msg format and description
async def token_invalid_expired_handler(
    request: Request, exc: TokenInvalidExpiredError
):
    logger.warning(
        "%s\n%s-URL:%s\nHeaders: %s",
        exc.err_msg,
        request.method,
        request.url,
        request.headers,
    )
    return JSONResponse(status_code=200, content=ERR_NUM_4001.dict)


async def refresh_token_invalid_expired_handler(
    request: Request, exc: RefreshTokenInvalidExpiredError
):
    logger.warning(
        "%s\n%s-URL:%s\nHeaders: %s",
        exc.err_msg,
        request.method,
        request.url,
        request.headers,
    )
    return JSONResponse(status_code=200, content=ERR_NUM_4011.dict)


async def permission_deny_handler(request: Request, exc: PermissionDenyError):
    logger.warning(
        "%s\n%s-URL:%s\nHeaders: %s",
        exc.err_msg,
        request.method,
        request.url,
        request.headers,
    )
    return JSONResponse(status_code=200, content=ERR_NUM_4003.dict)


async def request_validation_handler(request: Request, exc: RequestValidationError):
    logger.warning(
        "%s\n%s-URL:%s\nHeaders: %s",
        str(exc),
        request.method,
        request.url,
        request.headers,
    )
    return JSONResponse(
        status_code=200,
        content={"code": ERR_NUM_1.code, "data": str(exc), "msg": ERR_NUM_1.msg},
    )


async def inner_validation_handler(request: Request, exc: ValidationError):
    logger.warning(
        "%s\n%s-URL:%s\nHeaders: %s",
        traceback.format_exc(),
        request.method,
        request.url,
        request.headers,
    )
    return JSONResponse(
        status_code=200,
        content={"code": ERR_NUM_1.code, "data": str(exc), "msg": ERR_NUM_1.msg},
    )


exception_handlers = {
    TokenInvalidExpiredError: token_invalid_expired_handler,
    RefreshTokenInvalidExpiredError: refresh_token_invalid_expired_handler,
    PermissionDenyError: permission_deny_handler,
    RequestValidationError: request_validation_handler,
    ValidationError: inner_validation_handler,
}
