from uuid import UUID, uuid4
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import select, Session
from typing import List, Annotated, Optional
from ecom.utils.settings import REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.context import CryptContext
from datetime import timedelta
from ecom.utils.services import get_user_by_username, verify_password, create_access_token
from ecom.utils.models import Cart, CartCreate, OrderCreate, OrderDelete, OrderUpdate, Product, Token, Order, User, UserCreate, Userlogin
from ecom.utils.db import lifespan, db_session
from ecom.utils.openai import create_thread, get_response, user_chat
from ecom.utils.crud import cancel_order, update_order, create_order, create_product_cart, delete_cart_product, get_current_user, update_cart, user_cart, signup_user

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/login")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI(title="E-commerce API", version="0.1.0", lifespan=lifespan, docs_url="/api/docs")

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/api/products", response_model=Product)
def create_product(session: Annotated[Session, Depends(db_session)]):
    product1 = Product(sku = uuid4(), name="SLOGAN PRINT T-SHIRT", description="T-shirt with a round neckline and short sleeves. Featuring a contrast print on the front.", price="19.95", slug="slogan-print-t-shirt", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/nszsjbvofpqzksa0znq0.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/wuolmer0l19he3nun9dg.jpg")
    product2 = Product(sku = uuid4(), name="THE NOTORIOUS B.I.G. © BROOKLYN MINT T-SHIRT", description="T-shirt with a round neckline and short sleeves. Notorious B.I.G. © Brooklyn Mint, LLC contrast graphics on the front and back.", price="22.95", slug="the-notorious-b-i-g-brooklyn-mint-t-shirt", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/qnfmv6awxtriizs6t4fu.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/szswckzcbpmrh4qv63uk.jpg")
    product3 = Product(sku = uuid4(), name="SWEATER WITH TOPSTITCHING AND BAND DETAIL", description="Sweater made of spun cotton. Featuring a round neckline, long sleeves, contrast topstitching and ribbed trims.", price="35.95", slug="sweater-with-topstitching-and-band-detail", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/dmpxgeljvfpbw2hvwda2.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/f3avbcfwd42av1ogajhi.jpg")
    product4 = Product(sku = uuid4(), name="ACID WASH T-SHIRT WITH SLOGAN", description="Loose-fitting T-shirt with a round neck and short sleeves. Contrast slogan print on the front.", price="19.95", slug="acid-wash-t-shirt-with-slogan", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/s17qsbgw9hucem73pahg.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/idul25gtw1r2ivuz8jm6.jpg")
    product5 = Product(sku = uuid4(), name="SLOGAN PRINT T-SHIRT", description="Round neck T-shirt with short sleeves. Contrast patch detail on the front. Contrast prints on the front and back.", price="19.95", slug="slogan-print-t-shirt", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/m9sccjomzswl2osip0r1.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/y6cxbsooaqjcexszzuak.jpg")
    product6 = Product(sku = uuid4(), name="SLIM FIT JEANS", description="Slim fit jeans. Five pockets. Faded effect. Front zip fly and button fastening.", price="39.95", slug="slim-fit-jeans", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/scbx31b7ld0dsane7bm6.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/mlgz0ll6ellb3u1yedhb.jpg")
    product7 = Product(sku = uuid4(), name="BAGGY FIT JEANS", description="Baggy fit jeans. Five pockets. Faded effect. Front zip fly and button fastening.", price="29.95", slug="baggy-fit-jeans", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/t6umhkc6ttwe5xvngsih.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/jojqrxbw0olgkhkpypra.jpg")
    product8 = Product(sku = uuid4(), name="RIPPED BAGGY JEANS", description="Baggy fit jeans. Five pockets. Faded effect. Front zip fly and button fastening.", price="39.95", slug="rippled-baggy-jeans", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/m02qurxobydlxboudvhu.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/mo15mywcd3pprb9rsxvf.jpg")
    product9 = Product(sku = uuid4(), name="STRAIGHT FIT JEANS", description="Straight fit jeans with five pockets. Faded effect. Front zip fastening.", price="29.95", slug="straight-fit-jeans", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/nmgycnwwxzsuav7v6x7y.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/p2noahmhaogfipkyrcmp.jpg")
    product10 = Product(sku = uuid4(), name="SMART SLIM FIT JEANS", description="Slim fit jeans. Five pockets. Faded effect. Front zip fly and button fastening.", price="25.95", slug="smart-slim-fit-jeans", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/qenmfhryv2yaqdep35t8.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/w0nlhjq75njtio7bfole.jpg")
    product11 = Product(sku = uuid4(), name="CONTRAST PRINT SWEATSHIRT", description="Loose-fitting sweatshirt with a round neckline and long sleeves. Contrast prints on the front and back. Ribbed trims.", price="29.95", slug="contrast-print-sweatshirt", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/tubse7bu65igtamvwrqb.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/j1tqeaor7l56x0jhwovs.jpg")
    product12 = Product(sku = uuid4(), name="REGULAR FIT JEANS", description="Regular-fit jeans made of unwashed denim. This gives the garment a rigid appearance when first worn, which will fade over time with use.", price="49.95", slug="regular-fit-jeans", image1="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/jlxdjhdayokcitpawzkm.jpg", image2="https://res.cloudinary.com/dckjqf2cq/image/upload/f_auto,c_limit,w_384,q_auto/ryjzrr9t9clmtbfshq9s.jpg")
    products = [product1, product2, product3, product4, product5, product6, product7, product8, product9, product10, product11, product12]
    session.add_all(products)
    session.commit()
    return {"message": "Products created"}

@app.post("/api/login", response_model=Token)
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: Annotated[Session, Depends(db_session)]) -> Token:
    user: Userlogin = get_user_by_username(db, form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    refresh_token_expires = timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTES)
    refresh_token = create_access_token(
        data={"sub": user.username}, expires_delta=refresh_token_expires
    )
    return {"access_token": access_token, "refresh_token": refresh_token, "expires_in": access_token_expires+refresh_token_expires, "token_type": "bearer"}

@app.post("/api/signup", response_model=User)
async def signup(db: Annotated[Session, Depends(db_session)], user: UserCreate ):
    try:
        return signup_user(user, db)
    except Exception as e:
        raise HTTPException(status_code=400,detail=str(e))

@app.get("/api/users/me", response_model=User)
async def read_users_me(token: Annotated[str, Depends(oauth2_scheme)], db: Annotated[Session, Depends(db_session)]) -> User:
    user = await get_current_user(token, db)
    return user

@app.get("/api/products", response_model=List[Product])
def get_products(session: Annotated[Session, Depends(db_session)], query: Optional[str] = None) -> List[Product]:
    if query:
        products = session.exec(select(Product).where(Product.slug.contains(query))).all()
    else:
        products = session.exec(select(Product)).all()
    return products

@app.get("/api/products/{product_slug}", response_model=Product)
def get_product(product_slug: str, session: Annotated[Session, Depends(db_session)]) -> Product:
    product = session.exec(select(Product).filter(Product.slug == product_slug)).first()
    return product

@app.get("/api/product", response_model=Product)
def get_product_by_id(product_id: UUID, session: Annotated[Session, Depends(db_session)]) -> Product:
    product = session.exec(select(Product).where(Product.sku == product_id)).first()
    return product

@app.get("/api/cart", response_model=List[Cart])
def get_cart(session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]) -> List[Cart]:
    cart = user_cart(session, user)
    return cart

@app.post("/api/cart", response_model=Cart)
def post_cart(cart: CartCreate, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]) -> Cart:
    cart = create_product_cart(session, cart, user)
    return cart

@app.patch("/api/cart", response_model=Cart)
def patch_cart(cart: CartCreate, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]) -> Cart:
    updated_cart = update_cart(session, cart, user)
    return updated_cart

@app.delete("/api/cart", response_model=dict[str, str])
def delete_cart(cart: CartCreate, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]) -> dict[str, str]:
    delete_cart_product(session, cart, user)
    return {"message": "Product removed from cart"}

@app.post("/api/order", response_model=Order)
def post_order(order: OrderCreate, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]) -> Order:
    new_order = create_order(session, order, user)
    return new_order

@app.get("/api/orders", response_model=List[Order])
def get_orders(user: Annotated[User, Depends(get_current_user)],session: Annotated[Session, Depends(db_session)]):
    orders = session.exec(select(Order).where(Order.user_id == user.id)).all()
    return orders

# @app.post("/api/openai")
# def openai(prompt: str) -> dict:
#     messages = generate_message(prompt)
#     return {"message": messages}

@app.delete("/api/order", response_model=dict[str, str])
def cancel_order(order: OrderDelete, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]) -> dict[str, str]:
    cancel_order(session, order, user)
    return {"message": "Order cancelled"}

@app.patch("/api/order", response_model=Order)
def update_order(order: OrderUpdate, session: Annotated[Session, Depends(db_session)], user: Annotated[User, Depends(get_current_user)]) -> Order:
    updated_order = update_order(session, order, user)
    return updated_order

@app.post("/api/openai/start")
def start_a_conversation():
    thread = create_thread()
    return thread

# @app.post("/api/openai/messages")
# async def message(prompt: str, thread_id: str) -> dict:
#     response = await generate_message(prompt, thread_id)
#     return {"message": response}

@app.post("/api/messages")
async def message(prompt: str, thread_id: str):
    response = await user_chat(thread_id, prompt)
    return response

@app.get("/api/openai/getmessages")
def messages(thread_id: str):
    messages = get_response(thread_id)
    return {"messages": messages}