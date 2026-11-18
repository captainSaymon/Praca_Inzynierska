from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from schema.user import UserRegisterDetailsSchema, UserLoginDetailsSchema
from functions.password import create_hashed_password, verification_hashed_password
from database.model.users import UsersModel



def checking_emial_and_nickname(db: Session, email: str, nickname: str):
    result = db.execute(select(UsersModel).where((UsersModel.email == email) | (UsersModel.nickname == nickname))).scalars().first()

    if result:
        raise HTTPException(status_code=400, detail="Taki użytkownik już istnieje")
    return True


def creating_user(db: Session, data: UserRegisterDetailsSchema):
    user = UsersModel(email=data.email, nickname=data.nickname, password=create_hashed_password(data.password), birthday=data.birthday)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def checking_nickname(db: Session, nickname: str):
    result = db.execute(select(UsersModel).where((UsersModel.nickname == nickname))).scalars().first()

    if not result:
        raise HTTPException(status_code=404, detail="Taki użytkownik nie istnieje")
    return result

def verification(password, hashed_password):
    result = verification_hashed_password(password, hashed_password)

    if not result:
        raise HTTPException(status_code=404, detail="Hasło niepoprawne")
    return result


def register(db: Session, data: UserLoginDetailsSchema):
    checking_emial_and_nickname(db, data.email, data.nickname)
    return creating_user(db, data)


def login(db: Session, data: UserRegisterDetailsSchema):
    user = checking_nickname(db, data.nickname)
    verification(data.password, user.password)
    return user