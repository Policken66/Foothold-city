import sys
import os

# Добавляем путь к корневой директории проекта
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from PyQt6.QtWidgets import QApplication

from Foothold_city.Controllers.foothold_city_controller import FootholdCityController
from Foothold_city.Views.foothold_city_view import FootholdCityView
from Foothold_city.Controllers.foothold_city_controller import FootholdCityController

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = FootholdCityView()
    controller = FootholdCityController(view)

    view.show()
    app.exec()
