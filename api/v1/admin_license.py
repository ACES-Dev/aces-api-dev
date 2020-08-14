import logging
from typing import Any, List

from fastapi import APIRouter

from crud import license as crud
from models.license import License, LicenseCreate, LicenseUpdate


router = APIRouter()


@router.get(
    "",
    summary="Get licenses",
    response_model=List[License]
)
async def get(limit: int=20, skip: int=0):
    logging.info(">>> " + __name__ + ":get")
    return await crud.find_many(limit, skip)


@router.post(
    "",
    summary="Create licenses",
    response_model=License
)
async def create(data: LicenseCreate):
    '''Required: `slug, type, licenseName, contactName, contactEmail,
    publishedBy, publishDate`
    '''
    logging.info(">>> " + __name__ + ":create")
    return await crud.insert_one(data)


@router.get(
    "/{slug}",
    summary="Find license",
    response_model=License
)
async def find(slug: str):
    '''Required: `slug`'''
    logging.info(">>> " + __name__ + ":find")
    return await crud.find_one(slug)


@router.put(
    "/{slug}",
    summary="Update license",
    response_model=License
)
async def update(slug: str, data: LicenseUpdate):
    '''Required: `slug`'''
    logging.info(">>> " + __name__ + ":update")
    return await crud.update_one(slug, data)
