from PyQt6.QtWidgets import QFileDialog, QGraphicsScene, QSizePolicy, QWidget, QVBoxLayout

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
        self.view.ui.pushButton_save.clicked.connect(self.pushButton_save_clicked)

        # Подключение сигнала выбора элемента в QListWidget
        self.view.ui.listWidget.itemClicked.connect(self.listWidget_itemClicked)

        # Переменные
        self.visualization = None
        self.normalized_data = None
        self.radial_graphics = None
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
            # self.file_manager.load_excel(file_path)  # Загружаем данные в модель
            cities = self.file_manager.get_city_names()  # Получаем список городов
            print("_________cities_________")
            print(cities)
            # Нормализуем данные
            # self.normalized_data = self.file_manager.normalize_data()
            self.normalized_data = self.file_manager.normalize_data_2()
            print("_________normalized_data_________")
            print(self.normalized_data)


            if cities:
                self.view.ui.listWidget.clear()  # Очищаем список городов
                self.view.ui.listWidget.addItems(cities)  # Добавляем города в список

    def pushButton_save_clicked(self):
        print("Button save clicked")
        self.init_diagram()

    def listWidget_itemClicked(self, item):
        """Обработчик выбора элемента в QListWidget."""

        city_name = item.text()
        # Получаем данные для выбранного города
        city_spheres_data = self.get_city_spheres_data(city_name)
        # Создаем и отображаем визуализацию
        self.create_and_visualization(city_spheres_data)

    def get_city_spheres_data(self, city_name):
        """
        Возвращает данные для конкретного города в требуемом формате.

        :param city_name: Название города.
        :return: Словарь сфер с данными для города.
        """
        if self.normalized_data is None:
            print("Нормализованные данные не загружены.")
            return {}
        print(self.normalized_data)

        # Определение сфер и критериев
        spheres_mapping = {
            "Политическая": ["Население", "Избирательная компания"],
            "Экономическая": ["Связи с городами", "Предприятия"],
            "Социальная": ["Коэффициент рождаемости", "Качество городской среды", "IQ города"],
            "Духовная": ["Объекты населения", "Религиозные конфессии"]
        }
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
        self.visualization = VisualizationWidget()
        self.visualization.spheres = self.example_data
        self.view.ui.graphicsView.setScene(QGraphicsScene(self.view))  # Create a new QGraphicsScene
        self.view.ui.graphicsView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.view.ui.graphicsView.scene().addWidget(self.visualization)  # Add the VisualizationWidget to the scene

    def create_and_visualization(self, city_spheres_data):
        self.visualization = VisualizationWidget()
        self.visualization.spheres = city_spheres_data
        self.view.ui.graphicsView.setScene(QGraphicsScene(self.view))  # Create a new QGraphicsScene
        self.view.ui.graphicsView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.view.ui.graphicsView.scene().addWidget(self.visualization)
