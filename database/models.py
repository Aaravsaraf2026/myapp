from .db.core import Base
from sqlalchemy import String, Integer, Column



class User(Base):
    __tablename__ = "users"
    id    = Column(Integer, primary_key=True, index=True)
    name  = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)

class Products(Base):
    __tablename__ = "products"
    id    = Column(Integer, primary_key=True, index=True)
    Product_name  = Column(String, nullable=False)
    product_id = Column(Integer, unique=True, nullable=False, index=True)
    price = Column(Integer,nullable=False)
