from typing import List, Optional
from datetime import datetime

from sqlalchemy import update
from sqlalchemy.future import select
from sqlalchemy.orm import Session

from db.models.user import User

class UserDAL():
    def __init__(self, db_session: Session):
        self.db_session = db_session

    async def register_user(self, userid:int, username:str, email:str):
        user = User(userid=userid, username=username, email=email)
        self.db_session.add(user)
        await self.db_session.flush()

    async def get_user(self, userid:int) -> User:
        q = await self.db_session.execute(select(User).where(User.userid==userid))
        return q.scalars().all()

    async def update_user(self, userid:int, username:str, email:str):
        q = update(User).where(userid==userid)
        if username is not None:
            q = q.values(username=username)
        if email is not None:
            q = q.values(email=email)
        await self.db_session.execute(q)

