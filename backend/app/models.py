from sqlalchemy import Column, Integer, String, Float, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from.database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    category = Column(String, index=True)
    thickness = Column(String)
    price = Column(Float, default=0)
    stock = Column(Integer, default=0)
    image_url = Column(String, nullable=True)
    keunggulan = Column(Text, nullable=True)
    description = Column(String, nullable=True)

class Po(Base):
    __tablename__ = "pos"
    id = Column(Integer, primary_key=True, index=True)
    store_name = Column(String, index=True)
    sales_name = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    total = Column(Float, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)
    items = relationship("PoItem", back_populates="po", cascade="all, delete-orphan")

class PoItem(Base):
    __tablename__ = "po_items"
    id = Column(Integer, primary_key=True, index=True)
    po_id = Column(Integer, ForeignKey("pos.id"))
    product_id = Column(Integer)
    product_name = Column(String)
    price = Column(Float)
    qty = Column(Integer)
    subtotal = Column(Float)
    po = relationship("Po", back_populates="items")
