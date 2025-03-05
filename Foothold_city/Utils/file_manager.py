import pandas as pd


class FileManager:
    def __init__(self):
        """Инициализация класса для управления файлами."""
        self.data = None  # Переменная для хранения данных из файла

    def load_excel(self, file_path, sheet_name=0):
        """
        Загружает данные из Excel-файла.

        :param file_path: Путь к файлу Excel.
        :param sheet_name: Название листа или его индекс (по умолчанию первый лист).
        :return: DataFrame с данными или None в случае ошибки.
        """
        try:
            self.data = pd.read_excel(file_path, sheet_name=sheet_name)
            print(f"Файл успешно загружен: {file_path}")
            return self.data
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден по пути {file_path}")
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
        return None

    def get_data(self):
        """Возвращает данные из загруженного файла."""
        return self.data

    def save_to_excel(self, file_path, data=None, sheet_name="Sheet1"):
        """
        Сохраняет данные в Excel-файл.

        :param file_path: Путь для сохранения файла.
        :param data: Данные для сохранения (DataFrame). Если None, сохраняет текущие данные.
        :param sheet_name: Название листа.
        """
        if data is None:
            data = self.data

        if data is not None:
            try:
                data.to_excel(file_path, sheet_name=sheet_name, index=False)
                print(f"Данные успешно сохранены в файл: {file_path}")
            except Exception as e:
                print(f"Ошибка при сохранении файла: {e}")
        else:
            print("Нет данных для сохранения.")

    def get_city_names(self):
        """
        Возвращает список названий городов из загруженных данных.

        :return: Список названий городов.
        """
        if self.data is not None and 'Город' in self.data.columns:
            return self.data['Город'].tolist()
        else:
            print("Данные не загружены или столбец 'Город' отсутствует.")
            return []

    def get_city_data(self, city_name):
        """
        Возвращает данные для конкретного города.

        :param city_name: Название города.
        :return: Словарь с данными о городе или None, если город не найден.
        """
        if self.data is not None and 'Город' in self.data.columns:
            city_data = self.data[self.data['Город'] == city_name]
            if not city_data.empty:
                return city_data.to_dict(orient='records')[0]
        print(f"Город '{city_name}' не найден в данных.")
        return None
