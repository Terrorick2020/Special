from fastapi import APIRouter
from starlette.status import HTTP_200_OK, HTTP_201_CREATED

from . import parser_service
from config.routes_config import api_routes


parser_router = APIRouter()

@parser_router.get(
    api_routes.parser.inner.get_info,
    tags = ['Parse router'],
    summary = 'Получение сохранённой в базе данных информации!',
    status_code = HTTP_200_OK,
    responses = {},
)
async def get_info():
    get_info_res = await parser_service.get_info()
    return get_info_res

@parser_router.post(
    api_routes.parser.inner.parse_info,
    tags = ['Parse router'],
    summary = 'Парсинг информации с сайтов!',
    status_code = HTTP_201_CREATED,
    responses = {},
)
async def parse_info():
    parse_info_res = await parser_service.parse_info()
    return parse_info_res

@parser_router.post(
    api_routes.parser.inner.accamulation_info,
    tags = ['Parse router'],
    summary = 'Аккомулирование информации с использованием ИИ!',
    status_code = HTTP_201_CREATED,
    responses = {},
)
async def accamulation_info():
    accamulation_info_res = await parser_service.accamulation_info()
    return accamulation_info_res
