from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security, File
from fastapi.responses import Response, FileResponse
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.models.dog import DogOut, DogUpdate, DogCreate
from src.repositories import dog, avatar

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
async def edit_dog_avatar(dog_id: int, image: bytes = File(...), session: Session = Depends(get_db)):
    mapper = avatar.create_avatar(file=image, s=session)
    return dog.edit_avatar_id(dog_id=dog_id, avatar_id=mapper.id, s=session)


@router.get("/avatar", status_code=200, response_class=FileResponse)
async def get_dog_avatar(dog_id: int, session: Session = Depends(get_db)):
    curr_dog = dog.get_dog_by_id(dog_id, session)
    curr_avatar = avatar.get_avatar(curr_dog.avatar_id, session)
    if curr_avatar is None:
        return FileResponse('avatars/dog_default_avatar.png')
    return Response(content=curr_avatar.file, media_type='image/png')


@router.delete("/avatar", status_code=200, response_model=DogOut)
async def delete_dog_avatar(dog_id: int, session: Session = Depends(get_db)):
    curr_dog = dog.get_dog_by_id(dog_id, session)
    curr_avatar = avatar.get_avatar(curr_dog.avatar_id, session)
    if curr_avatar is None:
        raise HTTPException(status_code=400, detail=[{'msg': 'The user does not have an avatar'}])
    avatar.delete_avatar(curr_avatar.id, session)
    return dog.delete_avatar_id(dog_id, session)



