# Models

## Описание
Данная директория содержит модели приложения.

Модели представляют собой данные и бизнес-логику приложения. Здесь хранятся классы, которые описывают структуру данных и их поведение.

## Содержимое
- `user_model.py`: Модель для представления данных о пользователях.
- `database_model.py`: Модуль для работы с базой данных.
- `config_model.py`: Модель для хранения конфигурационных параметров.

## Пример использования
```python
from Models.user_model import UserModel

user = UserModel(name="John Doe", email="john.doe@example.com")
print(user.get_info())