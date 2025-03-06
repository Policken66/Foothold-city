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
        """   """
        origin = np.array([0, 0])

        # Определяем 4 вектора
        vectors = np.array([
            [2, 3],  # Вектор 1
            [4, 1],  # Вектор 2
            [-3, 2], # Вектор 3
            [1, -2]  # Вектор 4
        ])

        # Вычисляем углы каждого вектора относительно оси X
        angles = np.arctan2(vectors[:, 1], vectors[:, 0])

        # Сортируем векторы по углу (чтобы обойти их против часовой стрелки)
        sorted_indices = np.argsort(angles)
        vectors = vectors[sorted_indices]

        # Разделяем координаты концов векторов
        U, V = vectors[:, 0], vectors[:, 1]

        # Дублируем начальную точку (ноль) для всех векторов
        X = np.full(len(vectors), origin[0])
        Y = np.full(len(vectors), origin[1])

        # Рисуем векторы
        plt.quiver(X, Y, U, V, angles='xy', scale_units='xy', scale=1, color=['r', 'b', 'g', 'm'], width=0.005)

        # Отмечаем начала и концы векторов
        plt.scatter(origin[0], origin[1], color='black', label="Начало координат")
        plt.scatter(U, V, color=['red', 'blue', 'green', 'magenta'], label="Концы векторов")

        # Соединяем конечные точки векторов в порядке против часовой стрелки и заполняем многоугольник
        plt.fill(U, V, color='cyan', alpha=0.3, label="Заштрихованный многоугольник")  # alpha=0.3 делает заливку прозрачной

        # Оформление графика
        plt.xlim(-4, 5)
        plt.ylim(-3, 4)
        plt.axhline(0, color='gray', linewidth=0.5)
        plt.axvline(0, color='gray', linewidth=0.5)
        plt.grid()
        plt.legend()
        plt.show()
        
        """#Очищаем график
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
        self.canvas.draw()"""       
       
