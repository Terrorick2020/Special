from dotenv import load_dotenv
from pathlib import Path

import os


env_path = Path(__file__).resolve().parent.parent.parent / '.env'

load_dotenv(env_path)


HOST  = os.getenv( 'HOST', 'localhost' )
PORT  = int( os.getenv( 'PORT', 8080 ) )
MODE  = os.getenv( 'MODE', 'dev' )
isDev = MODE == 'dev'

DB_HOST     = os.getenv( 'DB_HOST' )
DB_PORT     = int( os.getenv( 'DB_PORT' ) )
DB_USER     = os.getenv( 'DB_USER' )
DB_PASSWORD = os.getenv( 'DB_PASSWORD' )
DB_NAME     = os.getenv( 'DB_NAME' )

CLAUD_API_HOST = os.getenv( 'CLAUD_API_HOST' )
CLAUD_API_KEY  = os.getenv( 'CLAUD_API_KEY' )

if  ( not DB_HOST )        or \
    ( not DB_PORT )        or \
    ( not DB_USER )        or \
    ( not DB_PASSWORD )    or \
    ( not DB_NAME )        or \
    ( not CLAUD_API_HOST ) or \
    ( not CLAUD_API_KEY )     \
:
    raise Exception( 'Отсутствуют важные для приложения окружающие среды!' )
