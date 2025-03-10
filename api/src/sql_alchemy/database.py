from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from .config import db_settings
from .modals import Base


class DBController:
    hello = 'dvsdv'

sync_engine = create_engine(
    url          = db_settings.DB_URL_psycopg,
    echo         = True,
    pool_size    = 5,
    max_overflow = 10,
)

async_engine = create_async_engine(
    url  = db_settings.DB_URL_asyncpg,
    echo = False
)

def sync_test_db():
    with sync_engine.connect() as conn:
        query = text( 'SELECT VERSION();' )
        res = conn.execute( query )
        print( f'{res=}' )

def async_test_db():
    with async_engine.connect() as conn:
        query = text( 'SELECT VERSION();' )
        res = conn.execute( query )
        print( f'{res=}' )

def sync_create_db_and_tables() -> None:
	Base.metadata.create_all(sync_engine)

async def async_create_db_and_tables() -> None:
	Base.metadata.create_all(async_engine) 

with sync_engine.connect() as conn:
    query = text( 'SELECT VERSION();' )
    res = conn.execute( query )
    print( f'{res=}' )