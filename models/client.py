from typing import List, Optional
from pydantic import BaseModel, EmailStr, validator

from models.base import DBModel, WithLicense, WithSlug

'''
## Client
- name
- description
- address
- phones[]
- fax
- website
- contacts[] (SimpleContact)'''

class Contact(BaseModel):
    name: str
    phone: str = None
    email: EmailStr = None
    messenger: str = None


class ClientInfo(BaseModel):
    name: str = None
    address: str = None
    phones: List[str] = []
    fax: str = None
    website: str = None
    contacts: List[Contact] = []


class ClientBase(ClientInfo):
    pass


class ClientCreate(ClientBase, WithLicense):
    name: str


class ClientUpdate(ClientBase):
    phones: List[str] = None
    contacts: List[Contact] = None


class Client(ClientBase, WithLicense, DBModel):
    pass
