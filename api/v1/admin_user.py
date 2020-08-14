import logging
from typing import Any, List

from fastapi import APIRouter

from crud import user as crud
from models.user import User, UserCreate, UserUpdate


router = APIRouter()


@router.get(
    "",
    summary="Get users",
    response_model=List[User]
)
async def get(license: str, limit: int=20, skip: int=0):
    '''License: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":get")
    return await crud.find_many(license, limit, skip)


@router.post(
    "",
    summary="Create user",
    response_model=User
)
async def create(data: UserCreate):
    '''Required: `license, name, username, email, password`'''
    logging.info(">>> " + __name__ + ":create")
    return await crud.insert_one(data)


@router.get(
    "/{search}",
    summary="Find license user",
    response_model=User
)
async def find(license: str, search: str):
    '''Required: `license, search`'''
    logging.info(">>> " + __name__ + ":find")
    return await crud.find_one(license, search)


@router.put(
    "/{search}",
    summary="Update license user",
    response_model=User
)
async def update(license: str, search: str, data: UserUpdate):
    '''Required: `license, search, data`'''
    logging.info(">>> " + __name__ + ":update")
    return await crud.update_one(license, search, data)


@router.delete(
    "/{search}",
    summary="Delete license user",
    response_model=Any
)
async def delete(license: str, search: str):
    '''Required: `license, search`'''
    logging.info(">>> " + __name__ + ":find")
    return await crud.delete(license, search)
