class FootholdCityController:
    """Контроллер для обработки событий"""

    def __init__(self, view):
        """
        Инициализация контроллера.
        :param view: Экземпляр класса представления (View).
        """
        self.view = view  # Сохраняем ссылку на представление

        # Подключение сигналов кнопок к соответствующим обработчикам событий
        self.view.ui.pushButton_open.clicked.connect(self.pushButton_open_clicked)
        self.view.ui.pushButton_save.clicked.connect(self.pushButton_save_clicked)

    def pushButton_open_clicked(self):
        print("Button open clicked")

    def pushButton_save_clicked(self):
        print("Button save clicked")

