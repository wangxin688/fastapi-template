from app.utils.error_code import ERR_NUM_4001, ERR_NUM_4003, ERR_NUM_4004

__all__ = (
    "TokenInvalidExpiredError",
    "RefreshTokenInvalidExpiredError",
    "PermissionDenyError",
    "ResourceNotFoundError",
)


class TokenInvalidExpiredError(Exception):
    def __init__(self, err_msg: str = ERR_NUM_4001.msg):
        self.err_msg = err_msg


class RefreshTokenInvalidExpiredError(Exception):
    def __init__(self, err_msg: str = ERR_NUM_4001.msg):
        self.err_msg = err_msg


class PermissionDenyError(Exception):
    def __init__(self, err_msg: str = ERR_NUM_4003.msg):
        self.err_msg = err_msg


class ResourceNotFoundError(Exception):
    def __init__(self, err_msg: str = ERR_NUM_4004.msg):
        self.err_msg = err_msg
