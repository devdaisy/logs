from db.config import async_session
from db.dals.query_dal import QueryDAL, QueryLogDAL, SavedQueryDAL
from db.dals.user_dal import UserDAL
from sqlalchemy import exc


async def get_query_dal():
    async with async_session() as session:
        async with session.begin():
        	yield QueryDAL(session)


async def get_log_dal():
    async with async_session() as session:
        async with session.begin():
            yield QueryLogDAL(session)

async def get_save_dal():
    async with async_session() as session:
        async with session.begin():
            yield SavedQueryDAL(session)

async def get_user_dal():
    async with async_session() as session:
        async with session.begin():
            yield UserDAL(session)