from fastapi import Request, Response, status
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import traceback
from model import StatusInfo
from fastapi.encoders import jsonable_encoder
import logging
LOG = logging.getLogger(__name__)


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next) -> Response:
        try:
            response: Response = await call_next(request)
            if response.status_code != 200:
                LOG.error(traceback.format_exc())
                response = JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))
        except Exception as e:
            LOG.error(traceback.format_exc())
            response = JSONResponse(content=jsonable_encoder(StatusInfo(status="ERROR", message=traceback.format_exc())))

        return response
