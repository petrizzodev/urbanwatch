from enum import Enum

from pydantic import BaseModel, EmailStr, constr


class UserState(str, Enum):
    ACTIVE = 'active'
    INACTIVE = 'inactive'


class UserDocumentType(str, Enum):
    CEDULA_DE_CIUDADANIA = 'cedula_de_ciudadania'
    TARJETA_DE_IDENTIDAD = 'tarjeta_de_identidad'
    CEDULA_DE_EXTRANJERIA = 'cedula_de_extranjeria'
    PASAPORTE = 'pasaporte'
    OTRO = 'otro'


class User(BaseModel):
    username: str
    email: EmailStr
    full_name: str
    type_document: UserDocumentType
    id_document: constr(min_length=7, max_length=11)
    is_admin: bool = False
    disable_notifications: bool = False
    disabled: bool = False


class UserUpdate(BaseModel):
    full_name: str
    type_document: UserDocumentType
    id_document: constr(min_length=7, max_length=11)
    is_admin: bool = False
    disable_notifications: bool = False
    disabled: bool = False


class UserInDB(User):
    password: str
 
    class Config:
        orm_mode = True
        