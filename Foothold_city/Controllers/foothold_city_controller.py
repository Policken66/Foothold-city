from PyQt6.QtWidgets import QFileDialog, QGraphicsScene, QSizePolicy, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt

from Foothold_city.Utils.file_manager import FileManager
from Foothold_city.Views.foothold_city_view import FootholdCityView
from Foothold_city.Views.visualization import VisualizationWidget


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
        self.view.ui.pushButton_open_plot.clicked.connect(self.pushButton_open_plot_clicked)

        # Настройка QListWidget для множественного выбора
        self.view.ui.listWidget.setSelectionMode(self.view.ui.listWidget.SelectionMode.MultiSelection)
        self.view.ui.listWidget.itemClicked.connect(self.listWidget_itemClicked)

        # Добавляем кнопку очистки графика
        self.clear_button = QPushButton("Очистить график", self.view)
        self.clear_button.clicked.connect(self.clear_visualization)
        self.view.ui.gridLayout.addWidget(self.clear_button, 1, 2, 1, 1)

        # Переменные
        self.visualization = None
        self.normalized_data = None
        self.radial_graphics = None
        self.popup_window = None  # Добавляем переменную для хранения ссылки на окно
        self.example_data = {
            "Политическая": [("Население", 8), ("Избирательная кампания", 3)],
            "Экономическая": [("Связи с городами", 4), ("Предприятия", 6)],
            "Социальная": [("Коэффициент рождаемости", 10), ("Качество городской среды", 4), ("IQ города", 7)],
            "Духовная": [("Объекты наследия", 5), ("Религиозные конфессии", 3)]
        }

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
            self.file_manager.load_excel_2(file_path)  # Загружаем данные в модель
            cities = self.file_manager.get_city_names()  # Получаем список городов
            print("_________cities_________")
            print(cities)
            # Нормализуем данные
            self.normalized_data = self.file_manager.normalize_data_2()
            print("_________normalized_data_________")
            print(self.normalized_data)

            if cities:
                self.view.ui.listWidget.clear()  # Очищаем список городов
                self.view.ui.listWidget.addItems(cities)  # Добавляем города в список

    def pushButton_open_plot_clicked(self):
        print("Button open plot clicked")
        if self.visualization is not None:
            # создаём новый виджет для всплывающего окна
            popup_visualization = VisualizationWidget()
            
            # копируем данные городов в новый виджет
            for city_name, city_data in self.visualization.cities_data.items():
                popup_visualization.add_city_data(city_name, city_data)
            
            # создайм новое окно
            self.popup_window = QWidget()  # Сохраняем ссылку на окно
            self.popup_window.setWindowTitle("График городов")
            layout = QVBoxLayout(self.popup_window)
            layout.addWidget(popup_visualization)
            self.popup_window.resize(800, 800)
            self.popup_window.show()
        else:
            return

    def clear_visualization(self):
        """Очищает график от всех городов и снимает выделение в списке"""
        if self.visualization is not None:
            self.visualization.clear_cities()
            # Пересоздаем виджет визуализации
            self.visualization = VisualizationWidget()
            self.view.ui.graphicsView.setScene(QGraphicsScene(self.view))
            self.view.ui.graphicsView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.view.ui.graphicsView.scene().addWidget(self.visualization)
            
            # Снимаем выделение со всех городов в списке
            self.view.ui.listWidget.clearSelection()

    def listWidget_itemClicked(self, item):
        """Обработчик выбора элемента в QListWidget."""
        city_name = item.text()
        
        # Создаем визуализацию, если она еще не создана
        if self.visualization is None:
            self.visualization = VisualizationWidget()
            self.view.ui.graphicsView.setScene(QGraphicsScene(self.view))
            self.view.ui.graphicsView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
            self.view.ui.graphicsView.scene().addWidget(self.visualization)

        # Получаем данные для выбранного города
        city_spheres_data = self.get_city_spheres_data(city_name)
        
        # Если элемент выбран, добавляем город, если нет - удаляем
        if item.isSelected():
            self.visualization.add_city_data(city_name, city_spheres_data)
        else:
            # Обновляем визуализацию без этого города
            self.visualization.cities_data.pop(city_name, None)
            if self.visualization.cities_data:
                # Если есть другие города, обновляем с последним добавленным
                last_city = next(reversed(self.visualization.cities_data))
                self.visualization.spheres = self.visualization.cities_data[last_city]
            else:
                # Если городов не осталось, очищаем график
                self.visualization.clear_cities()

    def get_city_spheres_data(self, city_name):
        """
        Возвращает данные для конкретного города в требуемом формате.

        :param city_name: Название города.
        :return: Словарь сфер с данными для города.
        """
        if self.normalized_data is None:
            print("Нормализованные данные не загружены.")
            return {}

        # Определение сфер и критериев
        spheres_mapping = self.file_manager.spheres_mapping

        # Фильтруем данные для указанного города
        city_data = self.normalized_data[self.normalized_data['Город'] == city_name]
        if city_data.empty:
            print(f"Город '{city_name}' не найден в данных.")
            return {}

        # Формируем словарь сфер
        city_spheres_data = {}
        for sphere, criteria in spheres_mapping.items():
            sphere_data = []
            for criterion in criteria:
                norm_column = f"{criterion}_норм"
                if norm_column in city_data.columns:
                    value = city_data[norm_column].values[0]  # Берем значение для города
                    sphere_data.append((criterion, value))
            city_spheres_data[sphere] = sphere_data

        return city_spheres_data

    def init_diagram(self):
        # Создаем и добавляем виджет визуализации        
        self.visualization.spheres = self.example_data
        self.view.ui.graphicsView.setScene(QGraphicsScene(self.view))  # Create a new QGraphicsScene
        self.view.ui.graphicsView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.view.ui.graphicsView.scene().addWidget(self.visualization)  # Add the VisualizationWidget to the scene

    def create_and_visualization(self, city_spheres_data):
        if self.visualization is not None:
            self.visualization.plot.close()
        self.visualization = VisualizationWidget()
        self.visualization.spheres = city_spheres_data
        self.view.ui.graphicsView.setScene(QGraphicsScene(self.view))  # Create a new QGraphicsScene
        self.view.ui.graphicsView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.view.ui.graphicsView.scene().addWidget(self.visualization)
