from datetime import datetime
# from dateutil.parser import parse
from typing import Dict
from fastapi import HTTPException
from pydantic import BaseModel


def raise_not_found(message: str = "Not found"):
	raise HTTPException(
		status_code=404,
		detail=message
	)


def raise_bad_request(message: str="Bad request"):
	raise HTTPException(
		status_code=400,
		detail=message
	)


def raise_server_error(message: str="Server error"):
	raise HTTPException(
		status_code=500,
		detail=message
	)


def is_date(date_string: str):
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return True
    except ValueError:
        return False

