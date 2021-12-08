from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.dog import DogCreate, DogUpdate

from src.db.dog import Dog


def create_dog(d: DogCreate, user_id: int, s: Session):
    dog = Dog()
    dog.breed = d.breed
    dog.nickname = d.nickname
    dog.size_in_kg = d.size_in_kg
    dog.date_of_birth = d.date_of_birth
    dog.user_id = user_id

    s.add(dog)
    try:
        s.commit()
        return dog
    except IntegrityError:
        return None


def get_dog_by_id(id: int, s: Session):
    return s.query(Dog).filter(Dog.id == id).first()


def get_all_user_dog(s: Session, user_id: int):
    return s.query(Dog).filter(Dog.user_id == user_id).all()


def edit_dog(d: DogUpdate, id: int, user_id: int, s: Session):
    dog = s.query(Dog).filter(Dog.id == id).first()
    if dog.user_id == user_id:
        dog.breed = d.breed
        dog.nickname = d.nickname
        dog.size_in_kg = d.size_in_kg
        dog.date_of_birth = d.date_of_birth

        s.add(dog)
        s.commit()
        return dog
    return None


def edit_avatar_path(id: int, user_id: int, avatar_path: str, s: Session):
    dog = s.query(Dog).filter(Dog.id == id).first()
    if dog.user_id == user_id:
        dog.avatar_path = avatar_path

        s.add(dog)
        s.commit()
        return dog
    return None


def delete_avatar_path(id: int, user_id: int, s: Session):
    dog = s.query(Dog).filter(Dog.id == id).first()
    if dog.user_id == user_id:
        dog.avatar_path = None

        s.add(dog)
        s.commit()
        return dog
    return None
