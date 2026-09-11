from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from app.models import Product
from app.repository import ProductRepository
from app.schemas import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repo: ProductRepository | None = None):
        self.repo = repo or ProductRepository()

    def get_or_404(self, db: Session, product_id: int) -> Product:
        product = self.repo.get_by_id(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Producto no encontrado")
        return product

    def create(self, db: Session, data: ProductCreate) -> Product:
        if self.repo.get_by_sku(db, data.sku):
            raise HTTPException(status_code=409, detail="El SKU ya existe")
        product = Product(**data.model_dump(), active=True)
        try:
            return self.repo.create(db, product)
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=409, detail="El SKU ya existe")

    def update(self, db: Session, product_id: int, data: ProductUpdate) -> Product:
        product = self.get_or_404(db, product_id)
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(product, field, value)
        return self.repo.update(db, product)

    def deactivate(self, db: Session, product_id: int) -> Product:
        product = self.get_or_404(db, product_id)
        if not product.active:
            raise HTTPException(status_code=409, detail="El producto ya está inactivo")
        product.active = False
        return self.repo.update(db, product)
