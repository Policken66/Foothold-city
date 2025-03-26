from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QMainWindow, QGraphicsScene, QSizePolicy

from Foothold_city.Ui.ui_foothold_city import Ui_FootholdCity
from Foothold_city.Views.visualization import *


class FootholdCityView(QMainWindow):
    def __init__(self):
        super().__init__()  # Вызываем конструктор родительского класса
        self.ui = Ui_FootholdCity()  # Создаем экземпляр UI
        self.ui.setupUi(self)  # Устанавливаем интерфейс

        self.setWindowIcon(QIcon("Resources/Images/icon.png"))

        # Добавляем стили к QListWidget
        self.style_for_QListWidget()

    def style_for_QListWidget(self):
        style = ("""
                    QListWidget {
                        font-size: 16px; /* Размер шрифта для всего списка */
                    }
                
                    QListWidget::item {
                        border: 1px solid #8fbc8f; /* Скругленная рамка вокруг каждого элемента */
                        border-radius: 10px; /* Скругление углов */
                        margin: 5px; /* Пробел между элементами */
                    }
                
                    QListWidget::item:selected {
                        background-color: #b3c9b3; /* Нежно-зеленый цвет фона при выборе элемента */
                        color: #000000; /* Цвет текста при выборе элемента */
                        border: 1px solid #b3c9b3; /* Нежно-зеленая рамка вокруг выбранного элемента */
                        border-radius: 10px; /* Сохраняем скругление углов */
                    }
                """
                 )

        self.ui.listWidget.setStyleSheet(style)
