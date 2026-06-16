from app.database import SessionLocal, engine
from app import models

# bikin tabel dulu kalau belum ada
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()
# hapus data lama, aman karena tabel sudah pasti ada
db.query(models.Product).delete()

products = [
  {"name":"Kanal DT 0.75", "price":0, "stock":0, "description":"Coating AZ100 anti karat, baja full 0.75mm, batang lurus tidak melintir"},
  {"name":"Kanal DT 0.70", "price":0, "stock":0, "description":"Toleransi tebal minim, sambungan presisi, alternatif hemat dari 0.75"},
  {"name":"Kanal DT 0.60", "price":0, "stock":0, "description":"Ekonomis untuk partisi/kanopi ringan, tetap lurus SNI"},
  {"name":"Spandek ALS 0.25", "price":0, "stock":0, "description":"Warna ALS stabil, gelombang rapi, tidak bocor di overlap"},
  {"name":"Spandek ALS 0.30", "price":0, "stock":0, "description":"Kaku, tidak berisik saat hujan, coating AZ100"},
  {"name":"Spandek Pasir 0.25", "price":0, "stock":0, "description":"Redam panas dan suara, anti silau, tampilan premium"},
  {"name":"Spandek Pasir 0.30", "price":0, "stock":0, "description":"Pasir rekat kuat tidak rontok, lebih adem 3-5°C"},
  {"name":"Spandek Merah Putih 0.30", "price":0, "stock":0, "description":"Warna doff tidak pudar, cocok branding toko/proyek"},
  {"name":"Reng DT 0.40", "price":0, "stock":0, "description":"Kaku tidak melendut, lubang sekrup presisi, anti karat"},
  {"name":"Reng DT 0.45", "price":0, "stock":0, "description":"Paling kaku di kelasnya, cocok genteng beton/keramik"},
]

for p in products:
    db.add(models.Product(**p))
db.commit()
print("10 produk DT masuk")
