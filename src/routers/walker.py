from typing import List

from fastapi import APIRouter, Depends, HTTPException, Security
from fastapi_jwt_auth import AuthJWT
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from src.app.dependencies import get_db
from src.models.walker import WalkerOut, WalkerUpdate, WalkerCreate
from src.models.general import UserWalker
from src.repositories import walker, user, order

router = APIRouter(prefix="/walker", tags=["Walker"])
security = HTTPBearer()


@router.get("/curr", status_code=200, response_model=UserWalker)
async def get_current_walker(session: Session = Depends(get_db),
                     Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    mapper = walker.get_walker_by_id(int(Authorize.get_jwt_subject()), session)
    ratings = order.get_all_rating_and_reviews_walker(int(Authorize.get_jwt_subject()), session)
    sum_rating = 0
    count_rating = 0
    for i in ratings:
        if i.rating:
            sum_rating += i.rating
            count_rating += 1
    try:
        rating = round(sum_rating / count_rating, 1)
    except ZeroDivisionError:
        rating = 0
    mapper.Walker.rating = rating
    return UserWalker(
        User=mapper.User,
        Walker=mapper.Walker,
    )


@router.get("/all", status_code=200, response_model=List[UserWalker])
async def get_all_walker(limit: int = 100, skip: int = 0, session: Session = Depends(get_db)):
    mappers = walker.get_all_walker(session, limit, skip)
    result = []
    for i in mappers:
        ratings = order.get_all_rating_and_reviews_walker(i.User.id, session)
        sum_rating = 0
        count_rating = 0
        for j in ratings:
            if j.rating:
                sum_rating += j.rating
                count_rating += 1
        try:
            rating = round(sum_rating / count_rating, 1)
        except ZeroDivisionError:
            rating = 0
        i.Walker.rating = rating
        result.append(UserWalker(User=i.User, Walker=i.Walker))
    return result


@router.post("/", status_code=200, response_model=WalkerOut)
async def create_walker(walker_info: WalkerCreate, session: Session = Depends(get_db),
                        Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    curr_user = user.get_user_by_id(int(Authorize.get_jwt_subject()), session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User not exist'}])
    curr_walker = walker.create_walker(w=walker_info, s=session)
    if not walker:
        raise HTTPException(status_code=400, detail=[{'msg': 'Walker info not create'}])
    user.edit_walker_id(user_id=int(Authorize.get_jwt_subject()), walker_id=curr_walker.id, s=session)
    return curr_walker


@router.patch("/", status_code=200, response_model=WalkerOut)
async def update_current_walker(walker_info: WalkerUpdate, session: Session = Depends(get_db),
                       Authorize: AuthJWT = Depends(), auth: HTTPAuthorizationCredentials = Security(security)):
    Authorize.jwt_required()
    curr_user = user.get_user_by_id(int(Authorize.get_jwt_subject()), session)
    if not curr_user:
        raise HTTPException(status_code=400, detail=[{'msg': 'User not exist'}])
    curr_walker = walker.edit_walker(id=curr_user.walker_id, w=walker_info, s=session)
    if not walker:
        raise HTTPException(status_code=400, detail=[{'msg': 'Walker info not edit'}])
    return curr_walker


@router.get('/', status_code=200, response_model=UserWalker)
async def get_walker(user_id: int, session: Session = Depends(get_db)):
    curr_walker = walker.get_walker_by_id(user_id, session)
    if not curr_walker:
        raise HTTPException(status_code=400, detail=[{'msg': 'Walker from this User not exist'}])
    ratings = order.get_all_rating_and_reviews_walker(user_id, session)
    sum_rating = 0
    count_rating = 0
    for i in ratings:
        if i.rating:
            sum_rating += i.rating
            count_rating += 1
    try:
        rating = round(sum_rating / count_rating, 1)
    except ZeroDivisionError:
        rating = 0
    curr_walker.Walker.rating = rating
    return UserWalker(User=curr_walker.User, Walker=curr_walker.Walker)

