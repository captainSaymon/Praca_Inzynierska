from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from fastapi import HTTPException, Depends
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from schema.user import UserRegisterDetailsSchema, UserLoginDetailsSchema, UsersUpdateDetailsSchema
from functions.password import create_hashed_password, verification_hashed_password
from database.model.users import UsersModel
from functions.token import create_acces_jwt



# REJESTRACJA
def register(db: Session, data: UserLoginDetailsSchema):
    # sprawdzanie czy nie ma uzytkownika z takim samym emialem czy nazwa
    result = db.execute(select(UsersModel).where((UsersModel.email == data.email) | (UsersModel.nickname == data.nickname))).scalars().first()

    if result:
        raise HTTPException(status_code=400, detail="Taki użytkownik już istnieje")

    # tworzenie uzytkowniika
    user = UsersModel(email=data.email, nickname=data.nickname, password=create_hashed_password(data.password), birthday=data.birthday)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user




# LOGOWANIE
def login(db: Session, data: UserLoginDetailsSchema):
    # sprawdzanie czy nazwa uzytkwonika jest w bazie
    user = db.execute(select(UsersModel).where((UsersModel.nickname == data.nickname))).scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="Taki użytkownik nie istnieje")


    # werifikacja hasla zahaszowanego
    result = verification_hashed_password(data.password, user.password)

    if not result:
        raise HTTPException(status_code=404, detail="Hasło niepoprawne")

    token_result = create_acces_jwt(id=user.id, nickname=user.nickname)
    return token_result



# EDYCJA
def edit(db: Session, data: UsersUpdateDetailsSchema):
    # Sprawdzanie id
    user = db.get(UsersModel, data.id)
    if not user:
        raise HTTPException(status_code=404, detail="Nie znaleziono takiego użytkownika.")

    new_data = data.model_dump(exclude_unset=True)

    # zmiana hasla musi byc chaszowana
    if "password" in new_data:
        new_data["password"] = create_hashed_password(new_data["password"])

    for key, value in new_data.items():
        setattr(user, key, value)

    try:
        db.commit()
        db.refresh(user)
        return user
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Użytkownik o takim email/nazwie już istnieje")


# USUWANIE KONTA
def delete(db: Session):
    pass