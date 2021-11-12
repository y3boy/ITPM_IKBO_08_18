from fastapi import APIRouter, Depends, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.database.crud import dog as dog_crud
from src.app.dependencies import get_db
from src.schemas.dog import Dog

router = APIRouter(prefix="/dog", tags=["Dog"])
security = HTTPBearer()


@router.post("/", status_code=200)
async def create_dog(dog_info: Dog, session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return dog_crud.create_dog(user_id=int(Authorize.get_jwt_subject()), dog_arg=dog_info, session=session)


@router.get("/", status_code=200)
async def get_all_user_dog(session: Session = Depends(get_db),
                           Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return dog_crud.get_all_dog_by_user_id(int(Authorize.get_jwt_subject()), session)


@router.patch("/", status_code=200)
async def set_dog(dog_info: Dog, session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return dog_crud.set_dog(int(Authorize.get_jwt_subject()), dog_info, session)


@router.delete("/", status_code=200)
async def delete_dog(dog_id: int, session: Session = Depends(get_db)):
    return dog_crud.delete_dog(dog_id, session)