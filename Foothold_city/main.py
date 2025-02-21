import sys

from PyQt6.QtWidgets import QApplication

from Foothold_city.Controllers.foothold_city_controller import FootholdCityController
from Foothold_city.Views.foothold_city_view import FootholdCityView

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = FootholdCityView()
    controller = FootholdCityController(view)

    view.show()
    app.exec()
