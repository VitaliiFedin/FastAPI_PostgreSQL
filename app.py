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


@app.get('/item/{item_id}')
def get_item(item_id: int):
    pass


@app.post('/item-create/', response_model=ItemSerializer, status_code=status.HTTP_201_CREATED)
def create_item(item: ItemSerializer):
    new_item = Item(
        name=item.name,
        description=item.description,
        price=item.price,
        on_offer=item.on_offer

    )
    db_item = db.query(Item).filter(item.name == new_item.name).first()

    if db_item is not None:
        raise HTTPException(status_code=400, detail='Item already exists')
    db.add(new_item)
    db.commit()

    return new_item


@app.delete('item-delete/{item_id}')
def delete_item(item_id: int):
    pass


@app.put('item-update/{item_id}')
def update_item(item_id):
    pass
