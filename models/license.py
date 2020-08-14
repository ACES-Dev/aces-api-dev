from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator

from core.config import (
    LICENSE_TYPES,
    LICENSE_CODE_MIN_LENGTH,
    LICENSE_CODE_MAX_LENGTH,
    LICENSE_CODE_ERROR_MESSAGE,
    USERNAME_ERROR_MESSAGE,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
    PASSWORD_ERROR_MESSAGE,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
)
from models.base import DBModel, WithSlug
from utils.utils import is_date


class LicenseBase(BaseModel):
    type: str
    licenseName: str
    contactName: str
    contactEmail: EmailStr
    publishedBy: str
    publishDate: str        # First published
    refreshDate: Optional[datetime]   # Refresh
    expiryDate: Optional[datetime]
    disabled: bool = False

    @validator("type")
    @classmethod
    def validate_type(cls, v):
        v = v.strip()
        if not v.lower() in LICENSE_TYPES:
            raise ValueError("Illegal license type")
        return v.lower()

    @validator("publishDate")
    @classmethod
    def validate_publishDate(cls, v):
        v = v.strip()
        if not is_date(v):
            raise ValueError("Date format error")
        return v


class LicenseCreate(LicenseBase, WithSlug):
    @validator("slug")
    @classmethod
    def validate_slug(cls, v):
        v = v.strip()
        if not (LICENSE_CODE_MIN_LENGTH <= len(v) <= LICENSE_CODE_MAX_LENGTH and v.isalnum()):
            raise ValueError(LICENSE_CODE_ERROR_MESSAGE)
        return v.lower()


class LicenseUpdate(BaseModel):
    type: str = None
    licenseName: str = None
    contactName: str = None
    contactEmail: EmailStr = None
    publishDate: str = None
    refreshDate: datetime = None
    expiryDate: datetime = None
    disabled: bool = None


class LicenseInfoUpdate(BaseModel):
    licenseName: str = None
    contactName: str = None
    contactEmail: EmailStr = None


class License(LicenseBase, WithSlug, DBModel):
    pass
