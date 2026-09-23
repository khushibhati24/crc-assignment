from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from sqlmodel import Session, select

from database import create_db_and_tables, get_session
from models import Item, ItemCreate, ItemStatus, ItemUpdate


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="College Lost & Found API",
    description="A beginner-friendly REST API for reporting and managing lost and found items on campus.",
    version="1.0.0",
    lifespan=lifespan,
)

SessionDependency = Annotated[Session, Depends(get_session)]


@app.post(
    "/items",
    response_model=Item,
    status_code=status.HTTP_201_CREATED,
    summary="Create an item report",
)
def create_item(item: ItemCreate, session: SessionDependency):
    new_item = Item.model_validate(item)
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item


@app.get("/items", response_model=list[Item], summary="List all item reports")
def read_items(session: SessionDependency):
    return session.exec(select(Item)).all()


@app.get("/items/status/{item_status}", response_model=list[Item], summary="Filter items by status")
def read_items_by_status(item_status: ItemStatus, session: SessionDependency):
    return session.exec(select(Item).where(Item.status == item_status)).all()


@app.get("/items/category/{category}", response_model=list[Item], summary="Filter items by category")
def read_items_by_category(category: str, session: SessionDependency):
    return session.exec(select(Item).where(Item.category == category)).all()


@app.get("/items/{item_id}", response_model=Item, summary="Get one item report")
def read_item(item_id: int, session: SessionDependency):
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item


@app.put("/items/{item_id}", response_model=Item, summary="Update an item report")
def update_item(item_id: int, item_update: ItemUpdate, session: SessionDependency):
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    update_data = item_update.model_dump(exclude_unset=True)
    if not update_data:
        raise HTTPException(status_code=400, detail="At least one field is required for an update")

    for field_name, value in update_data.items():
        setattr(item, field_name, value)

    session.add(item)
    session.commit()
    session.refresh(item)
    return item


@app.delete("/items/{item_id}", summary="Delete an item report")
def delete_item(item_id: int, session: SessionDependency):
    item = session.get(Item, item_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    session.delete(item)
    session.commit()
    return {"message": "Item deleted successfully"}
