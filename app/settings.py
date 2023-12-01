from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DEBUG: bool = True

    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    API_KEY: str = "top_secret_token"
    API_KEY_NAME: str = "x-api-key"

    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "rootpassword"
    DB_DATABASE: str = "postgres"

    JWT_KEY_NAME: str = 'token'
    JWT_AUTH_SECRET: str = 'top_secret_token'
    JWT_ALGORITHM: str = 'HS256'
    JWT_TOKEN_AUDIENCE: str = 'http://localhost:8080'
    JWT_TOKEN_ISSUER: str = 'http://localhost:8080'
    JWT_EXPIRES: int = 60 * 60 * 24
    
    class Config:
        env_file = ".env"

settings = Settings()