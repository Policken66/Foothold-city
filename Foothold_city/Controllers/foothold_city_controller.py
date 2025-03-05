from PyQt6.QtWidgets import QFileDialog

from Foothold_city.Utils.file_manager import FileManager
from Foothold_city.Views.foothold_city_view import FootholdCityView


class FootholdCityController:
    """Контроллер для обработки событий"""

    def __init__(self, view: FootholdCityView):
        """
        Инициализация контроллера.
        :param view: Экземпляр класса представления (View).
        """
        self.view = view  # Сохраняем ссылку на представление
        self.file_manager = FileManager()

        # Подключение сигналов кнопок к соответствующим обработчикам событий
        self.view.ui.pushButton_open.clicked.connect(self.pushButton_open_clicked)
        self.view.ui.pushButton_save.clicked.connect(self.pushButton_save_clicked)

        # Подключение сигнала выбора элемента в QListWidget
        self.view.ui.listWidget.itemClicked.connect(self.listWidget_itemClicked)

    def pushButton_open_clicked(self):
        """Обработчик нажатия кнопки 'Open'."""
        print("Button open clicked")

        # Открываем диалог выбора файла
        file_path, _ = QFileDialog.getOpenFileName(
            self.view,  # Родительский виджет
            "Выберите файл",  # Заголовок диалогового окна
            "",  # Начальный каталог
            "Excel Files (*.xlsx *.xls)"  # Фильтр типов файлов
        )

        if file_path:  # Если файл выбран
            print(f"Выбран файл: {file_path}")
            self.file_manager.load_excel(file_path)  # Загружаем данные в модель
            cities = self.file_manager.get_city_names()  # Получаем список городов
            print(cities)
            if cities:
                self.view.ui.listWidget.clear()  # Очищаем список городов
                self.view.ui.listWidget.addItems(cities)  # Добавляем города в список

    def pushButton_save_clicked(self):
        print("Button save clicked")

    def listWidget_itemClicked(self, item):
        """Обработчик выбора элемента в QListWidget."""
        print(item.text())
