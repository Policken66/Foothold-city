from PyQt6.QtWidgets import QMainWindow

from Foothold_city.Ui.ui_foothold_city import Ui_FootholdCity


class FootholdCityView(QMainWindow):
    def __init__(self):
        super().__init__()  # Вызываем конструктор родительского класса
        self.ui = Ui_FootholdCity()  # Создаем экземпляр UI
        self.ui.setupUi(self)  # Устанавливаем интерфейс


