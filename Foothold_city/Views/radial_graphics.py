from PyQt6.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np


class RadialGraphics(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        # Создаем фигуру Matplotlib
        self.figure = Figure()
        self.canvas = FigureCanvas(self.figure)

        # Создаем макет для размещения canvas
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)

        # Инициализация полярной диаграммы
        self.ax = None

    def draw_radial_chart(self, data, city_name):
        """
        Рисует радиальную диаграмму.

        :param data: Словарь с данными для параметров (нормализованные значения).
        :param city_name: Название города.
        """
        # Очищаем предыдущий график
        self.figure.clear()

        # Создаем полярные оси
        self.ax = self.figure.add_subplot(111, polar=True)

        # Подготовка данных
        labels = list(data.keys())
        values = list(data.values())

        # Вычисляем углы для каждого параметра
        angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
        values += values[:1]  # Замыкаем график
        angles += angles[:1]

        # Рисуем линию и заливку
        self.ax.plot(angles, values, color="blue", linewidth=2)
        self.ax.fill(angles, values, color="blue", alpha=0.25)

        # Добавляем метки для параметров
        self.ax.set_xticks(angles[:-1])
        self.ax.set_xticklabels(labels)

        # Устанавливаем заголовок
        self.ax.set_title(f"Город: {city_name}", va='bottom')

        # Обновляем canvas
        self.canvas.draw()