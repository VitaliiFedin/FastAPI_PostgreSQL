from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
from database import SessionLocal
from typing import Optional, List
from models import Item

app = FastAPI()


# serializer
class ItemSerializer(BaseModel):
    id: int
    name: str
    description: str
    price: int
    on_offer: bool

    class Config:
        orm_mode = True


db = SessionLocal()


@app.get('/items', response_model=List[ItemSerializer], status_code=200)
def get_all():
    items = db.query(Item).all()
    return items


@app.get('/item/{item_id}', response_model=ItemSerializer, status_code=status.HTTP_200_OK)
def get_item(item_id: int):
    item = db.query(Item).filter(Item.id == item_id).first()
    return item


@app.post('/item-create/', response_model=ItemSerializer, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemSerializer):
    new_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        on_offer=item.on_offer

    )
    db_item = db.query(Item).filter(Item.name == item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400, detail='Item already exists')
    db.add(new_item)
    db.commit()

    return new_item


@app.delete('/item-delete/{item_id}')
def delete_item(item_id: int):
    item_to_delete = db.query(Item).filter(Item.id == item_id).first()

    if item_to_delete is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Resource not found')

    db.delete(item_to_delete)
    db.commit()

    return item_to_delete


@app.put('/item-update/{item_id}', response_model=ItemSerializer, status_code=status.HTTP_200_OK)
def update_item(item_id: int, item: ItemSerializer):
    item_to_update = db.query(Item).filter(Item.id == item_id).first()
    item_to_update.name = item.name
    item_to_update.description = item.description
    item_to_update.price = item.price
    item_to_update.on_offer = item.on_offer

    db.commit()

    return item_to_update
