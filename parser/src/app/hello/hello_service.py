from fastapi.responses import JSONResponse
from starlette.status import HTTP_200_OK


async def hello():
    hello_res_content = {
        'block': 'hello',
        'message': 'success',
    }

    return JSONResponse(
        content     = hello_res_content,
        status_code = HTTP_200_OK,
    )
