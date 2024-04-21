from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi.security import OAuth2PasswordBearer
from ecom.utils.db import db_session
from ecom.utils.settings import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, JWT_REFRESH_SECRET_KEY
from ecom.utils.models import Cart, CartDelete, CartUpdate, Order, OrderCreate, OrderDelete, OrderUpdate, Product, TokenData, User, UserCreate
from datetime import datetime, timedelta, timezone
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from pydantic import EmailStr
from uuid import uuid4
from typing import Annotated, List, Union, Any

SECRET_KEY = str(SECRET_KEY)
ALGORITHM = str(ALGORITHM)
ACCESS_TOKEN_EXPIRE_MINUTES = ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_MINUTES = REFRESH_TOKEN_EXPIRE_MINUTES
JWT_REFRESH_SECRET_KEY = str(JWT_REFRESH_SECRET_KEY)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def get_user_by_username(db:Session,username:str) -> User:
    if username is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,headers={"WWW-Authenticate": 'Bearer'},detail={"error": "invalid_token", "error_description": "The access token expired"})

    user = db.exec(select(User).where(User.username == username)).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user

def get_user_by_id(db: Session, userid: int) -> User:
    if userid is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                             headers={"WWW-Authenticate": 'Bearer'},
                             detail={"error": "invalid_token", "error_description": "The access token expired"})
    user = db.get(User, userid)

    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    
    return user
    
def get_user_by_email(db:Session,user_email: EmailStr) -> User:
    if user_email is None:
        raise  HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,headers={"WWW-Authenticate": 'Bearer'},detail={"error": "invalid_token", "error_description": "The access token expired"})

    user = db.get(User, user_email)

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="User not found")
    return user

def authenticate_user(db, username: str, password: str) -> User:
    user = get_user_by_username(db, username)
    if not user:
        return False
    if not verify_password(password, user.password):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def create_refresh_token(data: Union[str, Any], expires_delta: int = None) -> str:
    if expires_delta is not None:
        expires_delta = datetime.now() + expires_delta
    else:
        expires_delta = datetime.now() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"exp": expires_delta, "sub": str(data)}
    encoded_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encoded_jwt

def signup_user(user: UserCreate, db: Session) -> User:
    search_user_by_email = db.exec(select(User).where(User.email == user.email)).first()
    if search_user_by_email:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Email id already registered")
    
    search_user_by_username = db.exec(select(User).where(User.username == user.username)).first()
    if search_user_by_username:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Try Different username")
    
    hashed_password = get_password_hash(user.password)

    new_user = User(id = uuid4(),username=user.username, email=user.email, password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(db_session)]) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user_by_username(db, username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

def user_cart(db: Session, user: User) -> list[Cart]:
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    cart = db.exec(select(Cart).where(Cart.user_id == user.id)).all()
    return cart

def update_cart(db: Session, cart: CartUpdate, user: User) -> Cart:
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    product = db.exec(select(Product).where(Product.sku == cart.product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    dbcart = db.exec(select(Cart).where(Cart.user_id == user.id, Cart.product_size == cart.product_size, Cart.product_id == cart.product_id)).first()
    if not dbcart:
        raise HTTPException(status_code=404, detail="Cart not found")
    dbcart.id = dbcart.id
    dbcart.user_id = user.id
    dbcart.product_id = cart.product_id
    dbcart.product_size = cart.product_size
    dbcart.quantity = cart.quantity
    dbcart.product_total = product.price * dbcart.quantity
    db.add(dbcart)
    db.commit()
    db.refresh(dbcart)
    return dbcart

def update_cart_quantity(db: Session, cart: CartUpdate, user: User) -> Cart:
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    product = db.exec(select(Product).where(Product.sku == cart.product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    dbcart = db.exec(select(Cart).where(Cart.user_id == user.id, Cart.product_size == cart.product_size, Cart.product_id == cart.product_id)).first()
    if not dbcart:
        raise HTTPException(status_code=404, detail="Cart not found")
    dbcart.id = dbcart.id
    dbcart.user_id = user.id
    dbcart.product_id = cart.product_id
    dbcart.product_size = cart.product_size
    dbcart.quantity += cart.quantity
    dbcart.product_total = product.price * dbcart.quantity
    db.add(dbcart)
    db.commit()
    db.refresh(dbcart)
    return dbcart

def delete_cart_product(db: Session, cart: CartDelete, user: User) -> Cart:
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    product = db.exec(select(Product).where(Product.sku == cart.product_id, Cart.product_size == cart.product_size)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    cart = db.exec(select(Cart).where(Cart.user_id == user.id, Cart.product_id == cart.product_id, Cart.product_size == cart.product_size)).first()
    if not cart:
        raise HTTPException(status_code=404, detail="Cart not found")
    db.delete(cart)
    db.commit()
    return cart

def create_product_cart(db: Session, cart: Cart, user: User) -> Cart:
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    product = db.exec(select(Product).where(Product.sku == cart.product_id)).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    product_in_cart = db.exec(select(Cart).where(Cart.product_id == cart.product_id, Cart.user_id == user.id, Cart.product_size == cart.product_size)).first()
    if product_in_cart:
        product = update_cart_quantity(db, cart, user)
        return product
    dbcart = Cart(product_id=cart.product_id, product_total=product.price*cart.quantity, product_size=cart.product_size, quantity=cart.quantity, user_id=user.id)
    db.add(dbcart)
    db.commit()
    db.refresh(dbcart)
    return dbcart

def create_order(db: Session, order: OrderCreate, user: User) -> Order:
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    cart: List[Cart] = user_cart(db, user)
    order_total = sum(item.product_total for item in cart)
    order = Order(user_id=user.id, payment_method=order.payment_method, order_total=order_total, first_name=order.first_name, last_name=order.last_name, address=order.address, city=order.city, state=order.state, contact_number=order.contact_number)
    db.add(order)
    for item in cart:
        db.delete(item)
        db.commit()
    db.commit()
    db.refresh(order)
    return order

def update_order(db: Session, order: OrderUpdate, user: User) -> Order:
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    order = db.exec(select(Order).where(Order.user_id == user.id, Order.id == order.order_id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.payment_method = order.payment_method
    order.first_name = order.first_name
    order.last_name = order.last_name
    order.address = order.address
    order.city = order.city
    order.state = order.state
    order.contact_number = order.contact_number
    order.order_status = order.order_status
    db.add(order)
    db.commit()
    db.refresh(order)
    return order

def cancel_order(db: Session, order: OrderDelete, user: User) -> Order:
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    order = db.exec(select(Order).where(Order.id == order.order_id, Order.user_id == user.id)).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    order.order_status = "cancelled"
    db.add(order)
    db.commit()
    db.refresh(order)
    return order