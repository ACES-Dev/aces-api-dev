import re
from datetime import datetime, timedelta
from typing import Any, List, Optional
from pydantic import BaseConfig, BaseModel, EmailStr, Schema, validator
from bson.objectid import ObjectId
from core.config import (
    CLIENT_CODE_ERROR_MESSAGE,
    CLIENT_CODE_MAX_LENGTH,
    CLIENT_CODE_MIN_LENGTH,
    LICENSE_CODE_ERROR_MESSAGE,
    LICENSE_CODE_MAX_LENGTH,
    LICENSE_CODE_MIN_LENGTH,
)


class RWModel(BaseModel):
    class Config(BaseConfig):
        allow_population_by_alias = True
        json_encoders = {
            datetime: lambda dt: dt.replace(tzinfo=timezone.utc)
            .isoformat()
            .replace("+00:00", "Z")
        }


class DBModel(RWModel):
    oid: Optional[Any] = Schema(..., alias="_id")
    @validator("oid")
    @classmethod
    def validate_id(cls, v):
        return str(v)


class WithSlug(BaseModel):
    slug: str


class WithLicense(BaseModel):
    license: str
    @validator("license")
    @classmethod
    def validate_license(cls, v):
        v = v.strip().lower()
        if not (LICENSE_CODE_MIN_LENGTH <= len(v) <= LICENSE_CODE_MAX_LENGTH and v.isalnum()):
            raise ValueError(LICENSE_CODE_ERROR_MESSAGE)
        return v


class WithClient(BaseModel):
    client: str
    @validator("client")
    @classmethod
    def validate_client(cls, v):
        if not (CLIENT_CODE_MIN_LENGTH <= len(v) <= CLIENT_CODE_MAX_LENGTH and v.isalpha()):
            raise ValueError(CLIENT_CODE_ERROR_MESSAGE)
        return v.upper()


class WithProject(BaseModel):
    project: str
    @validator("project")
    @classmethod
    def validate_project(cls, v):
        # lowercase
        if not re.match('^[a-z0-9\-]+$', v):
            raise ValueError('Project code format error')
        return str(v)


