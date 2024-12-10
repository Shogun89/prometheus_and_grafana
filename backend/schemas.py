from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from models import OrderStatus  # Add this import at the top

#######################
# Product Categories
#######################

class ProductCategoryBase(BaseModel):
    """Base schema for product category with common attributes."""
    name: str

class ProductCategoryCreate(ProductCategoryBase):
    """Schema for creating a new product category. Inherits all from base."""
    pass

class ProductCategory(ProductCategoryBase):
    """Schema for complete product category data, used for responses."""
    id: int

    class Config:
        from_attributes = True

class ProductCategoryUpdate(BaseModel):
    """Schema for updating a product category. All fields are optional."""
    name: Optional[str] = None


#######################
# Products
#######################

class ProductBase(BaseModel):
    """Base schema for product with common attributes."""
    name: str
    description: Optional[str] = None
    price: float
    category_id: int

class ProductCreate(ProductBase):
    """Schema for creating a new product. Inherits all from base."""
    pass

class Product(ProductBase):
    """Schema for complete product data, used for responses."""
    id: int
    category: ProductCategory

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    """Schema for updating a product. All fields are optional."""
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    category_id: Optional[int] = None


#######################
# Order Items
#######################

class OrderItemBase(BaseModel):
    """Base schema for order items with common attributes."""
    product_id: int
    quantity: int
    price: float

class OrderItemCreate(OrderItemBase):
    """Schema for creating a new order item. Inherits all from base."""
    pass

class OrderItem(OrderItemBase):
    """Schema for complete order item data, used for responses."""
    id: int
    order_id: int
    product: Product

    class Config:
        from_attributes = True

class OrderItemUpdate(BaseModel):
    """Schema for updating an order item. All fields are optional."""
    quantity: Optional[int] = None
    price: Optional[float] = None


#######################
# Orders
#######################

class OrderBase(BaseModel):
    """Base schema for orders with common attributes."""
    total_amount: float
    status: OrderStatus  # Change from str to OrderStatus enum

class OrderCreate(OrderBase):
    """Schema for creating a new order. Inherits all from base."""
    pass

class Order(OrderBase):
    """Schema for complete order data, used for responses."""
    id: int
    user_id: int
    order_items: List[OrderItem]

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    """Schema for updating an order. All fields are optional."""
    total_amount: Optional[float] = None
    status: Optional[OrderStatus] = None  # Change from str to OrderStatus enum


#######################
# Users
#######################

class UserBase(BaseModel):
    """Base schema for users with common attributes."""
    email: str
    is_active: bool = True

class UserCreate(UserBase):
    """Schema for creating a new user. Inherits all from base."""
    password: str

class UserUpdate(BaseModel):
    """Schema for updating a user. All fields are optional."""
    email: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    """Schema for complete user data, used for responses."""
    id: int
    created_at: datetime
    last_login: Optional[datetime] = None

    class Config:
        from_attributes = True
