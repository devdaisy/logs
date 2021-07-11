from typing import List, Optional

from fastapi import APIRouter, Depends

from db.dals.user_dal import UserDAL
from db.models.user import User
from dependencies import get_user_dal

router = APIRouter()


@router.post("/user")
async def register_user(userid:int, 
	username:str, 
	email:str, 
	user_dal: UserDAL=Depends(get_user_dal)):
    return await user_dal.register_user(userid=userid, username=username, email=email)


@router.get("/user/{userid}")
async def get_user(userid:int,
 	user_dal: UserDAL = Depends(get_user_dal)) -> User:
    return await user_dal.get_user(userid)

@router.put("/user/{userid}")
async def update_user(userid:int, 
	username: Optional[str]=None, 
	email: Optional[str]=None,
	user_dal: UserDAL = Depends(get_user_dal)):
	return await user_dal.update_user(userid, username, email)