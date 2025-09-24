from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional
from enum import Enum


class UserStatus(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"


class UserBase(BaseModel):
    """Базовая схема пользователя"""
    name: str = Field(..., min_length=1, max_length=50, description="Имя пользователя")
    email: EmailStr = Field(None, description="Email пользователя")
    age: int = Field(..., ge=0, le=150, description="Возраст пользователя")
    status: UserStatus = Field(default=UserStatus.ACTIVE, description="Статус пользователя")

    model_config = ConfigDict(extra='forbid')


class UserCreate(UserBase):
    """Схема для создания пользователя"""
    pass


class UserUpdate(BaseModel):
    """Схема для обновления пользователя"""
    name: Optional[str] = Field(None, min_length=1, max_length=50, description="Имя пользователя")
    email: Optional[EmailStr] = Field(None, description="Email пользователя")
    age: Optional[int] = Field(None, ge=0, le=150, description="Возраст пользователя")
    status: Optional[UserStatus] = Field(None, description="Статус пользователя")


class User(UserBase):
    """Схема пользователя с ID"""
    id: int = Field(..., description="Уникальный идентификатор пользователя")

    class Config:
        from_attributes = True


class UserList(BaseModel):
    """Схема для списка пользователей"""
    users: list[User]
    total: int