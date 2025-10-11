from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_DRIVER: str
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DATABASE_URL :str
    TABLE_PREFIX:str = ""

    class Config:
        env_file = ".env"

    BASE_URL: str = "http://localhost:8000"

settings = Settings()
