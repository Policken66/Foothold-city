from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
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

        self.spheres = {
            "Политическая": [("Население", 8), ("Избирательная кампания", 3)],
            "Экономическая": [("Связи с городами", 4), ("Предприятия", 6)],
            "Социальная": [("Коэффициент рождаемости", 10), ("Качество городской среды", 4), ("IQ города", 7)], 
            "Духовная": [("Объекты наследия", 5), ("Религиозные конфессии", 3)]
        }
        
        self.setup_quadrants()
    
    """делим на 4 сферы"""
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
    
    def plot_axes(self):
        sphere_angles = {
            "Политическая": (np.pi/12, 5*np.pi/12),    # 15°–75°
            "Экономическая": (7*np.pi/12, 11*np.pi/12), # 105°–165°
            "Социальная": (13*np.pi/12, 17*np.pi/12),   # 195°–255°
            "Духовная": (19*np.pi/12, 23*np.pi/12)      # 285°–345°
        }

        points = []  # Для хранения координат точек критериев
        
        for sphere, axes in self.spheres.items():
            start_angle, end_angle = sphere_angles[sphere]
            count = len(axes)
            total_span = end_angle - start_angle
            step = total_span / (count + 1) if count > 1 else total_span / 2
            
            for i, (axis_name, value) in enumerate(axes):
                angle = start_angle + step * (i + 1)
                max_length = 9  # Максимальная длина оси
                
                # Координаты конца оси
                x_end = max_length * np.cos(angle)
                y_end = max_length * np.sin(angle)
                
                # Координаты точки критерия (пропорционально значению)
                x = (value / max_length) * x_end
                y = (value / max_length) * y_end
                points.append((x, y))
                
                # Рисуем ось со стрелкой
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
                
                # Определение позиции текста оси
                angle_deg = np.degrees(angle) % 360
                ha, va, text_x, text_y = self.get_text_position(
                    angle_deg, x_end, y_end, offset=1.5
                )
                
                # Подпись оси
                self.ax.text(
                    text_x, text_y, axis_name,
                    fontsize=10,
                    ha=ha,
                    va=va,
                    bbox=dict(boxstyle='round,pad=0.2', fc='white', ec='none', alpha=0.9)
                )
                
                # Подпись значения и точка на оси
                self.ax.scatter(x, y, color='red', zorder=3)
                self.ax.text(
                    x * 1.1, y * 1.1, f"{value}",
                    fontsize=8,
                    ha='center',
                    va='center',
                    color='darkred'
                )

        # Отрисовка многоугольника
        if len(points) >= 3:
            points = np.array(points)
            sorted_indices = np.argsort(np.arctan2(points[:, 1], points[:, 0]))
            points = points[sorted_indices]
            X, Y = points[:, 0], points[:, 1]
            
            self.ax.fill(X, Y, color='cyan', alpha=0.3)
            self.ax.plot(np.append(X, X[0]), np.append(Y, Y[0]), 'k-', linewidth=2)

        # Скрытие стандартных осей
        for spine in self.ax.spines.values():
            spine.set_visible(False)
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        self.canvas.draw()
        plt.show()
    
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
    
    def update_graph(self, new_spheres):
        """Обновление данных и перерисовка"""
        self.spheres = new_spheres
        self.setup_quadrants()