import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import numpy as np

class VisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvas(self.figure)
        self.setup_quadrants()
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)  # Add the canvas to the layout
        self.setLayout(layout)

    def setup_quadrants(self):
        # Очищаем график
        self.ax.clear()
        
        # Устанавливаем границы графика
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        
        # Рисуем оси координат
        self.ax.axhline(y=0, color='gray', linewidth=1, linestyle='--')
        self.ax.axvline(x=0, color='gray', linewidth=1, linestyle='--')
        
        # Добавляем подписи для каждой четверти
        self.ax.text(5, 5, 'Политическая сфера',                
                    horizontalalignment='center', 
                    verticalalignment='center')
        self.ax.text(-5, 5, 'Экономическая сфера', 
                    horizontalalignment='center', 
                    verticalalignment='center')
        self.ax.text(-5, -5, 'Социальная сфера', 
                    horizontalalignment='center', 
                    verticalalignment='center')
        self.ax.text(5, -5, 'Духовная сфера', 
                    horizontalalignment='center', 
                    verticalalignment='center')
        
        # Добавляем векторы для политической сферы
        num_political_vectors = 2
        political_angles = [0, 90]  # Angles for political vectors
        for angle in political_angles:
            x = 2 * np.cos(np.radians(angle))
            y = 2 * np.sin(np.radians(angle))
            self.ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color='blue' if angle == 0 else 'red')
            label = 'Население' if angle == 0 else 'Избирательная кампания'
            self.ax.text(x, y, label, color='blue' if angle == 0 else 'red', fontsize=10, ha='center', va='bottom', rotation=angle)

        
        # Добавляем векторы для социальной сферы
        num_social_vectors = 3
        social_angles = [0, 120, 240]  # Angles for social vectors
        for angle in social_angles:
            x = 2 * np.cos(np.radians(angle))
            y = 2 * np.sin(np.radians(angle))
            color = 'green' if angle == 0 else 'orange' if angle == 120 else 'purple'
            label = 'Коэффициент рождаемости' if angle == 0 else 'IQ города' if angle == 120 else 'Качество городской среды'
            self.ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color=color)
            self.ax.text(x, y, label, color=color, fontsize=10, ha='center', va='bottom', rotation=angle)


        # Добавляем векторы для экономической сферы
        num_economic_vectors = 2
        economic_angles = [0, 90]  # Angles for economic vectors
        for angle in economic_angles:
            x = 2 * np.cos(np.radians(angle))
            y = 2 * np.sin(np.radians(angle))
            color = 'purple' if angle == 0 else 'brown'
            label = 'Связи с городами' if angle == 0 else 'Предприятия'
            self.ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color=color)

            self.ax.text(-5 + x, y, label, color=color, fontsize=10, ha='center', va='bottom', rotation=angle)


        # Добавляем векторы для духовной сферы
        num_spiritual_vectors = 2
        spiritual_angles = [0, 90]  # Angles for spiritual vectors
        for angle in spiritual_angles:
            x = 2 * np.cos(np.radians(angle))
            y = 2 * np.sin(np.radians(angle))
            color = 'cyan' if angle == 0 else 'magenta'
            label = 'Объекты культурного наследия' if angle == 0 else 'Религиозные конфессии'
            self.ax.quiver(0, 0, x, y, angles='xy', scale_units='xy', scale=1, color=color)

            self.ax.text(5 + x, y, label, color=color, fontsize=10, ha='center', va='bottom', rotation=angle)


        # Убираем оси и рамки
        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Обновляем график
        self.canvas.draw()
