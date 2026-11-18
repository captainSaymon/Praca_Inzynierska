from sqlalchemy.orm import Session
from sqlalchemy import select
from fastapi import HTTPException

from schema.user import UserCreateDetailsSchema
from functions.password import create_hashed_password
from database.model.users import UsersModel



def checking_emial_and_nickname(db: Session, email: str, nickname: str):
    result = db.execute(select(UsersModel).where((UsersModel.email == email) | (UsersModel.nickname == nickname))).scalars().first()

    if result:
        raise HTTPException(status_code=400, detail="Taki użytkownik już istnieje")
    return True


def creating_user(db: Session, data: UserCreateDetailsSchema):
    user = UsersModel(email=data.email, nickname=data.nickname, password=create_hashed_password(data.password), birthday=data.birthday)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def create(db: Session, data: UserCreateDetailsSchema):
    checking_emial_and_nickname(db, data.email, data.nickname)
    return creating_user(db, data)