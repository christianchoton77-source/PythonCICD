from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator


class ProductCreate(BaseModel):
    sku: str = Field(min_length=3, max_length=30)
    name: str = Field(min_length=3, max_length=120)
    price: Decimal = Field(gt=0, decimal_places=2)
    stock: int = Field(default=0, ge=0)

    @field_validator("sku")
    @classmethod
    def normalize_sku(cls, value: str) -> str:
        return value.strip().upper()

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        return value.strip()


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=3, max_length=120)
    price: Decimal | None = Field(default=None, gt=0, decimal_places=2)
    stock: int | None = Field(default=None, ge=0)


class ProductResponse(ProductCreate):
    id: int
    active: bool
    model_config = ConfigDict(from_attributes=True)
