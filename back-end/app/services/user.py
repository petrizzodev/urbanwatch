from typing import List, Optional

from fastapi import HTTPException

from core.db import SessionLocal
from utils.auth import get_password_hash
from models.user import UserInDB as UserModel
from schemas.user import UserInDB, UserDocumentType, UserUpdate


def validate_email(email: str) -> Optional[None]:
    try:
        db = SessionLocal()
        existing_user = db.query(UserModel).filter(UserModel.email == email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail='The email is already in use')
    finally:
        db.close()


def validate_unique_id_document(id_document: int, type_document: UserDocumentType) -> Optional[None]:
    try:
        db = SessionLocal()
        existing_user = db.query(UserModel).filter(UserModel.id_document == id_document, UserModel.type_document == type_document).first()
        if existing_user:
            raise HTTPException(status_code=400, detail=f'The document {id_document} is already in use for the document type {type_document.value}')
    finally:
        db.close()


def get_user_by_username(username: str) -> UserInDB:
    try:
        db = SessionLocal()
        user = db.query(UserModel).filter(UserModel.username == username).first()
        if not user:
            raise HTTPException(status_code=404, detail='User not found')
        return user
    finally:
        db.close()


def get_all_users() -> List[UserInDB]:
    try:
        db = SessionLocal()
        return db.query(UserModel).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error fetching all users') from e
    finally:
        db.close()


def create_user(user_data: UserInDB) -> UserInDB:
    validate_email(user_data.email)
    print(validate_email(user_data.email))
    validate_unique_id_document(user_data.id_document, user_data.type_document)
    print(validate_unique_id_document(user_data.id_document, user_data.type_document))
    try:
        db = SessionLocal()
        hashed_password = get_password_hash(user_data.password)
        user_data.password = hashed_password
        new_user = UserModel(**user_data.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error creating user') from e
    finally:
        db.close()


def update_user(username: str, user_data: UserUpdate) -> UserInDB:
    db_user = get_user_by_username(username)
    if (user_data.id_document != db_user.id_document or 
            user_data.type_document != db_user.type_document):
            validate_unique_id_document(user_data.id_document, user_data.type_document)
    try:    
        db = SessionLocal()
        db_user = db.query(UserModel).filter(UserModel.username == username).first()
        db_user.full_name = user_data.full_name
        db_user.type_document = user_data.type_document
        db_user.id_document = user_data.id_document
        db_user.is_admin = user_data.is_admin
        db_user.disable_notifications = user_data.disable_notifications
        db_user.disabled = user_data.disabled
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error updating user') from e
    finally:
        db.close()


def delete_by_username(username: str) -> bool:
    user = get_user_by_username(username)
    try:
        db = SessionLocal()
        user = db.query(UserModel).filter(UserModel.username == username).first()
        db.delete(user)
        db.commit()
        return True
    except Exception as e:
        raise HTTPException(status_code=500, detail='Error deleting user') from e
    finally:
        db.close()
