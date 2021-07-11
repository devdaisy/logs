from typing import List, Optional
from datetime import datetime
import hashlib

from sqlalchemy import update, delete, and_
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.query import Query, SavedQuery, QueryLog
from db.models.user import User


class QueryDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    def get_query_hash(self, query_type, query_params):
        queryhash = query_type+query_params
        queryhash = hashlib.md5(queryhash.encode('utf8'))
        queryhash = queryhash.hexdigest()
        return queryhash

    async def create(self, query_type:str, query_params:str):
        queryhash = self.get_query_hash(query_type, query_params)
        cached_result = ''
        query = Query(queryhash=queryhash, query_type=query_type,
            query_params=query_params)
        self.db_session.add(query)
        await self.db_session.flush()

    async def update(self, query_type:str, query_params:str,
        cache_file:str, cached:bool):
        queryhash = self.get_query_hash(query_type, query_params)
        q = update(Query).where(Query.queryhash == queryhash)
        if cache_file is not None:
            q = q.values(cache_file=cache_file)
        if cached is not None:
            q = q.values(cached=cached)
        q.execution_options(synchronize_session="fetch")
        await self.db_session.execute(q)

    async def read(self, query_type, query_params):
        queryhash = self.get_query_hash(query_type, query_params)
        q = select(Query).where(Query.queryhash==queryhash)
        q = await self.db_session.execute(q)
        return q.scalars().all()


class QueryLogDAL():

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, queryhash:str, userid:int, rows_returned:int):
        q = QueryLog(queryhash=queryhash, userid=userid, rows_returned=rows_returned)
        self.db_session.add(q)
        await self.db_session.flush()

    async def update(self, userid, queryhash, rows_returned):
        q = select(QueryLog).where(and_(QueryLog.userid==userid, QueryLog.queryhash==queryhash))
        q = q.order_by(QueryLog.timestamp.desc()).limit(1)
        q = await self.db_session.execute(q)
        q = q.scalars().all()
        logid = q[0].logid
        q = update(QueryLog).where(QueryLog.logid==logid)
        if rows_returned is not None:
            q = q.values(rows_returned=rows_returned)
        await self.db_session.execute(q)

    async def read(self, userid:int, limit:int) -> List[Query]:
        q = select(QueryLog, Query).join(Query).where(QueryLog.userid==userid)
        q = q.order_by(QueryLog.timestamp.desc()).limit(limit)
        q = await self.db_session.execute(q)
        return q.all()

class SavedQueryDAL():

    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def create(self, queryhash, userid, alerts):
        q = SavedQuery(queryhash=queryhash, userid=userid, alerts=alerts)
        self.db_session.add(q)
        await self.db_session.flush()

    async def update(self, savedid, alerts):
        q = update(SavedQuery).where(SavedQuery.savedid==savedid)
        if alerts is not None:
            q = q.values(alerts=alerts)
        await self.db_session.execute(q)

    async def read(self, userid:int):
        q = select(SavedQuery, Query).join(Query).where(SavedQuery.userid==userid)
        q = await self.db_session.execute(q)
        return q.all()

    async def delete(self, savedid):
        q = delete(SavedQuery).where(SavedQuery.savedid==savedid)
        await self.db_session.execute(q)



