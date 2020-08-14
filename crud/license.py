import logging
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_LICENSE as DOCUMENT_TYPE,
    ERROR_MONGODB_UPDATE,
)
from db.mongo import get_collection
from models.license import (
    BaseModel,
    License,
    LicenseCreate,
    LicenseUpdate,
    LicenseInfoUpdate,
)
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


def _seek(license: str):
    return {"slug": license.strip().lower()}


async def is_license_valid(license: str):
    logging.info(">>> " + __name__ + ":is_license_valid")
    collection = get_collection(DOCUMENT_TYPE)
    seek = _seek(license)
    found = await collection.find_one(seek, {"_id": True})
    logging.info(found)
    return True if found else False


async def find_many(limit: int, skip: int):
    logging.info(">>> " + __name__ + ":find_many")
    collection = get_collection(DOCUMENT_TYPE)
    rs: List[License] = []
    cursor = collection.find({}, limit=limit, skip=skip)
    async for row in cursor:
        rs.append(row)
    return rs


async def insert_one(data: LicenseCreate):
    logging.info(">>> " + __name__ + ":insert_one")
    collection = get_collection(DOCUMENT_TYPE)
    props = fields_in_create(data)
    logging.info(props)
    try:
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            license = await collection.find_one({"_id": rs.inserted_id})
            return license
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))


async def find_one(slug: str):
    logging.info(">>> " + __name__ + ":find_one")

    collection = get_collection(DOCUMENT_TYPE)
    seek = _seek(slug)
    found = await collection.find_one(seek)
    return found if found else raise_not_found()


# async def update_one(slug: str, data: LicenseUpdate):
async def update_one(slug: str, data: BaseModel):
    logging.info(">>> " + __name__ + ":update_one")

    props = delete_empty_keys(data)
    logging.info( props )
    if len(props) == 0:
        raise_bad_request("No data supplied")

    collection = get_collection(DOCUMENT_TYPE)
    seek = _seek(slug)

    rs = await collection.find_one_and_update(
        seek,
        {"$set": fields_in_update(props)},
        return_document=ReturnDocument.AFTER
    )
    return rs if rs else raise_server_error(ERROR_MONGODB_UPDATE)


# async def update_info(slug: str, data: LicenseUpdateInfo):
