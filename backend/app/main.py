from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from. import models
from.database import engine, get_db
models.Base.metadata.create_all(bind=engine)
app = FastAPI(title="Katalog DT Sales")

class ProductCreate(BaseModel):
    name: str; category: str; thickness: str
    price: float = 0; stock: int = 0
    image_url: str | None = None
    keunggulan: str | None = None
    description: str | None = None

@app.get("/products")
def list_products(db: Session = Depends(get_db)):
    return db.query(models.Product).all()
@app.post("/products")
def create_product(p: ProductCreate, db: Session = Depends(get_db)):
    obj = models.Product(**p.model_dump()); db.add(obj); db.commit(); db.refresh(obj); return obj

class PoItemCreate(BaseModel):
    product_id: int; product_name: str; price: float; qty: int
class PoCreate(BaseModel):
    store_name: str; sales_name: str | None = None; notes: str | None = None; items: List[PoItemCreate]

@app.post("/po")
def create_po(p: PoCreate, db: Session = Depends(get_db)):
    if not p.items: raise HTTPException(400, "items kosong")
    po = models.Po(store_name=p.store_name, sales_name=p.sales_name, notes=p.notes, total=0)
    db.add(po); db.flush(); total=0
    for it in p.items:
        subtotal = it.price * it.qty; total += subtotal
        db.add(models.PoItem(po_id=po.id, product_id=it.product_id, product_name=it.product_name, price=it.price, qty=it.qty, subtotal=subtotal))
    po.total = total; db.commit(); db.refresh(po)
    return db.query(models.Po).filter(models.Po.id == po.id).first()

@app.get("/po")
def list_pos(db: Session = Depends(get_db)):
    return db.query(models.Po).order_by(models.Po.id.desc()).all()
@app.get("/po/{po_id}")
def get_po(po_id: int, db: Session = Depends(get_db)):
    po = db.query(models.Po).filter(models.Po.id == po_id).first()
    if not po: raise HTTPException(404, "PO tidak ketemu")
    return po
