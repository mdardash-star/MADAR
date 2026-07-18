from pydantic import BaseModel, Field


class DepartmentCreateRequest(BaseModel):
    company_id: int
    branch_id: int | None = None
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    description: str | None = None
    is_active: bool = True


class DepartmentUpdateRequest(BaseModel):
    branch_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    is_active: bool | None = None


class DepartmentRead(BaseModel):
    id: int
    company_id: int
    branch_id: int | None = None
    name: str
    code: str
    description: str | None = None
    is_active: bool


class WarehouseCreateRequest(BaseModel):
    company_id: int
    branch_id: int | None = None
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    address: str | None = None
    is_active: bool = True


class WarehouseUpdateRequest(BaseModel):
    branch_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    address: str | None = None
    is_active: bool | None = None


class WarehouseRead(BaseModel):
    id: int
    company_id: int
    branch_id: int | None = None
    name: str
    code: str
    address: str | None = None
    is_active: bool


class CustomerCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool = True


class CustomerUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool | None = None


class CustomerRead(BaseModel):
    id: int
    company_id: int
    name: str
    code: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool


class SupplierCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool = True


class SupplierUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool | None = None


class SupplierRead(BaseModel):
    id: int
    company_id: int
    name: str
    code: str
    email: str | None = None
    phone: str | None = None
    address: str | None = None
    is_active: bool


class ProductCategoryCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    description: str | None = None
    is_active: bool = True


class ProductCategoryUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    is_active: bool | None = None


class ProductCategoryRead(BaseModel):
    id: int
    company_id: int
    name: str
    code: str
    description: str | None = None
    is_active: bool


class UnitOfMeasureCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    abbreviation: str | None = None
    is_active: bool = True


class UnitOfMeasureUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    abbreviation: str | None = None
    is_active: bool | None = None


class UnitOfMeasureRead(BaseModel):
    id: int
    company_id: int
    name: str
    code: str
    abbreviation: str | None = None
    is_active: bool


class TaxSettingCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    rate_percent: float = Field(ge=0)
    is_active: bool = True


class TaxSettingUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    rate_percent: float | None = Field(default=None, ge=0)
    is_active: bool | None = None


class TaxSettingRead(BaseModel):
    id: int
    company_id: int
    name: str
    code: str
    rate_percent: float
    is_active: bool


class CurrencySettingCreateRequest(BaseModel):
    company_id: int
    code: str = Field(min_length=1, max_length=10)
    name: str = Field(min_length=1, max_length=255)
    symbol: str | None = Field(default=None, max_length=10)
    exchange_rate: float = Field(ge=0)
    is_active: bool = True


class CurrencySettingUpdateRequest(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=10)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    symbol: str | None = Field(default=None, max_length=10)
    exchange_rate: float | None = Field(default=None, ge=0)
    is_active: bool | None = None


class CurrencySettingRead(BaseModel):
    id: int
    company_id: int
    code: str
    name: str
    symbol: str | None = None
    exchange_rate: float
    is_active: bool


class ProductCreateRequest(BaseModel):
    company_id: int
    category_id: int | None = None
    brand_id: int | None = None
    unit_of_measure_id: int | None = None
    name: str = Field(min_length=1, max_length=255)
    sku: str = Field(min_length=1, max_length=100)
    barcode: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=500)
    description: str | None = None
    selling_price: float = Field(ge=0)
    cost_price: float = Field(ge=0)
    is_active: bool = True


class ProductUpdateRequest(BaseModel):
    category_id: int | None = None
    brand_id: int | None = None
    unit_of_measure_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    sku: str | None = Field(default=None, min_length=1, max_length=100)
    barcode: str | None = Field(default=None, max_length=100)
    image_url: str | None = Field(default=None, max_length=500)
    description: str | None = None
    selling_price: float | None = Field(default=None, ge=0)
    cost_price: float | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductRead(BaseModel):
    id: int
    company_id: int
    category_id: int | None = None
    brand_id: int | None = None
    unit_of_measure_id: int | None = None
    name: str
    sku: str
    barcode: str | None = None
    image_url: str | None = None
    description: str | None = None
    selling_price: float
    cost_price: float
    is_active: bool


class ProductVariantCreateRequest(BaseModel):
    product_id: int
    name: str = Field(min_length=1, max_length=255)
    sku: str = Field(min_length=1, max_length=100)
    variant_price: float = Field(ge=0)
    is_active: bool = True


class ProductVariantUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    sku: str | None = Field(default=None, min_length=1, max_length=100)
    variant_price: float | None = Field(default=None, ge=0)
    is_active: bool | None = None


class ProductVariantRead(BaseModel):
    id: int
    product_id: int
    name: str
    sku: str
    variant_price: float
    is_active: bool
