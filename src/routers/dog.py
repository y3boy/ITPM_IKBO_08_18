from typing import List
import os

from fastapi import APIRouter, Depends, HTTPException, Security, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.models.dog import DogOut, DogUpdate, DogCreate
from src.repositories import dog

router = APIRouter(prefix="/dog", tags=["Dog"])
security = HTTPBearer()


@router.get("/", status_code=200, response_model=DogOut)
async def get_dog_by_id(id: int, session: Session = Depends(get_db)):
    return dog.get_dog_by_id(id=id, s=session)


@router.get("/all", status_code=200, response_model=List[DogOut])
async def get_all_current_user_dog(session: Session = Depends(get_db),
                                   Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    return dog.get_all_user_dog(s=session, user_id=int(Authorize.get_jwt_subject()))


@router.post("/", status_code=200, response_model=DogOut)
async def create_dog(dog_info: DogCreate, session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    return dog.create_dog(d=dog_info, user_id=int(Authorize.get_jwt_subject()), s=session)


@router.patch("/", status_code=200, response_model=DogOut)
async def update_dog(dog_info: DogUpdate, dog_id: int, session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    return dog.edit_dog(d=dog_info, id=dog_id, user_id=int(Authorize.get_jwt_subject()), s=session)


@router.patch("/avatar", status_code=200, response_model=DogOut)
async def edit_current_user_avatar(id: int, image: UploadFile = File(...), session: Session = Depends(get_db),
                      Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    try:
        os.mkdir('avatars')
    except Exception as e:
        pass
    try:
        os.mkdir('avatars\\dog')
    except Exception as e:
        pass
    file_name = os.getcwd() + '\\avatars\\dog\\' + str(Authorize.get_jwt_subject()) + '.' + image.filename.split('.')[-1]
    with open(file_name, 'wb+') as f:
        f.write(image.file.read())
        f.close()
    return dog.edit_avatar_path(id=id, user_id=int(Authorize.get_jwt_subject()), avatar_path=jsonable_encoder(file_name), s=session)


@router.delete("/avatar", status_code=200, response_model=DogOut)
async def delete_current_user_avatar(dog_id: int, session: Session = Depends(get_db),
                                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    corr_dog = dog.get_dog_by_id(dog_id, session)
    try:
        os.remove(corr_dog.avatar_path)
        return dog.delete_avatar_path(id=dog_id, user_id=int(Authorize.get_jwt_subject()), s=session)
    except Exception as e:
        pass

