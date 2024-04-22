from starlette.config import Config
from starlette.datastructures import Secret

try:
    config = Config(".env")
except FileNotFoundError:
    config = Config()

DATABASE_URL = config("DATABASE_URL", cast=Secret)
TEST_DATABASE_URL = config("TEST_DATABASE_URL", cast=Secret)
SECRET_KEY = config("SECRET_KEY", cast=Secret)
ALGORITHM = config("ALGORITHM", cast=Secret)
ACCESS_TOKEN_EXPIRE_MINUTES = config("ACCESS_TOKEN_EXPIRE_MINUTES", cast=int)
REFRESH_TOKEN_EXPIRE_MINUTES = config("REFRESH_TOKEN_EXPIRE_MINUTES", cast=int)
JWT_REFRESH_SECRET_KEY = config("JWT_REFRESH_SECRET_KEY", cast=Secret)
OPENAI_API_KEY = config("OPENAI_API_KEY", cast=Secret)
ASSISTANT_ID = config("ASSISTANT_ID", cast=Secret)