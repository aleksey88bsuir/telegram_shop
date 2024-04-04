from sqlalchemy import Column, String, Boolean, Integer
from data_base.dbcore import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String, index=True)
    is_active = Column(Boolean)

    def __repr__(self):
        return self.name
