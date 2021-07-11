from typing import List, Optional

from fastapi import APIRouter, Depends

from sqlalchemy import exc
from db.dals.query_dal import QueryDAL
from dependencies import get_query_dal

router = APIRouter()


@router.post("/query")
async def create(query_type:str,
			query_params:str,
            query_dal: QueryDAL = Depends(get_query_dal)):
    try:
    	await query_dal.create(query_type, query_params)
    	await query_dal.db_session.commit()
    	return 'created!'
    except exc.IntegrityError:
    	return 'already exists!'



@router.put("/query/{query_type}")
async def update(query_type: str, 
				query_params:str,
				cache_file:str,
				cached:bool,
                query_dal: QueryDAL = Depends(get_query_dal)):
    return await query_dal.update(query_type, query_params, cache_file, cached)


@router.get("/query/{query_type}")
async def read(query_type: str, 
				query_params:str,
				query_dal: QueryDAL = Depends(get_query_dal)):
    return await query_dal.read(query_type, query_params)

