from fastapi import APIRouter, Depends, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.crud import client as client_crud
from src.app.dependencies import get_db
from src.schemas.user import UserBase
from src.schemas.client import Client

router = APIRouter(prefix="/client", tags=["Client"])
security = HTTPBearer()


@router.post("/", status_code=200)
async def create_walker(user_info: UserBase, client_info: Client, session: Session = Depends(get_db)):
    return client_crud.create_client(user_arg=user_info, client_arg=client_info, session=session)


@router.get("/", status_code=200)
async def get_client(session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return client_crud.get_client(int(Authorize.get_jwt_subject()), session)


@router.patch("/", status_code=200)
async def set_client(client_info: Client, session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return client_crud.set_client(int(Authorize.get_jwt_subject()), client_info, session)