import asyncio
import logging
from typing import Literal

import httpx

async def http_req(
        method: Literal["GET", "POST", "PUT", "DELETE", "PATCH"],
        url: str,
        headers: dict = None,
        payload: dict = None,
):
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.request(
                method=method,
                url=url,
                headers=headers,
                data=payload
            )
        except httpx.RequestError as e:
            logging.error(f"{url} request failed, {e}")
        assert resp.status_code in [200, 201], resp.text
        logging.info(f"{url} return code={resp.status_code}, info={resp.text}")
        return resp


# asyncio.run(
#     http_req("GET", "http://www.baidu.com")
# )
