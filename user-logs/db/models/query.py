from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from datetime import datetime
from db.config import Base

class Query(Base):
    __tablename__ = 'queries'

    queryhash = Column(String, primary_key=True)
    query_type = Column(String)
    query_params = Column(String)
    cached = Column(Boolean, default=False)
    cache_file = Column(String, default='')

class SavedQuery(Base):
    __tablename__ = 'saved_queries'

    savedid = Column(Integer, primary_key=True)
    queryhash = Column(String, ForeignKey('queries.queryhash'), index=True)
    userid = Column(Integer, index=True)#ForeignKey('users.userid'), index=True)
    alerts = Column(Boolean)

class QueryLog(Base):
    __tablename__ = 'query_logs'

    logid = Column(Integer, primary_key=True)
    queryhash = Column(String, ForeignKey('queries.queryhash'), index=True)
    userid = Column(Integer, index=True)#ForeignKey('users.userid'), index=True)
    rows_returned = Column(Integer)
    timestamp = Column(TIMESTAMP, default=datetime.now)