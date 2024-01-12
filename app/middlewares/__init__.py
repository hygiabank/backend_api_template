import time
import logging
from fastapi import FastAPI, Request
from starlette.middleware.base import BaseHTTPMiddleware

logging.basicConfig(level=logging.INFO)

class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        process_time = process_time * 1000
        process_time = round(process_time, 2)
        logging.info(f"\nRequest: {request.url.path} completed in {process_time} milliseconds")
        return response
    


def init_middlewares(app: FastAPI) -> None:
    app.add_middleware(ProcessTimeMiddleware)