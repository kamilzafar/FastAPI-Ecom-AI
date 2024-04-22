from uuid import uuid4
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from ecom.utils.settings import ALGORITHM, SECRET_KEY
from ecom.utils.models import TokenData, User, UserCreate, Product, Cart, CartUpdate, CartDelete, Order, OrderCreate, OrderUpdate, OrderDelete, UserUpdate
from typing import List, Annotated
from jose import JWTError, jwt
from ecom.utils.db import db_session
from ecom.utils.services import get_user_by_username, oauth2_scheme, get_password_hash

ALGORITHM = str(ALGORITHM)
SECRET_KEY = str(SECRET_KEY)

def signup_user(user: UserCreate, db: Session) -> User:
    """
    Create a new user.
    Args:
        user (UserCreate): The user data.
        db (Session): The database session.
    Returns:
        User: The user object.
    """
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
    """
    Get the current user.
    Args:
        token (str): The access token.
        db (Session): The database session.
    Returns:
        User: The user object.
    """
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
    """
    Get the cart of the user.
    Args:
        db (Session): The database session.
        user (User): The user object.
    Returns:
        list[Cart]: The cart of the user.
        """
    user = db.exec(select(User).where(User.username == user.username)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    cart = db.exec(select(Cart).where(Cart.user_id == user.id)).all()
    return cart

def update_cart(db: Session, cart: CartUpdate, user: User) -> Cart:
    """
    Update the cart.
    Args:
        db (Session): The database session.
        cart (CartUpdate): The cart data.
        user (User): The user object.
    Returns:
        Cart: The updated cart.
    """
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
    """
    Update the cart quantity.
    Args:
        db (Session): The database session.
        cart (CartUpdate): The cart data.
        user (User): The user object.
    Returns:
        Cart: The updated cart.
    """
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
    """
    Delete the product from the cart.
    Args:
        db (Session): The database session.
        cart (CartDelete): The cart data.
        user (User): The user object.
    Returns:
        Cart: The deleted cart.
    """
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
    """
    Add the product to the cart.
    Args:
        db (Session): The database session.
        cart (Cart): The cart data.
        user (User): The user object.
    Returns:
        Cart: The cart object.
        """
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
    """
    Create a new order.
    Args:
        db (Session): The database session.
        order (OrderCreate): The order data.
        user (User): The user object.
    Returns:
        Order: The order object.
    """
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
    """
    Update the user order.
    Args:
        db (Session): The database session.
        order (OrderUpdate): The order data.
        user (User): The user object.
    Returns:
        Order: The updated order.
        """
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
    """
    Cancel the user order.
    Args:
        db (Session): The database session.
        order (OrderDelete): The order data.
        user (User): The user object.
    Returns:
        Order: The cancelled order.
        """
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