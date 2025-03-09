from fastapi import Fastapi
import uvicorn

from .config import main_config
from .config.routes_config import api_routes
from .app.hello.hello_routes import hello_router
from .app.parser.parser_routes import parser_router


def main():
    try:
        app = Fastapi()

        api_prefix = api_routes.prefix if main_config.isDev else ''

        hello_glob = api_routes.hello.glob
        hello_prefix = f'{api_prefix}{hello_glob}'

        parser_glob = api_routes.parser.glob
        parser_prefix = f'{api_prefix}{parser_glob}'

        app.include_router( hello_router, prefix = hello_prefix )
        app.include_router( parser_router, prefix = parser_prefix )

        uvicorn.run(
            app    = app,
            host   = main_config.HOST,
            port   = main_config.PORT,
            reload = main_config.isDev,
        )
    except Exception as ex:
        print(ex)
    finally:
        print('Сервер закончил работу!')
    

if __name__ == "__main__":
    main()
