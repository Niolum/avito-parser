import os


DATABASE = {
    "DB_USER": os.getenv("DB_USER", "postgres"),
    "DB_PASS": os.getenv("DB_PASS", "1234"),
    "DB_HOST": os.getenv("DB_HOST", "localhost"),
    "DB_PORT": os.getenv("DB_PORT", "5432"),
    "DB_NAME": os.getenv("DB_NAME", "db")
}

SECRET_KEY = os.getenv("SECRET_KEY", "zmfc9qllfixbnb3nb37z5q6n1055mzf8php9lg64exacgeuam63xjf05ha2fxiyr")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)

try:
    from config_local import *
except:
    pass

SQLALCHEMY_DATABASE_URL = 'postgresql://{}:{}@{}:{}/{}'.format(DATABASE["DB_USER"], DATABASE["DB_PASS"], DATABASE["DB_HOST"], DATABASE["DB_PORT"], DATABASE["DB_NAME"])