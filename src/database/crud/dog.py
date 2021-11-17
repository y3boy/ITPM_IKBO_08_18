from sqlalchemy.orm import Session

from src.database.models import Dog
from src.schemas import dog as pd_dog


def create_dog(user_id: int, dog_arg: pd_dog.Dog, session: Session):
    dog = Dog(user_id=user_id, **dog_arg.dict())
    session.add(dog)
    session.commit()
    return dog


def get_dog(dog_id: int, session: Session):
    return session.query(Dog).get(dog_id)


def get_all_dog_by_user_id(user_id: int, session: Session):
    return session.query(Dog).filter(Dog.user_id == user_id).all()


def set_dog(dog_id: int, dog_arg: pd_dog.DogEdit, session: Session):
    dog = session.query(Dog).get(dog_id)
    if dog:
        if dog_arg.breed:
            dog.breed = dog_arg.breed
        if dog_arg.nickname:
            dog.nickname = dog_arg.nickname
        if dog_arg.avatar_url:
            dog.avatar_url = dog_arg.avatar_url
        session.add(dog)
        session.commit()
        return dog
    return None


def delete_dog(dog_id, session: Session):
    dog = session.query(Dog).get(dog_id)
    session.delete(dog)
    session.commit()
    return dog