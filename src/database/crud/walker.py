from sqlalchemy.orm import Session

from src.database.models import UserBase, Walker
from src.schemas import walker as pd_walker
from src.database.crud.user import create_user_obj, get_user


def create_walker(user_arg: UserBase, walker_arg: pd_walker.WalkerCreate, session: Session):
    walker = Walker(**walker_arg.dict())
    session.add(walker)
    session.commit()

    user = create_user_obj(user_arg)
    user.walker_id = walker.id
    session.add(user)
    session.commit()
    return user


def get_walker(user_id: int, session: Session):
    user = get_user(user_id, session)
    if user:
        if user.walker_id:
            return session.query(Walker).get(user.walker_id)


def get_all_walker(session: Session):
    return session.query(Walker).all()


def set_walker(user_id: int, walker_arg: pd_walker.Walker, session: Session):
    user = session.query(UserBase).get(user_id)
    if user:
        walker = session.query(Walker).get(user.walker_id)
        if walker:
            if walker_arg.rating:
                walker.rating = walker_arg.rating
            if walker_arg.counter:
                walker.counter = walker_arg.counter
            if walker_arg.region_code:
                walker.region_code = walker_arg.region_code
            if walker_arg.price_per_hour:
                walker.price_per_hour = walker_arg.price_per_hour
            if walker_arg.practice_in_year:
                walker.practice_in_year = walker_arg.practice_in_year
            if walker_arg.min_dog_size_in_kg:
                walker.min_dog_size_in_kg = walker_arg.min_dog_size_in_kg
            if walker_arg.max_dog_size_in_kg:
                walker.max_dog_size_in_kg = walker_arg.max_dog_size_in_kg
            if walker_arg.min_dog_age_in_years:
                walker.min_dog_age_in_years = walker_arg.min_dog_age_in_years
            if walker_arg.max_dog_age_in_years:
                walker.max_dog_age_in_years = walker_arg.max_dog_age_in_years
            if walker_arg.schedule:
                walker.schedule = walker_arg.schedule
            if walker_arg.about_walker:
                walker.about_walker = walker_arg.about_walker
            session.add(walker)
            session.commit()
            return walker
    return None