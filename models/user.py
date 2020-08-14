from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator
from core.config import (
    PASSWORD_ERROR_MESSAGE,
    PASSWORD_MAX_LENGTH,
    PASSWORD_MIN_LENGTH,
    USERNAME_ERROR_MESSAGE,
    USERNAME_MAX_LENGTH,
    USERNAME_MIN_LENGTH,
)
from models.base import DBModel, WithLicense

class UserInfo(BaseModel):
    name: str
    username: str
    email: EmailStr
    licenseContact: bool = False
    verified: bool = False
    disabled: bool = False
    gender: str = None
    phone: str = None
    userRoles: List[str] = []

    @validator('username')
    def check_username(cls, v):
        v = v.strip()
        if not (USERNAME_MIN_LENGTH <= len(v) <= USERNAME_MAX_LENGTH):
            raise ValueError(USERNAME_ERROR_MESSAGE)
        return v


class UserBase(UserInfo, WithLicense):
    pass


class User(UserBase, DBModel):
    pass


class UserCreate(UserBase):
    password: str
    @validator('password')
    def check_password(cls, v):
        v = v.strip()
        if not (PASSWORD_MIN_LENGTH <= len(v) <= PASSWORD_MAX_LENGTH):
            raise ValueError(PASSWORD_ERROR_MESSAGE)
        return v


class UserInDB(UserBase):
    hashed_password: str


class UserUpdate(BaseModel):
    # All fields must be None or Optional
    name: str = None
    licenseContact: bool = None
    disabled: bool = None
    gender: str = None
    phone: str = None
    userRoles: List[str] = None


class UserInfoUpdate(BaseModel):
    # All fields must be None or Optional
    name: str = None
    # licenseContact: bool = None
    disabled: bool = None
    gender: str = None
    phone: str = None
    userRoles: List[str] = None
