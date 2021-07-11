from typing import List, Optional

from fastapi import APIRouter, Depends

from db.dals.query_dal import SavedQueryDAL
from dependencies import get_save_dal

router = APIRouter()


@router.post("/save")
async def create(queryhash:str, userid:int, alerts:bool,
            save_dal: SavedQueryDAL = Depends(get_save_dal)):
    return await save_dal.create(queryhash, userid, alerts)


@router.put("/save/{savedid}")
async def update(savedid:int,
				alerts:bool,
                save_dal: SavedQueryDAL = Depends(get_save_dal)):
    return await save_dal.update(savedid, alerts)


@router.get("/save/{query_type}")
async def read(userid: int, 
				save_dal: SavedQueryDAL = Depends(get_save_dal)):
    return await save_dal.read(userid)

@router.delete("/save/{savedid}")
async def delete(savedid:int,
                save_dal: SavedQueryDAL = Depends(get_save_dal)):
    return await save_dal.delete(savedid)