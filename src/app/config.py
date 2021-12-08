from pydantic import BaseSettings


class Settings(BaseSettings):
    authjwt_secret_key: str = "cd1fecf4a1e926647380fedd9fcd706ee3c0dbe4c7a9f18b45932eb0351964e8"
    postgres_url: str = "postgresql://pkthfznrzjwufa:3a1003d279f4c57fb056576a0bceff4c570d01421d8a6c9398bdfacbd58d6190@ec2-54-216-17-9.eu-west-1.compute.amazonaws.com:5432/dukoskle53nmk"
    # timeout: int = 5

    class Config:
        env_file = '.env'
