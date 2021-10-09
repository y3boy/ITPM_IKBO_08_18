from pydantic import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str = "SECRET"
    postgres_url: str
    timeout: int = 5

    class Config:
        env_file = '.env'
