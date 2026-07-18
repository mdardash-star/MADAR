from pydantic import BaseModel, Field


class CostCenterCreateRequest(BaseModel):
    company_id: int
    branch_id: int | None = None
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    description: str | None = None
    is_active: bool = True


class CostCenterUpdateRequest(BaseModel):
    branch_id: int | None = None
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    is_active: bool | None = None


class CostCenterRead(BaseModel):
    id: int
    company_id: int
    branch_id: int | None = None
    name: str
    code: str
    description: str | None = None
    is_active: bool


class CustomerGroupCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    description: str | None = None
    is_active: bool = True


class CustomerGroupUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    is_active: bool | None = None


class CustomerGroupRead(BaseModel):
    id: int
    company_id: int
    name: str
    code: str
    description: str | None = None
    is_active: bool


class CustomerContactCreateRequest(BaseModel):
    company_id: int
    customer_id: int
    full_name: str = Field(min_length=1, max_length=255)
    position: str | None = None
    email: str | None = None
    phone: str | None = None
    is_primary: bool = False
    is_active: bool = True


class CustomerContactUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    position: str | None = None
    email: str | None = None
    phone: str | None = None
    is_primary: bool | None = None
    is_active: bool | None = None


class CustomerContactRead(BaseModel):
    id: int
    company_id: int
    customer_id: int
    full_name: str
    position: str | None = None
    email: str | None = None
    phone: str | None = None
    is_primary: bool
    is_active: bool


class CustomerAddressCreateRequest(BaseModel):
    company_id: int
    customer_id: int
    label: str = Field(min_length=1, max_length=100)
    street: str | None = None
    city: str | None = None
    country: str | None = None
    postal_code: str | None = None
    is_primary: bool = False
    is_active: bool = True


class CustomerAddressUpdateRequest(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=100)
    street: str | None = None
    city: str | None = None
    country: str | None = None
    postal_code: str | None = None
    is_primary: bool | None = None
    is_active: bool | None = None


class CustomerAddressRead(BaseModel):
    id: int
    company_id: int
    customer_id: int
    label: str
    street: str | None = None
    city: str | None = None
    country: str | None = None
    postal_code: str | None = None
    is_primary: bool
    is_active: bool


class SupplierContactCreateRequest(BaseModel):
    company_id: int
    supplier_id: int
    full_name: str = Field(min_length=1, max_length=255)
    position: str | None = None
    email: str | None = None
    phone: str | None = None
    is_primary: bool = False
    is_active: bool = True


class SupplierContactUpdateRequest(BaseModel):
    full_name: str | None = Field(default=None, min_length=1, max_length=255)
    position: str | None = None
    email: str | None = None
    phone: str | None = None
    is_primary: bool | None = None
    is_active: bool | None = None


class SupplierContactRead(BaseModel):
    id: int
    company_id: int
    supplier_id: int
    full_name: str
    position: str | None = None
    email: str | None = None
    phone: str | None = None
    is_primary: bool
    is_active: bool


class SupplierAddressCreateRequest(BaseModel):
    company_id: int
    supplier_id: int
    label: str = Field(min_length=1, max_length=100)
    street: str | None = None
    city: str | None = None
    country: str | None = None
    postal_code: str | None = None
    is_primary: bool = False
    is_active: bool = True


class SupplierAddressUpdateRequest(BaseModel):
    label: str | None = Field(default=None, min_length=1, max_length=100)
    street: str | None = None
    city: str | None = None
    country: str | None = None
    postal_code: str | None = None
    is_primary: bool | None = None
    is_active: bool | None = None


class SupplierAddressRead(BaseModel):
    id: int
    company_id: int
    supplier_id: int
    label: str
    street: str | None = None
    city: str | None = None
    country: str | None = None
    postal_code: str | None = None
    is_primary: bool
    is_active: bool


class BrandCreateRequest(BaseModel):
    company_id: int
    name: str = Field(min_length=1, max_length=255)
    code: str = Field(min_length=1, max_length=50)
    description: str | None = None
    is_active: bool = True


class BrandUpdateRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    code: str | None = Field(default=None, min_length=1, max_length=50)
    description: str | None = None
    is_active: bool | None = None


class BrandRead(BaseModel):
    id: int
    company_id: int
    name: str
    code: str
    description: str | None = None
    is_active: bool


class StorageLocationCreateRequest(BaseModel):
    company_id: int
    warehouse_id: int
    code: str = Field(min_length=1, max_length=50)
    name: str = Field(min_length=1, max_length=255)
    description: str | None = None
    is_active: bool = True


class StorageLocationUpdateRequest(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=50)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = None
    is_active: bool | None = None


class StorageLocationRead(BaseModel):
    id: int
    company_id: int
    warehouse_id: int
    code: str
    name: str
    description: str | None = None
    is_active: bool


class StockOpeningBalanceCreateRequest(BaseModel):
    company_id: int
    warehouse_id: int
    product_id: int
    storage_location_id: int | None = None
    quantity: float = Field(ge=0)
    unit_cost: float = Field(ge=0)
    batch_no: str | None = None


class StockOpeningBalanceUpdateRequest(BaseModel):
    warehouse_id: int | None = None
    product_id: int | None = None
    storage_location_id: int | None = None
    quantity: float | None = Field(default=None, ge=0)
    unit_cost: float | None = Field(default=None, ge=0)
    batch_no: str | None = None


class StockOpeningBalanceRead(BaseModel):
    id: int
    company_id: int
    warehouse_id: int
    product_id: int
    storage_location_id: int | None = None
    quantity: float
    unit_cost: float
    batch_no: str | None = None


class BarcodeCreateRequest(BaseModel):
    company_id: int
    product_id: int
    code: str = Field(min_length=1, max_length=100)
    barcode_type: str | None = Field(default=None, max_length=50)
    is_active: bool = True


class BarcodeUpdateRequest(BaseModel):
    code: str | None = Field(default=None, min_length=1, max_length=100)
    barcode_type: str | None = Field(default=None, max_length=50)
    is_active: bool | None = None


class BarcodeRead(BaseModel):
    id: int
    company_id: int
    product_id: int
    code: str
    barcode_type: str | None = None
    is_active: bool


class ProductImageCreateRequest(BaseModel):
    company_id: int
    product_id: int
    image_url: str = Field(min_length=1, max_length=500)
    caption: str | None = Field(default=None, max_length=255)
    is_primary: bool = False
    is_active: bool = True


class ProductImageUpdateRequest(BaseModel):
    image_url: str | None = Field(default=None, min_length=1, max_length=500)
    caption: str | None = Field(default=None, max_length=255)
    is_primary: bool | None = None
    is_active: bool | None = None


class ProductImageRead(BaseModel):
    id: int
    company_id: int
    product_id: int
    image_url: str
    caption: str | None = None
    is_primary: bool
    is_active: bool
