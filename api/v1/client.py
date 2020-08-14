import logging
from typing import Any, List

from fastapi import APIRouter

from crud import client as crud
from models.client import Client, ClientCreate, ClientUpdate


router = APIRouter()


@router.get(
    "",
    summary="Get clients",
    response_model=List[Client]
)
async def get(license: str, limit: int=20, skip: int=0):
    '''License: license's slug or * (all)'''
    logging.info(">>> " + __name__ + ":get")
    return await crud.find_many(license, limit, skip)


@router.post(
    "",
    summary="Create client",
    response_model=Client
)
async def create(data: ClientCreate):
    '''Required: `license, name`'''
    logging.info(">>> " + __name__ + ":create")
    return await crud.insert_one(data)


@router.get(
    "/{id}",
    summary="Find client",
    response_model=Client
)
async def find(license: str, id: str):
    '''Required: `license, id`'''
    logging.info(">>> " + __name__ + ":find")
    return await crud.find_one(license, id)


@router.put(
    "/{id}",
    summary="Update client",
    response_model=Client
)
async def update(license: str, id: str, data: ClientUpdate):
    '''Required: `license, id, data`'''
    logging.info(">>> " + __name__ + ":update")
    return await crud.update_one(license, id, data)


@router.delete(
    "/{id}",
    summary="Delete client",
    response_model=Any
)
async def delete(license: str, id: str):
    '''Required: `license, id`'''
    logging.info(">>> " + __name__ + ":find")
    return await crud.delete(license, id)
