from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import URL, create_engine, text
from .config import db_settings


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

with sync_engine.connect() as conn:
    query = text( 'SELECT VERSION();' )
    res = conn.execute( query )
    print( f'{res=}' )