import psutil
from fastapi import FastAPI, APIRouter, Depends
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.utils import get_openapi

from .router import main_router
from .response.errors import BaseHTTPException
from .middleware.key import confirm_api_key
from .database.pg import Base, pg_engine

app = FastAPI(
    docs_url="/documentation"
)

v1 = APIRouter(
    prefix="/v1",
    dependencies=[Depends(confirm_api_key)]
)

# Init database
Base.metadata.create_all(pg_engine)

@app.exception_handler(BaseHTTPException)
def http_exception_handler(request: Request, exc: BaseHTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "ok": False,
            "code": exc.code.value,
            "message": exc.message,
        },
        headers=exc.headers,
    )

@v1.get("/ping", tags=['Ping'])
def ping():
    return "pong"

@v1.get("/load", tags=['Healthcheck'])
def cpu_usage():
    # Get CPU and RAM usage
    _cpu =  psutil.cpu_percent()
    _ram = psutil.virtual_memory().percent
    return { 'cpu': _cpu, 'ram': _ram }

v1.include_router(main_router)
app.include_router(v1)