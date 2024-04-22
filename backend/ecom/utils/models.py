from sqlmodel import SQLModel, Field, Column, Enum
import enum
from typing import List, Optional
from uuid import UUID
from datetime import datetime, timedelta

class ProductBase(SQLModel):
    name: str = Field(nullable=False)
    description: str 
    price: float 
    slug: str 
    image1: str 
    image2: str 

# Define the SQLModel
class Product(ProductBase, table=True):
    sku: UUID = Field(index=True, primary_key=True)

class ProductCreate(ProductBase):
    pass

class TokenData(SQLModel):
    username: str

class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int

class UserBase(SQLModel):
    username: str = Field(nullable=False)
    password: str = Field(nullable=False)

class Userlogin(UserBase):
    pass

class UserUpdate(SQLModel):
    username: str

class User(UserBase, table=True):
    id: Optional[UUID] = Field(primary_key=True, index=True)
    email: str = Field(index=True, unique=True, nullable=False)

class UserCreate(UserBase):
    email: str

class ProductSize(str, enum.Enum):
    S = "S"
    M = "M"
    L = "L"
    XL = "XL"

class CartBase(SQLModel):
    product_id: UUID = Field(default=None, foreign_key="product.sku")
    product_size: ProductSize = Field(default=ProductSize.M, sa_column=Column("product_size", Enum(ProductSize)))
    quantity: int

class Cart(CartBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    user_id: UUID = Field(default=None, foreign_key="user.id")
    product_total: float

class CartCreate(CartBase):
    pass

class CartUpdate(CartBase):
    pass

class CartDelete(CartBase):
    pass

class Token(SQLModel):
    access_token: str
    token_type: str
    expires_in: int | timedelta
    refresh_token: str

class TokenData(SQLModel):
    username: str | None = None

class OrderStatus(str, enum.Enum):
    pending = "pending"
    confirmed = "confirmed"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"

class PaymentMethod(str, enum.Enum):
    card = "card"
    cash = "cash"

class OrderBase(SQLModel):
    payment_method: PaymentMethod = Field(default=PaymentMethod.cash,sa_column=Column("payment_method", Enum(PaymentMethod)))
    first_name: str
    last_name: str
    address: str
    city: str
    state: str
    contact_number: str

class Order(OrderBase, table=True):
    id: Optional[int] = Field(primary_key=True)
    order_date: datetime = Field(default=datetime.now())
    user_id: UUID = Field(default=None, foreign_key="user.id")
    order_total: float
    order_status: OrderStatus = Field(default=OrderStatus.pending, sa_column=Column("order_status", Enum(OrderStatus)))

class OrderCreate(OrderBase):
    pass

class OrderUpdate(OrderBase):
    order_id: int
    order_status: OrderStatus

class OrderDelete(SQLModel):
    order_id: int
    order_status: OrderStatus

class RequiredAction(str, enum.Enum):
    completed = "completed"
    pending = "pending"
    failed = "failed"
    requires_action = "requires_action"
    cancelled = "cancelled"
    expired = "expired"

class RunStatus(SQLModel):
    run_id: str
    thread_id: str
    status: str
    required_action: Optional[RequiredAction]

class ThreadMessage(SQLModel):
    content: str
    role: str
    hidden: bool
    id: str
    created_at: int


class Thread(SQLModel):
    messages: List[ThreadMessage]


class CreateMessage(SQLModel):
    content: str