from typing import Dict, List
from schemas import User, UserCreate, UserUpdate


class Database:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.current_id = 1

    def get_all_users(self) -> List[User]:
        """Получить всех пользователей"""
        return list(self.users.values())

    def get_user(self, user_id: int):
        """Получить пользователя по ID"""
        return self.users.get(user_id)

    def create_user(self, user: UserCreate) -> User:
        """Создать нового пользователя"""
        new_user = User(
            id=self.current_id,
            name=user.name,
            email=user.email,
            age=user.age,
            status=user.status
        )
        self.users[self.current_id] = new_user
        self.current_id += 1
        return f"Пользователь добавлен{new_user}"

    def update_user(self, user_id: int, user_update: UserUpdate):
        """Обновить пользователя"""
        if user_id not in self.users:
            return None

        existing_user = self.users[user_id]
        update_data = user_update.model_dump(exclude_unset=True)

        updated_user = existing_user.model_copy(update=update_data)
        self.users[user_id] = updated_user

        return updated_user

    def delete_user(self, user_id: int):
        """Удалить пользователя"""
        if user_id in self.users:
            del self.users[user_id]
            return True
        return False


# Создаем экземпляр базы данных
db = Database()