from sqlalchemy import Column, Integer, String, TIMESTAMP, Boolean, ForeignKey
from datetime import datetime
from db.config import Base

class User(Base):
	__tablename__ = 'users'

	userid = Column(Integer, primary_key=True, autoincrement=False)
	username = Column(String)
	email = Column(String)
