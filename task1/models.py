from enum import Enum
from typing import Optional

from sqlmodel import Field, SQLModel
from pydantic import field_validator


class ItemStatus(str, Enum):
    LOST = "Lost"
    FOUND = "Found"
    RETURNED = "Returned"


def non_blank(value: str, field_name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must not be empty or whitespace-only")
    return value.strip()


class ItemBase(SQLModel):
    title: str
    description: str
    category: str
    location: str
    reported_by: str
    status: ItemStatus

    @field_validator("title", "description", "category", "location", "reported_by")
    @classmethod
    def validate_text(cls, value: str, info):
        return non_blank(value, info.field_name)


class Item(ItemBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)


class ItemCreate(ItemBase):
    pass


class ItemUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    location: Optional[str] = None
    reported_by: Optional[str] = None
    status: Optional[ItemStatus] = None

    @field_validator("title", "description", "category", "location", "reported_by")
    @classmethod
    def validate_optional_text(cls, value: Optional[str], info):
        if value is None:
            return value
        return non_blank(value, info.field_name)
