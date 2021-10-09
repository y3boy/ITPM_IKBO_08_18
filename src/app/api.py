from time import time

from sqlalchemy.orm import Session
from sqlalchemy.exc import OperationalError
from typing import Optional
from fastapi import FastAPI, Request, Response, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_jwt_auth import AuthJWT
from fastapi_jwt_auth.exceptions import AuthJWTException
from pydantic import BaseModel

from src.database import models, crud
from src.app.tags import tags_metadata
from src.database.database import engine, SessionLocal
from src.app.dependencies import get_db, get_settings


app = FastAPI(title="Group project backend", version="1.0", openapi_tags=tags_metadata,
              dependencies=[Depends(get_db)])
settings = get_settings()


app.add_middleware(CORSMiddleware,
                   allow_origins=["*"],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"], )


class JWTSettings(BaseModel):
    authjwt_secret_key: str = settings.authjwt_secret_key


@AuthJWT.load_config
def get_config():
    return JWTSettings()


@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )


@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response


@app.on_event("startup")
def startup(db: Session = Depends(get_db)):
    start = time()
    connected = False
    while not connected:
        try:
            models.DataBase.metadata.create_all(bind=engine)
            connected = True
        except OperationalError as e:
            if time() - start > settings.timeout:
                raise e

    with Session(engine) as db:
        pass
        # тут создаем необходимые при старте элементы
