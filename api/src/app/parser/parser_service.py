from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK, HTTP_201_CREATED


async def get_info():
    get_info_res_content = {
        'block': 'get_info',
        'message': 'success',
    }

    return JSONResponse(
        content     = get_info_res_content,
        status_code = HTTP_200_OK,
    )

async def parse_info():
    parse_info_res_content = {
        'block': 'parse_info',
        'message': 'success',
    }

    return JSONResponse(
        content     = parse_info_res_content,
        status_code = HTTP_201_CREATED,
    )

async def accamulation_info():
    accamulation_info_res_content = {
        'block': 'accamulation_info',
        'message': 'success',
    }

    return JSONResponse(
        content     = accamulation_info_res_content,
        status_code = HTTP_201_CREATED,
    )
