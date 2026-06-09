from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    model_name: str
    DATABASE_URL: str

    google_client_id: str
    google_client_secret: str
    password: str

    class Config:
        env_file = ".env"