from models import ItemFactory

items = ItemFactory.create_batch(10)

for item in items:
    print(item)
