from contextlib import asynccontextmanager
from sqlmodel import SQLModel, create_engine, Session, select
from fastapi import FastAPI

# Create the database engine
# connctionstring = str(settings.DATABASE_URL)

# engine = create_engine(connctionstring, pool_recycle=300, connect_args={"sslmode": "require"}) 

sqlite_file_name = "database.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)

# Create the tables
def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database connection")
    create_db_and_tables()
    yield

def db_session():
    with Session(engine) as session:
        yield session