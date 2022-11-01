import json
import time
import traceback
from dataclasses import asdict, dataclass
from typing import Any, Callable, Literal
from uuid import uuid4

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from app.utils.error_code import ERR_NUM_500
from app.utils.loggers import json_logger as logger


@dataclass(frozen=True)
class AuditLog:
    duration: float
    code: int
    data: Any
    msg: str
    ip: str
    method: Literal["GET", "POST", "PUT", "DELETE"]
    user: str
    path: str
    path_params: str | int
    query_params: dict
    payload: dict
    x_request_id: uuid4

    def dict(self):
        return asdict(self)


class AuditRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handeler = super().get_route_handler()

        async def audit_route_hanlder(request: Request) -> Response:
            before = time.time()
            try:
                response: Response = await original_route_handeler(request)
            except Exception as e:
                logger.error(traceback.format_exc())
                rsp = ERR_NUM_500.dict
                rsp["data"] = str(e)
                response = JSONResponse(status_code=200, content=rsp)
            payload = None
            if request.method in ["POST", "PUT"]:
                payload = await request.body()
            else:
                payload = None
            duration = time.time() - before
            result = json.loads(response.body.decode("utf-8"))
            data = AuditLog(
                duration=duration,
                code=result["code"],
                data=result.get("data", None),
                msg=result["msg"],
                ip=request.client.host,
                method=request.method,
                user=request.state.current_user,
                path=request.url.path,
                path_params=request.path_params if request.path_params else None,
                query_params=request.query_params._dict
                if request.query_params
                else None,
                payload=payload,
            )
            logger.info(data.dict())
            return response

        return audit_route_hanlder
