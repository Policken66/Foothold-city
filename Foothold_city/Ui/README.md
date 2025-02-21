# Ui

## Описание
Данная директория содержит файлы пользовательского интерфейса.

Здесь хранятся файлы, созданные с помощью инструментов для дизайна GUI (например, Qt Designer). Эти файлы обычно преобразуются в Python-код с помощью утилит, таких как `pyuic`.

## Содержимое
- `ui_main_window.py`: Графический интерфейс главного окна.
- `ui_login_dialog.py`: Графический интерфейс диалогового окна входа.
- `ui_settings_dialog.py`: Графический интерфейс окна настроек.

## Пример использования
```python
from PyQt5.QtWidgets import QApplication
from Ui.ui_main_window import Ui_MainWindow

app = QApplication([])
window = Ui_MainWindow()
window.show()
app.exec_()