import numpy as np
import pandas as pd
from PyQt6.QtWidgets import QFileDialog, QGraphicsScene, QSizePolicy, QWidget, QVBoxLayout, QPushButton, QMessageBox
from PyQt6.QtCore import Qt
import matplotlib.pyplot as plt
from PyQt6.uic.properties import QtWidgets

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
        self.view.ui.pushButton_clear.clicked.connect(self.clear_visualization)
        self.view.ui.pushButton_start_sort.clicked.connect(self.pushButton_start_sort_clicked)

        # Настройка QListWidget для множественного выбора
        self.view.ui.listWidget.setSelectionMode(self.view.ui.listWidget.SelectionMode.MultiSelection)
        self.view.ui.listWidget.itemClicked.connect(self.listWidget_itemClicked)

        # Начальные настройки для QComboBox
        self.comboBox_setting()

        # Инициализация состояния виджетов
        # self.hide_listWidget_sort()

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
            self.file_manager.load_excel(file_path)  # Загружаем данные в модель
            cities = self.file_manager.get_city_names()  # Получаем список городов
            print("_________cities_________")
            print(cities)
            # Нормализуем данные
            self.normalized_data = self.file_manager.normalize_data()
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
            popup_visualization.setSizePolicy(
                QSizePolicy.Policy.Expanding,
                QSizePolicy.Policy.Expanding
            )
            layout = QVBoxLayout(self.popup_window)
            layout.addWidget(popup_visualization)
            layout.setContentsMargins(0, 0, 0, 0)

            self.popup_window.showMaximized()
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
            # Удаляем чекбокс города
            self.visualization.remove_city_checkbox(city_name)
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

    def comboBox_setting(self):
        self.view.ui.comboBox_sort.addItem("Не выбран")
        self.view.ui.comboBox_sort.addItem("Вариант 1")
        self.view.ui.comboBox_sort.addItem("Вариант 2")

    def pushButton_start_sort_clicked(self):
        # Получаем выбранные элементы из QListWidget
        selected_items = self.view.ui.listWidget.selectedItems()

        # Получаем выбранный вариант сортировки
        selected_option = self.view.ui.comboBox_sort.currentText()

        # Проверяем, загружены ли нормализованные данные
        if self.normalized_data is None:
            QMessageBox.warning(
                self.view,  # Родительский виджет
                "Ошибка",  # Заголовок окна
                "Данные не загружены."  # Сообщение
            )
            return

        # Проверяем, выбран ли вариант сортировки
        if selected_option == "Не выбран":
            QMessageBox.warning(
                self.view,
                "Ошибка",
                "Сортировка не выбрана."
            )
            return

        # Проверяем, что выбрано минимум три города
        if len(selected_items) < 3:
            QMessageBox.warning(
                self.view,
                "Ошибка",
                "Выберите минимум три города для сортировки."
            )
            return
        selected_cities = [item.text() for item in selected_items]
        # data_selected_cities = self.normalized_data[self.normalized_data['Город'].isin(selected_cities)]

        # Распределение по действиям
        if selected_option == "Вариант 1":
            self.sort_variant_1(selected_cities)
        elif selected_option == "Вариант 2":
            self.sort_variant_1(selected_cities)

    def sort_variant_1(self, cities):
        print("sort_variant_1")
        cities_values = {}
        for city in cities:
            data = self.file_manager.get_city_normalized_data(city)
            full_data = self.fill_data(data)
            value = self.calculate_polygon_area(full_data)
            cities_values[city] = value

        sorted_cities = sorted(cities_values.items(), key=lambda x: x[1], reverse=True)

        output_text = "\n".join([f"{city}: {value:.2f}" for city, value in sorted_cities])

        # Очищаем и обновляем QTextEdit
        self.view.ui.textEdit_sort.clear()
        self.view.ui.textEdit_sort.setText(output_text)

    def sort_variant_2(self, data):
        print("sort_variant_2")

    def fill_data(self, data):
        """
            Заполняет NaN значения в списке на основе ближайших левого и правого значений.
            :param data: Список числовых значений, который может содержать NaN.
            :return: Список с заполненными значениями вместо NaN.
            """
        n = len(data)
        filled_data = data.copy()  # Создаем копию списка для изменения

        for i in range(n):
            if pd.isna(filled_data[i]):  # Проверяем, является ли значение NaN
                left_value = None
                right_value = None

                # Ищем ближайшее левое значение
                for j in range(i - 1, -1, -1):  # Обратный проход от текущего к началу
                    if not pd.isna(filled_data[j]):
                        left_value = filled_data[j]
                        break

                # Ищем ближайшее правое значение
                for k in range(i + 1, n):  # Прямой проход от текущего к концу
                    if not pd.isna(filled_data[k]):
                        right_value = filled_data[k]
                        break

                # Если значение все еще не найдено, используем циклическую обработку
                if left_value is None:  # Если левое значение не найдено
                    for j in range(n - 1, -1, -1):  # Ищем справа (конец списка)
                        if not pd.isna(filled_data[j]):
                            left_value = filled_data[j]
                            break

                if right_value is None:  # Если правое значение не найдено
                    for k in range(n):  # Ищем слева (начало списка)
                        if not pd.isna(filled_data[k]):
                            right_value = filled_data[k]
                            break

                # Заполняем NaN средним арифметическим левого и правого значений
                if left_value is not None and right_value is not None:
                    filled_data[i] = (left_value + right_value) / 2
                elif left_value is not None:
                    filled_data[i] = left_value
                elif right_value is not None:
                    filled_data[i] = right_value

        return filled_data

    def calculate_polygon_area(self, city_data):
        """
        Вычисляет площадь многоугольника, образованного значениями на осях.
        :param city_data: Список нормированных значений критериев для города.
        :return: Площадь фигуры.
        """
        n = len(city_data)  # Количество критериев
        angles = [2 * 3.14159 * i / n for i in range(n)]  # Углы для каждой оси
        points = []

        # Вычисляем координаты точек
        for i, value in enumerate(city_data):
            x = value * np.cos(angles[i])  # Координата x
            y = value * np.sin(angles[i])  # Координата y
            points.append((x, y))

        # Добавляем первую точку в конец для замыкания фигуры
        points.append(points[0])

        # Вычисляем площадь многоугольника
        area = 0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            area += x1 * y2 - y1 * x2

        return abs(area) / 2
