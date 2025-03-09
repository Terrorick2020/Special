from fastapi import APIRouter
from starlette.status import HTTP_200_OK

from . import hello_service
from config.routes_config import api_routes


hello_router = APIRouter()

@hello_router.get(
    api_routes.hello.inner.preview,
    tags = ['Test router'],
    summary = 'Проверка работоспособности сервиса!',
    status_code = HTTP_200_OK,
    responses = {
        HTTP_200_OK: {
            'block': 'hello',
            'message': 'success',
        },
    },
)
async def hello():
    hello_res = await hello_service.hello()
    return hello_res
