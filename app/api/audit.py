import json
import time
import traceback
from typing import  Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from fastapi.routing import APIRoute

from app.utils.loggers import json_logger as logger
from app.utils.error_code import ERR_NUM_500


class AuditRoute(APIRoute):
    def get_route_handler(self) -> Callable:
        original_route_handeler = super().get_route_handler()

        async def audit_route_hanlder(request: Request)-> Response:
            before = time.time()
            try:
                response: Response = await original_route_handeler(request)
            except Exception as e:
                logger.error(traceback.format_exc())
                rsp = ERR_NUM_500.dict
                rsp["data"] = str(e)
                response = JSONResponse(status_code=200, content=rsp)
            rsp_status_code = response.status_code
            payload = None
            try:
                payload = await request.body()
            except Exception as e:
                logger.error(e)
            duration = time.time() - before
            result = json.loads(response.body.decode("utf-8"))
            audit_log = {
                
            }

