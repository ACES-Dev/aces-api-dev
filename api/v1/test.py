import random
import string
from typing import List
from fastapi import APIRouter

from db.mongo import get_collection, get_connection

router = APIRouter()

daftar: List[str] = []

def get_random_string(length):
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    # print("Random string of length", length, "is:", result_str)
    return result_str

def add_daftar():
    str = get_random_string(8)
    daftar.append(str)

@router.get("/", summary="Test")
async def test_daftar():
    add_daftar()
    return daftar


@router.get("/mongo", summary="Test mongo")
async def test_mongo():
    coll = get_collection("users")
    cs = coll.find({})
    rs: List[Any] = []
    async for row in cs:
        copy = row
        copy["_id"] = str(row["_id"])
        rs.append(copy)

    return rs