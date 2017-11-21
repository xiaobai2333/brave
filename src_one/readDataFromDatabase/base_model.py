from sqlalchemy import Column, Integer, DateTime, func, event
from sqlalchemy.ext.declarative import declarative_base, AbstractConcreteBase


Model = declarative_base()


class BaseModel(Model, AbstractConcreteBase):
    id = Column(Integer, primary_key=True)


class BaseMemoryModel(BaseModel, AbstractConcreteBase):
    __table_args__ = {'mysql_engine': 'Memory'}
