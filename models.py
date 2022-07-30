from database import Base
from sqlalchemy import ForeignKey, Column, Boolean, String, Integer, Text
import factory
import factory.fuzzy
from database import SessionLocal


class Item(Base):
    __tablename__ = 'items'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    description = Column(Text, nullable=False)
    price = Column(Integer, nullable=False)
    on_offer = Column(Boolean, default=False)

    def __repr__(self):
        return f"<Item name={self.name} price={self.price} description = {self.description} offer = {self.on_offer}>"


class ItemFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Item
        sqlalchemy_session = SessionLocal()

    id = factory.Sequence(lambda n: n)
    name = factory.Faker('name')
    description = factory.Faker('sentence')
    price = factory.fuzzy.FuzzyInteger(0, 10)
    on_offer = factory.fuzzy.FuzzyChoice(choices=[True, False])
