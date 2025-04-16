import numpy as np
import pandas as pd


class FileManager:
    def __init__(self):
        """Инициализация класса для управления файлами."""
        self.data = None  # Переменная для хранения данных из файла
        self.normalized_data = None
        self.spheres_mapping = {
            "Политическая": [],
            "Экономическая": [],
            "Социальная": [],
            "Духовная": []
        }

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

    def get_city_normalized_data(self, city_name):
        """
        Возвращает список числовых нормализованных данных для конкретного города.
        :param city_name: Название города.
        :return: Список числовых значений (или NaN) или None, если город не найден.
        """
        if self.normalized_data is not None and 'Город' in self.normalized_data.columns:
            # Ищем данные для указанного города
            city_data = self.normalized_data[self.normalized_data['Город'] == city_name]

            if not city_data.empty:
                # Исключаем столбец "Город" и преобразуем оставшиеся данные в список
                numeric_data = city_data.drop(columns=['Город']).values.flatten().tolist()
                return numeric_data

            print(f"Город '{city_name}' не найден в данных.")
            return None
        else:
            print("Нормализованные данные не загружены или столбец 'Город' отсутствует.")
            return None

    def load_excel(self, file_path, sheet_name=0):
        """
        Загружает данные из Excel-файла.

        :param file_path: Путь к файлу Excel.
        :param sheet_name: Название листа или его индекс (по умолчанию первый лист).
        :return: DataFrame с данными или None в случае ошибки.
        """
        try:
            df = pd.read_excel(file_path, sheet_name=sheet_name, header=None)

            # Определение соответствия заголовков сферам
            headers = df.iloc[0]  # Названия заголовков (первая строка)
            sphere_labels = df.iloc[1]  # Метки сфер (вторая строка)
            print("______________headers_______________")
            print(headers)
            print("______________sphere_labels_______________")
            print(sphere_labels)

            for header, sphere in zip(headers, sphere_labels):
                if sphere in self.spheres_mapping:
                    self.spheres_mapping[sphere].append(header)
            print("______________spheres_mapping_______________")
            print(self.spheres_mapping)
            print(f"Файл успешно загружен: {file_path}")

            # Теперь заполняем data
            # Удаление первых трех строк (служебные строки) и сброс индекса
            self.data = df.iloc[2:].reset_index(drop=True)

            # Переименование столбцов на основе второй строки
            self.data.columns = headers

            # Переименование первого столбца в "Город"
            if len(self.data.columns) > 0:
                self.data.rename(columns={self.data.columns[0]: "Город"}, inplace=True)

            # Сортировка столбцов по порядку: политическая → экономическая → социальная → духовная
            sorted_columns = ["Город"]  # Первый столбец всегда "Город"

            # Определяем порядок сфер
            sphere_order = ["Политическая", "Экономическая", "Социальная", "Духовная"]

            # Добавляем столбцы в соответствии с порядком сфер
            for sphere in sphere_order:
                if sphere in self.spheres_mapping:
                    sorted_columns.extend(self.spheres_mapping[sphere])

            # Фильтруем только те столбцы, которые существуют в данных
            sorted_columns = [col for col in sorted_columns if col in self.data.columns]

            # Перестраиваем DataFrame в соответствии с новым порядком столбцов
            self.data = self.data[sorted_columns]

            """# Добавление строки с нулями в конец DataFrame
            zero_row = pd.DataFrame([[0] * len(self.data.columns)], columns=self.data.columns)
            self.data = pd.concat([self.data, zero_row], ignore_index=True)"""
            # Создаем новую строку
            new_row = ["Г0"] + [0] * (len(self.data.columns) - 1)
            # Добавляем строку в DataFrame
            self.data.loc[len(self.data)] = new_row

            print("______________data_______________")
            print(self.data)
            return self.data
        except FileNotFoundError:
            print(f"Ошибка: Файл не найден по пути {file_path}")
        except Exception as e:
            print(f"Ошибка при загрузке файла: {e}")
        return None

    def normalize_data(self):
        """
        Нормализует данные для каждого города.
        :return: DataFrame с нормализованными данными.
        """
        if self.data is not None and 'Город' in self.data.columns:
            # Создаем новый DataFrame для нормализованных данных
            normalized_data = self.data.copy()

            # Преобразуем все столбцы, кроме "Город", в числовой формат
            for column in normalized_data.columns:
                if column != 'Город':
                    normalized_data[column] = pd.to_numeric(normalized_data[column], errors='coerce')

            # Проходим по всем числовым столбцам, кроме "Город"
            for column in normalized_data.columns:
                if column != 'Город' and pd.api.types.is_numeric_dtype(normalized_data[column]):
                    # Удаляем NaN значения для вычисления min и max
                    valid_data = normalized_data[column].dropna()

                    if not valid_data.empty:
                        min_val = valid_data.min()
                        max_val = valid_data.max()

                        if max_val > min_val:  # Избегаем деления на ноль
                            # Выполняем нормализацию только для числовых значений
                            normalized_data[f"{column}_норм"] = normalized_data[column].apply(
                                lambda x: ((x - min_val) / (max_val - min_val)) * 10 if pd.notnull(x) else np.nan
                            ).round(2)
                        else:
                            # Если все значения одинаковы, оставляем NaN или исходное значение
                            normalized_data[f"{column}_норм"] = normalized_data[column].apply(
                                lambda x: np.nan if pd.isnull(x) else 0
                            )
                    else:
                        # Если все значения NaN, оставляем столбец как NaN
                        normalized_data[f"{column}_норм"] = np.nan

            # Возвращаем только столбцы с нормализованными данными
            normalized_columns = [col for col in normalized_data.columns if col.endswith('_норм')]
            self.normalized_data = normalized_data[['Город'] + normalized_columns]
            return self.normalized_data
        else:
            print("Данные не загружены или столбец 'Город' отсутствует.")
            return None

    def get_criteria_names(self):
        """
        Возвращает список названий критериев из нормализованных данных.
        :return: Список названий критериев.
        """
        if self.normalized_data is not None and 'Город' in self.normalized_data.columns:
            # Исключаем столбец "Город" и возвращаем остальные названия столбцов
            criteria_names = [col.replace('_норм', '') for col in self.normalized_data.columns if col != 'Город']
            return criteria_names
        else:
            print("Нормализованные данные не загружены или столбец 'Город' отсутствует.")
            return []

    def print_criterion_data(self, criterion_name):
        """
        Выводит в консоль данные для указанного критерия.

        :param criterion_name: Название критерия (например, "Качество городской среды").
        """
        if self.data is None:
            print("Данные не загружены.")
            return

        # Проверяем, есть ли критерий в заголовках DataFrame
        if criterion_name in self.data.columns:
            print(f"Данные для критерия '{criterion_name}':")
            print(self.data[['Город', criterion_name]])
        else:
            print(f"Критерий '{criterion_name}' не найден в данных.")