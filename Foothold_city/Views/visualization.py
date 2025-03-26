import math
import random
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QCheckBox, QHBoxLayout, QListWidget, QListWidgetItem, QLabel, QPushButton
import numpy as np

# Установка глобальных параметров для шрифта Times New Roman
plt.rcParams['font.family'] = 'serif'
plt.rcParams['font.serif'] = ['Times New Roman']
plt.rcParams['font.size'] = 14  # Размер шрифта по умолчанию

class VisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.ax = plt.subplots(figsize=(20, 20))
        self.canvas = FigureCanvas(self.figure)
        self._spheres = None
        self.plt_size = 12
        self.plot = plt
        self.cities_data = {}  # словарь для хранения данных нескольких городов
        #словарь для цветовой палитры
        self.color_palette = ['#9673a64d', '#b854504d', '#d6b6564d', '#d79b004d', '#82b3664d', '#6c8ebf4d', 
                              '#6666664d', '#b465044d', '#ae41324d', '#0e80884d','#56517e4d','#23445d4d']
        self.value_visibility = {}  # словарь для отслеживания видимости значений для каждого города

        # Создаем основной layout
        main_layout = QHBoxLayout(self)
        
        # Создаем контейнер для графика
        graph_container = QWidget()
        graph_layout = QVBoxLayout(graph_container)
        graph_layout.addWidget(self.canvas)

        self.checkbox_label = QLabel("Скрыть/показать значения")
        self.button_clear_checkboxes = QPushButton("Очистить все")
        self.button_clear_checkboxes.clicked.connect(self.clear_checkboxes)
        self.button_show_checkboxes = QPushButton("Показать все")
        self.button_show_checkboxes.clicked.connect(self.show_checkboxes)

        # Создаем список для чекбоксов
        self.checkbox_list = QListWidget()
        
        # Создаем контейнер для чекбоксов
        checkboxes_container = QWidget()
        checkboxes_layout = QVBoxLayout(checkboxes_container)
        checkboxes_layout.addWidget(self.checkbox_label)
        checkboxes_layout.addWidget(self.checkbox_list)  
        checkboxes_layout.addWidget(self.button_show_checkboxes)  
        checkboxes_layout.addWidget(self.button_clear_checkboxes)              
        
        # Добавляем виджеты в основной layout
        main_layout.addWidget(graph_container)
        main_layout.addWidget(checkboxes_container)     

        # Устанавливаем фиксированную ширину для контейнера с чекбоксами
        checkboxes_container.setFixedWidth(180)

        # Добавляем виджеты в основной layout с указанием коэффициентов stretch
        main_layout.addWidget(graph_container, stretch=3)  # График занимает больше места
        main_layout.addWidget(checkboxes_container, stretch=1)  # Чекбоксы занимают меньше места  
        
        self.setLayout(main_layout)

    def add_city_data(self, city_name, spheres_data):
        """добавить или обновить данные для конкретного города"""
        self.cities_data[city_name] = spheres_data
        self._spheres = spheres_data  #сохранить данные посленего добавленного города для отрисовки осей
        
        # Создаем виджет для чекбокса
        checkbox_widget = QWidget()
        checkbox_layout = QHBoxLayout(checkbox_widget)
        checkbox_layout.setContentsMargins(5, 2, 5, 2)
        
        # Создаем чекбокс
        checkbox = QCheckBox(f"{city_name}")
        checkbox.setChecked(True)  # По умолчанию значения видимы
        checkbox.stateChanged.connect(lambda state, city=city_name: self.toggle_city_values(city, state))
        checkbox_layout.addWidget(checkbox)
        
        # Создаем элемент списка
        item = QListWidgetItem()
        item.setSizeHint(checkbox_widget.sizeHint())
        
        # Добавляем виджет в список
        self.checkbox_list.addItem(item)
        self.checkbox_list.setItemWidget(item, checkbox_widget)
        
        self.value_visibility[city_name] = True
        self.setup_quadrants()

    def remove_city_checkbox(self, city_name):
        """Remove checkbox for a specific city from the list widget"""
        for i in range(self.checkbox_list.count()):
            item = self.checkbox_list.item(i)
            widget = self.checkbox_list.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)
            if checkbox and checkbox.text() == city_name:
                self.checkbox_list.takeItem(i)
                break

    def clear_cities(self):
        """очистить данные о городах"""
        self.cities_data.clear()
        self._spheres = None
        # Очищаем список чекбоксов
        self.checkbox_list.clear()
        self.value_visibility.clear()
        self.setup_quadrants()

    def toggle_city_values(self, city_name, state):
        """Переключение видимости значений для конкретного города"""
        self.value_visibility[city_name] = bool(state)
        self.setup_quadrants()

    @property
    def spheres(self):
        """Геттер для _spheres"""
        return self._spheres

    @spheres.setter
    def spheres(self, spheres):
        """Сеттер для _spheres с обновлением графика"""
        self._spheres = spheres
        self.setup_quadrants()

    def setup_quadrants(self):
        """Метод разделяет график на 4 сферы"""
        self.ax.clear()
        self.ax.set_xlim(-15, 15)
        self.ax.set_ylim(-12, 12)

        # Разделение на 4 части
        self.ax.axhline(y=0, color = (153/255, 153/255, 153/255) , alpha=0.3, linewidth=1, linestyle='--', label='Разделение на сферы')
        self.ax.axvline(x=0, color = (153/255, 153/255, 153/255), alpha=0.3, linewidth=1, linestyle='--')

        # Подписи к сферам
        self.ax.text(self.plt_size, 1, 'Политическая сфера', ha='center', va='center', fontsize=24, color='gray', alpha=0.3,)
        self.ax.text(-self.plt_size, 1, 'Экономическая сфера', ha='center', va='center', fontsize=24, color='gray', alpha=0.3,)
        self.ax.text(-self.plt_size, -1, 'Социальная сфера', ha='center', va='center', fontsize=24, color='gray', alpha=0.3,)
        self.ax.text(self.plt_size, -1, 'Духовная сфера', ha='center', va='center', fontsize=24, color='gray', alpha=0.3,)

        self.plot_axes()

    def plot_axes(self):
        if not self._spheres:
            return

        sphere_angles = {
            "Политическая": (np.pi / 12, 5 * np.pi / 12),  # 15°–75°
            "Экономическая": (7 * np.pi / 12, 11 * np.pi / 12),  # 105°–165°
            "Социальная": (13 * np.pi / 12, 17 * np.pi / 12),  # 195°–255°
            "Духовная": (19 * np.pi / 12, 23 * np.pi / 12)  # 285°–345°
        }

        # рисуем оси один раз, используя данные последнего города
        self._draw_axes(sphere_angles)

        # рисуем матриу для каждого города
        for i, (city_name, city_data) in enumerate(self.cities_data.items()):
            color = self.color_palette[i % len(self.color_palette)]
            self._draw_city_polygon(city_data, sphere_angles, color, city_name)

        # Скрытие стандартных осей
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])

        self.canvas.draw()

    def _draw_axes(self, sphere_angles):
        """рисуем оси и их надписи"""
        # Добавляем в легенду обозначение для осей
        self.ax.plot([0, 0], [0, 0], color = (0/255, 0/255, 0/255) , alpha=0.3, linestyle='--', linewidth=1, 
                    marker='>', markersize=5, label='Оси численных\nхарактеристик\nописания городской среды')
        
        # Добавляем в легенду обозначение для точек (только один раз)
        self.ax.scatter([0], [0], facecolors='none', edgecolors='black', alpha=0.3, s=50, 
                       label='Точки численных\nхарактеристик\nописания городской среды')
        
        for sphere, axes in self._spheres.items():
            start_angle, end_angle = sphere_angles[sphere]
            count = len(axes)
            for i, (axis_name, value) in enumerate(axes):
                if math.isnan(value):
                    count -= 1
            total_span = end_angle - start_angle
            step = total_span / (count + 1) if count > 1 else total_span / 2

            for i, (axis_name, value) in enumerate(axes):
                if math.isnan(value):
                    continue

                angle = start_angle + step * (i + 1)
                max_length = 10

                x_end = max_length * np.cos(angle)
                y_end = max_length * np.sin(angle)

                # рисуем стрелку оси
                arrow = FancyArrowPatch(
                    (0, 0), (x_end, y_end),
                    arrowstyle='->',
                    linestyle='dashed',
                    color = (0/255, 0/255, 0/255) , 
                    alpha=0.3,
                    mutation_scale=15,
                    linewidth=1,
                    zorder=1
                )
                self.ax.add_patch(arrow)

                #добавить надпись оси
                angle_deg = np.degrees(angle) % 360
                ha, va, text_x, text_y = self.get_text_position(
                    angle_deg, x_end, y_end 
                )
                self.ax.text(
                    text_x, text_y, axis_name,
                    fontsize=14,
                    color = (0/255, 0/255, 0/255) , 
                    alpha=0.3,
                    ha=ha,
                    va=va,
                    rotation=angle_deg,
                    rotation_mode='anchor',
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none')
                )

    def _draw_city_polygon(self, city_data, sphere_angles, color, city_name):
        """рисуем матрицу для конкретного города"""
        points = []

        for sphere, axes in city_data.items():
            start_angle, end_angle = sphere_angles[sphere]
            count = len(axes)
            for i, (axis_name, value) in enumerate(axes):
                if math.isnan(value):
                    count -= 1
            total_span = end_angle - start_angle
            step = total_span / (count + 1) if count > 1 else total_span / 2

            for i, (axis_name, value) in enumerate(axes):
                if math.isnan(value):
                    continue

                angle = start_angle + step * (i + 1)
                max_length = 10

                x_end = max_length * np.cos(angle)
                y_end = max_length * np.sin(angle)

                x = (value / max_length) * x_end
                y = (value / max_length) * y_end
                points.append((x, y))

                # рисуем точку
                self.ax.scatter(x, y, color=color, zorder=3)
                
                # Показываем значение только если включена видимость для этого города
                if self.value_visibility.get(city_name, True):
                    self.ax.text(
                        x * 1.1, y * 1.1, f"{value}",
                        fontsize=14,
                        ha='center',
                        va='center',
                        color = (0/255, 0/255, 0/255) , 
                        alpha=0.3,
                    )

        # рисуем полигон
        if len(points) >= 3:
            points = np.array(points)
            sorted_indices = np.argsort(np.arctan2(points[:, 1], points[:, 0]))
            points = points[sorted_indices]
            X, Y = points[:, 0], points[:, 1]

            #self.ax.fill(X, Y, color=color, alpha=0.3, label=city_name)
            self.ax.plot(np.append(X, X[0]), np.append(Y, Y[0]), color=color, linewidth=2, label=city_name)

        # добавление легенды
        legend = self.ax.legend(loc='upper left', bbox_to_anchor=(1.14, 1.0), borderaxespad=0.5, labelcolor='#0000004d')
        
        # Adjust the figure to make room for the legend
        self.figure.subplots_adjust(right=0.65)

    def get_text_position(self, angle, x, y):
        """Определение позиции подписи оси"""
        # Добавляем смещение от конца оси
        offset_x = x
        offset_y = y

        if 0 <= angle < 45:  # Начало 1-й четверти
            return ('left', 'center', offset_x, offset_y)
        elif 45 <= angle < 90:  # Конец 1-й четверти
            return ('left', 'center', offset_x, offset_y)
        elif 90 <= angle < 135:  # Начало 2-й четверти
            return ('left', 'center', offset_x, offset_y)
        elif 135 <= angle < 180:  # Конец 2-й четверти
            return ('left', 'center', offset_x, offset_y)
        elif 180 <= angle < 225:  # конец 3-й четверти
            return ('left', 'center', offset_x, offset_y)
        elif 225 <= angle < 315:  # 4-я четверть
            return ('left', 'center', offset_x, offset_y)
        else:  # конец 4-й четверти (315-360)
            return ('left', 'center', offset_x, offset_y)
    
        
    def clear_checkboxes(self):
        """Сбросить чекбоксы"""
        for i in range(self.checkbox_list.count()):
            item = self.checkbox_list.item(i)
            widget = self.checkbox_list.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)
            if checkbox:
                checkbox.setChecked(False)

    def show_checkboxes(self):
        """выделить чекбоксы"""
        for i in range(self.checkbox_list.count()):
            item = self.checkbox_list.item(i)
            widget = self.checkbox_list.itemWidget(item)
            checkbox = widget.findChild(QCheckBox)
            if checkbox:
                checkbox.setChecked(True)

