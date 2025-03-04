from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QSizePolicy

from Foothold_city.Ui.ui_foothold_city import Ui_FootholdCity
from Foothold_city.Views.visualization import *

class FootholdCityView(QMainWindow):
    def __init__(self):
        super().__init__()  # Вызываем конструктор родительского класса
        self.ui = Ui_FootholdCity()  # Создаем экземпляр UI
        self.ui.setupUi(self)  # Устанавливаем интерфейс

        # Создаем и добавляем виджет визуализации
        self.visualization = VisualizationWidget()
        self.ui.graphicsView.setScene(QGraphicsScene(self))  # Create a new QGraphicsScene
        self.ui.graphicsView.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.ui.graphicsView.scene().addWidget(self.visualization)  # Add the VisualizationWidget to the scene
