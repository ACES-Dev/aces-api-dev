import logging
from bson.objectid import ObjectId
from pymongo import ReturnDocument

from core.config import (
    DOCTYPE_USER as DOCUMENT_TYPE,
    ERROR_MONGODB_DELETE,
    ERROR_MONGODB_UPDATE,
)
from core.security import get_password_hash
from db.mongo import get_collection
from models.user import (
    BaseModel,
    User,
    UserCreate,
    UserInDB,
    UserUpdate,
    UserInfoUpdate
)
from crud.license import is_license_valid
from crud.utils import (
    delete_empty_keys,
    fields_in_create,
    fields_in_update,
    raise_bad_request,
    raise_not_found,
    raise_server_error,
)


def _seek(license: str):
    slug = license.strip().lower()
    if slug == "all" or slug == "*":
        return {}
    else:
        return {"license": slug}


def _seek_user(license: str, search: str):
    seek = _seek(license)
    search = search.strip().lower()
    if ObjectId.is_valid(search):
        seek["_id"] = ObjectId(search)
    elif "@" in search and "." in search:
        seek["email"] = search
    else:
        seek["username"] = search
    return seek


async def find_many(license:str, limit: int, skip: int):
    logging.info(">>> " + __name__ + ":find_many")
    collection = get_collection(DOCUMENT_TYPE)
    seek = _seek(license)
    rs: List[User] = []
    cursor = collection.find(seek, limit=limit, skip=skip)
    async for row in cursor:
        rs.append(row)
    return rs


async def insert_one(data: UserCreate):
    logging.info(">>> " + __name__ + ":insert_one")

    # Check license
    valid = await is_license_valid(data.license)
    if not valid:
        raise_bad_request("License is not valid")

    collection = get_collection(DOCUMENT_TYPE)
    hashed_password = get_password_hash(data.password)
    model = UserInDB(**data.dict(), hashed_password=hashed_password)
    props = fields_in_create(model)

    try:
        rs = await collection.insert_one(props)
        if rs.inserted_id:
            user = await collection.find_one({"_id": rs.inserted_id})
            return user
    except Exception as e:
        logging.info(e)
        raise_server_error(str(e))


async def find_one(license: str, search: str):
    logging.info(">>> " + __name__ + ":find_one")

    collection = get_collection(DOCUMENT_TYPE)
    seek = _seek_user(license, search)
    found = await collection.find_one(seek)
    return found if found else raise_not_found()


# async def update_one(license: str, search: str, data: UserUpdate):
async def update_one(license: str, search: str, data: BaseModel):
    logging.info(">>> " + __name__ + ":update_one")

    props = delete_empty_keys(data)
    logging.info( props )
    if len(props) == 0:
        raise_bad_request("No data supplied")

    collection = get_collection(DOCUMENT_TYPE)
    seek = _seek_user(license, search)
    rs = await collection.find_one_and_update(
        seek,
        {"$set": fields_in_update(props)},
        return_document=ReturnDocument.AFTER
    )

    return rs if rs else raise_server_error(ERROR_MONGODB_UPDATE)


async def delete(license: str, search: str):
    logging.info(">>> " + __name__ + ":delete")

    collection = get_collection(DOCUMENT_TYPE)
    seek = _seek_user(license, search)

    # Do not delete license owner
    seek["licenseContact"] = False

    found = await collection.find_one_and_delete(
        seek,
        {"_id": True}
    )
    logging.info(found)
    message = {"message": "User deleted"}
    return message if found else raise_server_error(ERROR_MONGODB_DELETE)
