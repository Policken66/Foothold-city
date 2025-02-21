import sys

from PyQt6.QtWidgets import QApplication

from Foothold_city.Controllers.controller_foothold_city import ControllerFootholdCity
from Foothold_city.Views.view_foothold_city import ViewFootholdCity

if __name__ == "__main__":
    app = QApplication(sys.argv)
    view = ViewFootholdCity()
    controller = ControllerFootholdCity(view)

    view.show()
    app.exec()
