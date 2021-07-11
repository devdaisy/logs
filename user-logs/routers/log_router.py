from typing import List, Optional

from fastapi import APIRouter, Depends

from db.dals.query_dal import QueryLogDAL
from dependencies import get_log_dal

router = APIRouter()


@router.post("/log")
async def create(queryhash:str, 
			userid:int, 
			rows_returned:int,
            log_dal: QueryLogDAL = Depends(get_log_dal)):
    return await log_dal.create(queryhash, userid, rows_returned)


@router.put("/log/{userid}")
async def update(userid:int,
				queryhash:str,
				rows_returned:int,
                log_dal: QueryLogDAL = Depends(get_log_dal)):
    return await log_dal.update(userid, queryhash, rows_returned)


@router.get("/log/{userid}")
async def read(userid:int, 
				limit:int,
				log_dal: QueryLogDAL = Depends(get_log_dal)):
    return await log_dal.read(userid, limit)

