from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from database import get_db_session
from schemas import (
    Product, ProductCreate,
    Order, OrderCreate,
    OrderItem, OrderItemCreate,
    ProductCategory, ProductCategoryCreate,
    User, UserCreate
)
import crud

router = APIRouter()

# Product Category endpoints
@router.get("/categories", response_model=List[ProductCategory])
async def get_categories(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session)
):
    """Get list of product categories."""
    return await crud.get_categories(db, skip=skip, limit=limit)

@router.post("/categories", response_model=ProductCategory)
async def create_category(
    category: ProductCategoryCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new product category."""
    return await crud.create_category(db, category)

@router.get("/categories/{category_id}", response_model=ProductCategory)
async def get_category(
    category_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific product category by ID."""
    category = await crud.get_category(db, category_id)
    if category is None:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

# Product endpoints
@router.get("/products", response_model=List[Product])
async def get_products(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session)
):
    """Get list of products."""
    return await crud.get_products(db, skip=skip, limit=limit)

@router.post("/products", response_model=Product)
async def create_product(
    product: ProductCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new product."""
    return await crud.create_product(db, product)

@router.get("/products/{product_id}", response_model=Product)
async def get_product(
    product_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific product by ID."""
    product = await crud.get_product(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

# Order endpoints
@router.get("/orders", response_model=List[Order])
async def get_orders(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session)
):
    """Get list of orders."""
    return await crud.get_orders(db, skip=skip, limit=limit)

@router.post("/orders", response_model=Order)
async def create_order(
    order: OrderCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new order."""
    return await crud.create_order(db, order)

@router.get("/orders/{order_id}", response_model=Order)
async def get_order(
    order_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific order by ID."""
    order = await crud.get_order(db, order_id)
    if order is None:
        raise HTTPException(status_code=404, detail="Order not found")
    return order

# Order Item endpoints
@router.post("/orders/{order_id}/items", response_model=OrderItem)
async def create_order_item(
    order_id: int,
    item: OrderItemCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Add an item to an order."""
    return await crud.create_order_item(db, order_id, item)

# User endpoints
@router.get("/users", response_model=List[User])
async def get_users(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session)
):
    """Get list of users."""
    return await crud.get_users(db, skip=skip, limit=limit)

@router.get("/users/{user_id}", response_model=User)
async def get_user(
    user_id: int,
    db: AsyncSession = Depends(get_db_session)
):
    """Get a specific user by ID."""
    user = await crud.get_user(db, user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.get("/users/{user_id}/orders", response_model=List[Order])
async def get_user_orders(
    user_id: int,
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db_session)
):
    """Get orders for a specific user."""
    return await crud.get_user_orders(db, user_id, skip=skip, limit=limit)

@router.post("/users", response_model=User)
async def create_user(
    user: UserCreate,
    db: AsyncSession = Depends(get_db_session)
):
    """Create a new user."""
    return await crud.create_user(db, user)
