import logging
from typing import Any, List

from fastapi import APIRouter

from crud import license as crud
from models.license import License, LicenseInfoUpdate


router = APIRouter()


@router.get(
    "/{slug}",
    summary="Get license info",
    response_model=License
)
async def find(slug: str):
    '''Required: `slug`'''
    logging.info(">>> " + __name__ + ":find")
    return await crud.find_one(slug)


@router.put(
    "/{slug}",
    summary="Update license info",
    response_model=License
)
async def update(slug: str, data: LicenseInfoUpdate):
    '''Required: `slug` and `body` not empty'''
    logging.info(">>> " + __name__ + ":update")
    return await crud.update_one(slug, data)
