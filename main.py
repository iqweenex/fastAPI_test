from fastapi import FastAPI, HTTPException, status
from typing import List
from schemas import User, UserCreate, UserUpdate, UserList, UserStatus
from database import db

app = FastAPI(
    title="User Management API",
    description="Простое CRUD API для управления пользователями",
    version="1.0.0"
)


@app.get(
    "/users",
    response_model=UserList,
    summary="Получить список всех пользователей",
    description="Возвращает список всех пользователей с пагинацией"
)
async def list_users(skip: int = 0, limit: int = 100):
    """
    Получить список пользователей с поддержкой пагинации.

    - skip: Количество записей для пропуска
    - limit: Максимальное количество записей для возврата
    """
    users = db.get_all_users()[skip:skip + limit]
    return UserList(users=users, total=len(users))


@app.get(
    "/users/{user_id}",
    response_model=User,
    summary="Получить пользователя по ID",
    responses={
        404: {"description": "Пользователь не найден"},
        200: {"description": "Успешный запрос"}
    }
)
async def get_user(user_id: int):
    """
    Получить информацию о конкретном пользователе по его ID.

    - user_id: Уникальный идентификатор пользователя
    """
    user = db.get_user(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return user


@app.post(
    "/users",
    response_model=User,
    status_code=status.HTTP_201_CREATED,
    summary="Создать нового пользователя",
    responses={
        201: {"description": "Пользователь успешно создан"},
        400: {"description": "Некорректные данные"}
    }
)
async def create_user(user: UserCreate):
    """
    Создать нового пользователя.

    - name: Имя пользователя (обязательно)
    - email: Email пользователя (обязательно)
    - age: Возраст пользователя (обязательно)
    - status: Статус пользователя (по умолчанию: active)
    """
    return db.create_user(user)


@app.put(
    "/users/{user_id}",
    response_model=User,
    summary="Полностью обновить пользователя",
    responses={
        200: {"description": "Пользователь успешно обновлен"},
        404: {"description": "Пользователь не найден"}
    }
)
async def update_user(user_id: int, user: UserCreate):
    """
    Полностью обновить данные пользователя.

    - user_id: Уникальный идентификатор пользователя
    - Все поля пользователя: Все поля должны быть переданы
    """
    updated_user = db.update_user(user_id, UserUpdate(**user.model_dump()))
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return updated_user


@app.patch(
    "/users/{user_id}",
    response_model=User,
    summary="Частично обновить пользователя",
    responses={
        200: {"description": "Пользователь успешно обновлен"},
        404: {"description": "Пользователь не найден"}
    }
)
async def partial_update_user(user_id: int, user_update: UserUpdate):
    """
    Частично обновить данные пользователя.

    - user_id: Уникальный идентификатор пользователя
    - Любые поля пользователя: Можно передать только те поля, которые нужно обновить
    """
    updated_user = db.update_user(user_id, user_update)
    if updated_user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )
    return updated_user


@app.delete(
    "/users/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить пользователя",
    responses={
        204: {"description": "Пользователь успешно удален"},
        404: {"description": "Пользователь не найден"}
    }
)
async def delete_user(user_id: int):
    """
    Удалить пользователя по ID.

    - user_id: Уникальный идентификатор пользователя
    """
    if not db.delete_user(user_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Пользователь не найден"
        )


@app.get("/")
async def root():
    return {"message": "User Management API", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    # Только для разработки
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)
