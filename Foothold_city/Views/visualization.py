import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import QWidget, QVBoxLayout

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
        
        # Убираем оси и рамки
        for spine in self.ax.spines.values():
            spine.set_visible(False)

        self.ax.set_xticks([])
        self.ax.set_yticks([])
        
        # Обновляем график
        self.canvas.draw()
