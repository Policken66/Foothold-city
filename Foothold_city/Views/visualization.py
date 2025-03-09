import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.patches import FancyArrowPatch
from PyQt6.QtWidgets import QWidget, QVBoxLayout
import numpy as np

class VisualizationWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.figure, self.ax = plt.subplots(figsize=(6, 6))
        self.canvas = FigureCanvas(self.figure)
        
        layout = QVBoxLayout(self)
        layout.addWidget(self.canvas)
        self.setLayout(layout)

        # Определяем оси в каждой сфере
        self.spheres = {
            "Политическая": ["Население", "Избирательная кампания"],
            "Экономическая": ["Связи с городами", "Предприятия"],
            "Социальная": ["Коэффициент рождаемости", "Качество городской среды", "IQ города"],
            "Духовная": ["Объекты наследия", "Религиозные конфессии"]
        }
        
        self.setup_quadrants()
    
    """делим на 4 квадранта"""
    def setup_quadrants(self):
        self.ax.clear()
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        
        # Разделение на 4 части
        self.ax.axhline(y=0, color='gray', linewidth=1, linestyle='--')
        self.ax.axvline(x=0, color='gray', linewidth=1, linestyle='--')
        
        # Подписи к сферам
        self.ax.text(5, 5, 'Политическая сфера', ha='center', va='center', fontsize=16, color='gray')
        self.ax.text(-5, 5, 'Экономическая сфера', ha='center', va='center', fontsize=16, color='gray')
        self.ax.text(-5, -5, 'Социальная сфера', ha='center', va='center', fontsize=16, color='gray')
        self.ax.text(5, -5, 'Духовная сфера', ha='center', va='center', fontsize=16, color='gray')
        
        self.plot_axes()
    
    """отрисовка матрицы опорных городов"""
    def plot_axes(self):
        sphere_angles = {
            "Политическая": (np.pi/12, 5*np.pi/12),    # 15°–75°
            "Экономическая": (7*np.pi/12, 11*np.pi/12), # 105°–165°
            "Социальная": (13*np.pi/12, 17*np.pi/12),   # 195°–255°
            "Духовная": (19*np.pi/12, 23*np.pi/12)      # 285°–345°
        }

        axis_positions = {}
        text_offset = 1.5  # Увеличенный отступ для текста

        for sphere, axes in self.spheres.items():
            start_angle, end_angle = sphere_angles[sphere]
            count = len(axes)
            total_span = end_angle - start_angle
            step = total_span / (count + 1)
            
            for i, axis in enumerate(axes):
                angle = start_angle + step * (i + 1)
                x = 7 * np.cos(angle)
                y = 7 * np.sin(angle)
                axis_positions[axis] = (x, y)
                
                # Создание пунктирной оси со стрелкой
                arrow = FancyArrowPatch(
                    (0, 0), (x, y),
                    arrowstyle='->',           # Стрелка на конце
                    linestyle='dashed',        # Пунктирная линия
                    color='blue',
                    mutation_scale=15,         # Размер стрелки
                    linewidth=2,
                    zorder=1                  # Чтобы линия была под текстом
                )
                self.ax.add_patch(arrow)
                
                # Определение позиции текста
                angle_deg = np.degrees(angle) % 360
                ha, va, text_x, text_y = self.get_text_position(angle_deg, x, y, text_offset)
                
                # Добавление текста
                self.ax.text(
                    text_x, text_y, axis,
                    fontsize=10,
                    ha=ha,
                    va=va,
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.9)
                )
        
        # Отрисовка многоугольника и точек
        points = np.array(list(axis_positions.values()))
        sorted_indices = np.argsort(np.arctan2(points[:, 1], points[:, 0]))
        points = points[sorted_indices]
        X, Y = points[:, 0], points[:, 1]
        
        self.ax.fill(X, Y, color='cyan', alpha=0.3)
        self.ax.plot(np.append(X, X[0]), np.append(Y, Y[0]), 'k-')
        self.ax.scatter(X, Y, color='red')

        # Скрытие стандартных осей
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        self.canvas.draw()
        plt.show()

    def get_text_position(self, angle, x, y, offset):
        """Определение позиции и выравнивания текста в зависимости от угла"""
        if 0 <= angle < 45 or 315 <= angle < 360:
            return ('left', 'center', x + offset, y)
        elif 45 <= angle < 135:
            return ('center', 'bottom', x, y + offset)
        elif 135 <= angle < 225:
            return ('right', 'center', x - offset, y)
        else:  # 225 <= angle < 315
            return ('center', 'top', x, y - offset)
        
    def update_graph(self, new_spheres):
        self.spheres = new_spheres
        self.setup_quadrants()
