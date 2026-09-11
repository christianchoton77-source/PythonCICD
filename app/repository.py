from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Product


class ProductRepository:
    def get_all(self, db: Session, minimum_stock: int | None = None) -> list[Product]:
        stmt = select(Product).order_by(Product.id)
        if minimum_stock is not None:
            stmt = stmt.where(Product.stock >= minimum_stock)
        return list(db.scalars(stmt).all())

    def get_by_id(self, db: Session, product_id: int) -> Product | None:
        return db.get(Product, product_id)

    def get_by_sku(self, db: Session, sku: str) -> Product | None:
        return db.scalar(select(Product).where(Product.sku == sku))

    def create(self, db: Session, product: Product) -> Product:
        db.add(product)
        db.commit()
        db.refresh(product)
        return product

    def update(self, db: Session, product: Product) -> Product:
        db.commit()
        db.refresh(product)
        return product
