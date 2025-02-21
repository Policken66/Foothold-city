# Controllers

## Описание
Данная директория содержит контроллеры приложения.

Контроллеры отвечают за логику взаимодействия между пользовательским интерфейсом (Views) и данными (Models). Они обрабатывают события пользователя, выполняют бизнес-логику и передают результаты обратно в представления.

## Содержимое
- `main_controller.py`: Основной контроллер приложения.
- `user_controller.py`: Контроллер для работы с пользователями.
- `settings_controller.py`: Контроллер для управления настройками.

## Пример использования
```python
from Controllers.main_controller import MainController

controller = MainController()
controller.handle_event("button_click")