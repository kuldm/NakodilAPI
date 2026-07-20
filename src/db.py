from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from config import settings

engine = create_async_engine(settings.DATABASE_URL, pool_pre_ping=True)

async_session_maker = async_sessionmaker(bind=engine, expire_on_commit=False)

sassion = async_session_maker()


class Base(DeclarativeBase):
    pass
