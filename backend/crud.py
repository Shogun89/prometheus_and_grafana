from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
import models, schemas
from typing import List, Optional

#######################
# Product Categories
#######################

async def get_product_category(db: AsyncSession, category_id: int):
    """
    Retrieve a product category by its ID.

    Args:
        db (AsyncSession): The database session.
        category_id (int): The ID of the product category to retrieve.

    Returns:
        models.ProductCategory: The product category object if found, else None.
    """
    result = await db.execute(
        db.query(models.ProductCategory)
        .filter(models.ProductCategory.id == category_id)
    )
    return result.scalar_one_or_none()


async def get_product_categories(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of product categories.

    Args:
        db (AsyncSession): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        List[models.ProductCategory]: A list of product category objects.
    """
    result = await db.execute(
        db.query(models.ProductCategory)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_product_category(db: AsyncSession, category: schemas.ProductCategoryCreate):
    """
    Create a new product category.

    Args:
        db (AsyncSession): The database session.
        category (schemas.ProductCategoryCreate): The product category data to create.

    Returns:
        models.ProductCategory: The created product category object.
    """
    db_category = models.ProductCategory(name=category.name)
    db.add(db_category)
    await db.commit()
    await db.refresh(db_category)
    return db_category


async def update_product_category(db: AsyncSession, category_id: int, category: schemas.ProductCategoryUpdate):
    """
    Update a product category.

    Args:
        db (AsyncSession): The database session.
        category_id (int): The ID of the category to update.
        category (schemas.ProductCategoryUpdate): The updated category data.

    Returns:
        models.ProductCategory: The updated category object if found, else None.
    """
    db_category = await get_product_category(db, category_id)
    if db_category:
        for key, value in category.dict(exclude_unset=True).items():
            setattr(db_category, key, value)
        await db.commit()
        await db.refresh(db_category)
    return db_category


async def delete_product_category(db: AsyncSession, category_id: int):
    """
    Delete a product category.

    Args:
        db (AsyncSession): The database session.
        category_id (int): The ID of the category to delete.

    Returns:
        bool: True if category was deleted, False if not found.
    """
    db_category = await get_product_category(db, category_id)
    if db_category:
        await db.delete(db_category)
        await db.commit()
        return True
    return False


#######################
# Products
#######################

async def get_product(db: AsyncSession, product_id: int):
    """
    Retrieve a product by its ID.

    Args:
        db (AsyncSession): The database session.
        product_id (int): The ID of the product to retrieve.

    Returns:
        models.Product: The product object if found, else None.
    """
    result = await db.execute(
        db.query(models.Product)
        .filter(models.Product.id == product_id)
    )
    return result.scalar_one_or_none()


async def get_products(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retrieve a list of products.

    Args:
        db (AsyncSession): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        List[models.Product]: A list of product objects.
    """
    result = await db.execute(
        db.query(models.Product)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def create_product(db: AsyncSession, product: schemas.ProductCreate):
    """
    Create a new product.

    Args:
        db (AsyncSession): The database session.
        product (schemas.ProductCreate): The product data to create.

    Returns:
        models.Product: The created product object.
    """
    db_product = models.Product(**product.dict())
    db.add(db_product)
    await db.commit()
    await db.refresh(db_product)
    return db_product


async def update_product(db: AsyncSession, product_id: int, product: schemas.ProductUpdate):
    """
    Update a product.

    Args:
        db (AsyncSession): The database session.
        product_id (int): The ID of the product to update.
        product (schemas.ProductUpdate): The updated product data.

    Returns:
        models.Product: The updated product object if found, else None.
    """
    db_product = await get_product(db, product_id)
    if db_product:
        for key, value in product.dict(exclude_unset=True).items():
            setattr(db_product, key, value)
        await db.commit()
        await db.refresh(db_product)
    return db_product


async def delete_product(db: AsyncSession, product_id: int):
    """
    Delete a product.

    Args:
        db (AsyncSession): The database session.
        product_id (int): The ID of the product to delete.

    Returns:
        bool: True if product was deleted, False if not found.
    """
    db_product = await get_product(db, product_id)
    if db_product:
        await db.delete(db_product)
        await db.commit()
        return True
    return False


#######################
# Users
#######################

async def get_users(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[models.User]:
    """Get list of users with pagination."""
    result = await db.execute(
        select(models.User)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()

async def get_user(db: AsyncSession, user_id: int) -> Optional[models.User]:
    """Get a specific user by ID."""
    result = await db.execute(
        select(models.User)
        .filter(models.User.id == user_id)
    )
    return result.scalar_one_or_none()

async def create_user(db: AsyncSession, user: schemas.UserCreate) -> models.User:
    """Create a new user."""
    db_user = models.User(
        email=user.email,
        is_active=user.is_active
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

async def update_user(db: AsyncSession, user_id: int, user: schemas.UserUpdate):
    """Update user in this shard"""
    db_user = await get_user(db, user_id)
    if db_user:
        for key, value in user.dict(exclude_unset=True).items():
            setattr(db_user, key, value)
        await db.commit()
        await db.refresh(db_user)
    return db_user


async def delete_user(db: AsyncSession, user_id: int):
    """Delete user from this shard"""
    db_user = await get_user(db, user_id)
    if db_user:
        await db.delete(db_user)
        await db.commit()
        return True
    return False


#######################
# Orders
#######################

async def create_order(db: AsyncSession, order: schemas.OrderCreate, user_id: int):
    """Create a new order."""
    db_order = models.Order(
        user_id=user_id,
        status=order.status,
        total_amount=order.total_amount
    )
    db.add(db_order)
    await db.commit()
    await db.refresh(db_order)
    return db_order


async def get_order(db: AsyncSession, order_id: int):
    """Retrieve an order by its ID."""
    result = await db.execute(
        db.query(models.Order)
        .filter(models.Order.id == order_id)
    )
    return result.scalar_one_or_none()


async def get_user_orders(db: AsyncSession, user_id: int, skip: int = 0, limit: int = 100):
    """Retrieve all orders for a specific user."""
    result = await db.execute(
        db.query(models.Order)
        .filter(models.Order.user_id == user_id)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def update_order_status(db: AsyncSession, order_id: int, status: str):
    """Update the status of an order."""
    db_order = await get_order(db, order_id)
    if db_order:
        db_order.status = status
        await db.commit()
        await db.refresh(db_order)
    return db_order


async def get_orders(db: AsyncSession, skip: int = 0, limit: int = 100):
    """
    Retrieve all orders with pagination.

    Args:
        db (AsyncSession): The database session.
        skip (int, optional): Number of records to skip. Defaults to 0.
        limit (int, optional): Maximum number of records to return. Defaults to 100.

    Returns:
        List[models.Order]: A list of order objects.
    """
    result = await db.execute(
        db.query(models.Order)
        .offset(skip)
        .limit(limit)
    )
    return result.scalars().all()


async def update_order(db: AsyncSession, order_id: int, order: schemas.OrderUpdate):
    """
    Update an order.

    Args:
        db (AsyncSession): The database session.
        order_id (int): The ID of the order to update.
        order (schemas.OrderUpdate): The updated order data.

    Returns:
        models.Order: The updated order object if found, else None.
    """
    db_order = await get_order(db, order_id)
    if db_order:
        for key, value in order.dict(exclude_unset=True).items():
            setattr(db_order, key, value)
        await db.commit()
        await db.refresh(db_order)
    return db_order


async def delete_order(db: AsyncSession, order_id: int):
    """
    Delete an order.

    Args:
        db (AsyncSession): The database session.
        order_id (int): The ID of the order to delete.

    Returns:
        bool: True if order was deleted, False if not found.
    """
    db_order = await get_order(db, order_id)
    if db_order:
        await db.delete(db_order)
        await db.commit()
        return True
    return False


#######################
# Order Items
#######################

async def create_order_item(db: AsyncSession, order_item: schemas.OrderItemCreate, order_id: int):
    """Create a new order item."""
    db_order_item = models.OrderItem(
        order_id=order_id,
        product_id=order_item.product_id,
        quantity=order_item.quantity,
        price=order_item.price
    )
    db.add(db_order_item)
    await db.commit()
    await db.refresh(db_order_item)
    return db_order_item


async def get_order_items(db: AsyncSession, order_id: int):
    """Retrieve all items for a specific order."""
    result = await db.execute(
        db.query(models.OrderItem)
        .filter(models.OrderItem.order_id == order_id)
    )
    return result.scalars().all()


async def get_order_item(db: AsyncSession, order_id: int, item_id: int):
    """
    Retrieve a specific order item.

    Args:
        db (AsyncSession): The database session.
        order_id (int): The ID of the order.
        item_id (int): The ID of the order item.

    Returns:
        models.OrderItem: The order item object if found, else None.
    """
    result = await db.execute(
        db.query(models.OrderItem)
        .filter(models.OrderItem.order_id == order_id)
        .filter(models.OrderItem.id == item_id)
    )
    return result.scalar_one_or_none()


async def update_order_item(db: AsyncSession, order_id: int, item_id: int, item: schemas.OrderItemUpdate):
    """
    Update an order item.

    Args:
        db (AsyncSession): The database session.
        order_id (int): The ID of the order.
        item_id (int): The ID of the order item to update.
        item (schemas.OrderItemUpdate): The updated order item data.

    Returns:
        models.OrderItem: The updated order item object if found, else None.
    """
    db_item = await get_order_item(db, order_id, item_id)
    if db_item:
        for key, value in item.dict(exclude_unset=True).items():
            setattr(db_item, key, value)
        await db.commit()
        await db.refresh(db_item)
    return db_item


async def delete_order_item(db: AsyncSession, order_id: int, item_id: int):
    """
    Delete an order item.

    Args:
        db (AsyncSession): The database session.
        order_id (int): The ID of the order.
        item_id (int): The ID of the order item to delete.

    Returns:
        bool: True if item was deleted, False if not found.
    """
    db_item = await get_order_item(db, order_id, item_id)
    if db_item:
        await db.delete(db_item)
        await db.commit()
        return True
    return False

