from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.walker import WalkerCreate, WalkerUpdate

from src.db.walker import Walker


def create_walker(w: WalkerCreate, s: Session):
    walker = Walker()
    walker.price_per_hour = w.price_per_hour
    walker.min_dog_size_in_kg = w.min_dog_size_in_kg
    walker.max_dog_size_in_kg = w.max_dog_size_in_kg
    walker.min_dog_age_in_years = w.min_dog_age_in_years
    walker.max_dog_age_in_years = w.max_dog_age_in_years
    walker.schedule = w.schedule
    walker.about_walker = w.about_walker

    s.add(walker)
    try:
        s.commit()
        return walker
    except IntegrityError:
        return None


def get_walker_by_id(id: int, s: Session):
    return s.query(Walker).filter(Walker.id == id).first()


def get_all_walker(s: Session, limit: int = 100, skip: int = 0):
    return s.query(Walker).limit(limit).offset(skip).all()


def edit_walker(w: WalkerUpdate, id: int, s: Session):
    walker = s.query(Walker).filter(Walker.id == id).first()
    walker.rating = w.rating
    walker.price_per_hour = w.price_per_hour
    walker.counter = w.counter
    walker.min_dog_size_in_kg = w.min_dog_size_in_kg
    walker.max_dog_size_in_kg = w.max_dog_size_in_kg
    walker.min_dog_age_in_years = w.min_dog_age_in_years
    walker.max_dog_age_in_years = w.max_dog_age_in_years
    walker.schedule = w.schedule
    walker.about_walker = w.about_walker

    s.add(walker)
    s.commit()
    return walker
