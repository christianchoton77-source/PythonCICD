from typing import Annotated
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.db import get_db
from app.repository import ProductRepository
from app.schemas import ProductCreate, ProductResponse, ProductUpdate
from app.security import require_role
from app.service import ProductService

router = APIRouter(prefix="/products", tags=["Products"])
Db = Annotated[Session, Depends(get_db)]
service = ProductService()
repo = ProductRepository()


@router.get("", response_model=list[ProductResponse])
def list_products(db: Db, minimum_stock: int | None = Query(default=None, ge=0)):
    return repo.get_all(db, minimum_stock)


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Db):
    return service.get_or_404(db, product_id)


@router.post("", response_model=ProductResponse, status_code=201)
def create_product(data: ProductCreate, db: Db, _admin: dict = Depends(require_role("admin"))):
    return service.create(db, data)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, data: ProductUpdate, db: Db, _admin: dict = Depends(require_role("admin"))):
    return service.update(db, product_id, data)


@router.patch("/{product_id}/deactivate", response_model=ProductResponse)
def deactivate_product(product_id: int, db: Db, _admin: dict = Depends(require_role("admin"))):
    return service.deactivate(db, product_id)
