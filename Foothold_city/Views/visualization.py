import math
import random
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import numpy as np


class VisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.figure, self.ax = plt.subplots(figsize=(10, 10))
        self.canvas = FigureCanvas(self.figure)
        self._spheres = None
        self.plt_size = 8
        self.plot = plt
        self.cities_data = {}  # словарь для хранения данных нескольких городов
        self.color_palette = ['cyan', 'magenta', 'yellow', 'lime', 'orange', 'purple', 'pink', 'brown']

        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

    def add_city_data(self, city_name, spheres_data):
        """добавить или обновить данные для конкретного города"""
        self.cities_data[city_name] = spheres_data
        self._spheres = spheres_data  #сохранить данные посленего добавленного города для отрисовки осей
        self.setup_quadrants()

    def clear_cities(self):
        """очистить данные о городах"""
        self.cities_data.clear()
        self._spheres = None
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
        self.ax.axhline(y=0, color='gray', linewidth=1, linestyle='--', label='Разделение на сферы')
        self.ax.axvline(x=0, color='gray', linewidth=1, linestyle='--')

        # Подписи к сферам
        self.ax.text(self.plt_size, self.plt_size, 'Политическая сфера', ha='center', va='center', fontsize=16, color='gray')
        self.ax.text(-self.plt_size, self.plt_size, 'Экономическая сфера', ha='center', va='center', fontsize=16, color='gray')
        self.ax.text(-self.plt_size, -self.plt_size, 'Социальная сфера', ha='center', va='center', fontsize=16, color='gray')
        self.ax.text(self.plt_size, -self.plt_size, 'Духовная сфера', ha='center', va='center', fontsize=16, color='gray')

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
        self.ax.plot([0, 0], [0, 0], color='blue', linestyle='--', linewidth=1, 
                    marker='>', markersize=5, label='Оси численных\nхарактеристик\nописания городской среды')
        
        # Добавляем в легенду обозначение для точек (только один раз)
        self.ax.scatter([0], [0], facecolors='none', edgecolors='black', s=50, 
                       label='Точки численных\nхарактеристик\nописания городской среды\n1-го рода')
        
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
                    color='blue',
                    mutation_scale=15,
                    linewidth=1,
                    zorder=1
                )
                self.ax.add_patch(arrow)

                #добавить надпись оси
                angle_deg = np.degrees(angle) % 360
                ha, va, text_x, text_y = self.get_text_position(
                    angle_deg, x_end, y_end, offset=1.5
                )
                self.ax.text(
                    text_x, text_y, axis_name,
                    fontsize=10,
                    ha=ha,
                    va=va,
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.9)
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
                self.ax.text(
                    x * 1.1, y * 1.1, f"{value}",
                    fontsize=8,
                    ha='center',
                    va='center',
                    color=color
                )

        # рисуем полигон
        if len(points) >= 3:
            points = np.array(points)
            sorted_indices = np.argsort(np.arctan2(points[:, 1], points[:, 0]))
            points = points[sorted_indices]
            X, Y = points[:, 0], points[:, 1]

            self.ax.fill(X, Y, color=color, alpha=0.3, label=city_name)
            self.ax.plot(np.append(X, X[0]), np.append(Y, Y[0]), color=color, linewidth=2)

        # добавление легенды
        legend = self.ax.legend(loc='upper left', bbox_to_anchor=(1.14, 1.0), borderaxespad=0.5)
        
        # Adjust the figure to make room for the legend
        self.figure.subplots_adjust(right=0.65)

    def get_text_position(self, angle, x, y, offset):
        """Определение позиции подписи оси"""
        if 0 <= angle < 45 or 315 <= angle < 360:
            return ('left', 'center', x + offset, y)
        elif 45 <= angle < 135:
            return ('center', 'bottom', x, y + offset)
        elif 135 <= angle < 225:
            return ('right', 'center', x - offset, y)
        else:
            return ('center', 'top', x, y - offset)
