import numpy as np
import pandas as pd


class DataAnalysis:

    @staticmethod
    def fill_data(data):
        """
            Заполняет NaN значения в списке на основе ближайших левого и правого значений.
            :param data: Список числовых значений, который может содержать NaN.
            :return: Список с заполненными значениями вместо NaN.
            """
        n = len(data)
        filled_data = data.copy()  # Создаем копию списка для изменения

        for i in range(n):
            if pd.isna(filled_data[i]):  # Проверяем, является ли значение NaN
                left_value = None
                right_value = None

                # Ищем ближайшее левое значение
                for j in range(i - 1, -1, -1):  # Обратный проход от текущего к началу
                    if not pd.isna(filled_data[j]):
                        left_value = filled_data[j]
                        break

                # Ищем ближайшее правое значение
                for k in range(i + 1, n):  # Прямой проход от текущего к концу
                    if not pd.isna(filled_data[k]):
                        right_value = filled_data[k]
                        break

                # Если значение все еще не найдено, используем циклическую обработку
                if left_value is None:  # Если левое значение не найдено
                    for j in range(n - 1, -1, -1):  # Ищем справа (конец списка)
                        if not pd.isna(filled_data[j]):
                            left_value = filled_data[j]
                            break

                if right_value is None:  # Если правое значение не найдено
                    for k in range(n):  # Ищем слева (начало списка)
                        if not pd.isna(filled_data[k]):
                            right_value = filled_data[k]
                            break

                # Заполняем NaN средним арифметическим левого и правого значений
                if left_value is not None and right_value is not None:
                    filled_data[i] = (left_value + right_value) / 2
                elif left_value is not None:
                    filled_data[i] = left_value
                elif right_value is not None:
                    filled_data[i] = right_value

        return filled_data

    @staticmethod
    def calculate_polygon_area(city_data):
        """
        Вычисляет площадь многоугольника, образованного значениями на осях.
        :param city_data: Список нормированных значений критериев для города.
        :return: Площадь фигуры.
        """
        n = len(city_data)  # Количество критериев
        angles = [2 * 3.14159 * i / n for i in range(n)]  # Углы для каждой оси
        points = []

        # Вычисляем координаты точек
        for i, value in enumerate(city_data):
            x = value * np.cos(angles[i])  # Координата x
            y = value * np.sin(angles[i])  # Координата y
            points.append((x, y))

        # Добавляем первую точку в конец для замыкания фигуры
        points.append(points[0])

        # Вычисляем площадь многоугольника
        area = 0
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]
            area += x1 * y2 - y1 * x2

        return abs(area) / 2

    @staticmethod
    def sort_variant_1(cities_values):
        # Сортировка городов по убыванию значений value
        sorted_cities_all = sorted(
            cities_values.items(),
            key=lambda x: x[1]["value"], reverse=True
        )

        # Исключение первого и последнего города для анализа
        filtered_cities = [data["full_data"] for city, data in sorted_cities_all[1:-1]]

        # Вычисление среднего значения для каждого критерия
        avg_full_data = [sum(values) / len(filtered_cities) for values in zip(*filtered_cities)]

        # Формирование результата
        result = []
        order_priority = {
            "Опорный город 1 порядка": 1,
            "Опорный город 2 порядка": 2,
            "Опорный город 3 порядка": 3,
            "Опорный город 4 порядка": 4
        }

        for i, (city, data) in enumerate(sorted_cities_all):
            if i == 0:
                order = "Опорный город 1 порядка"
            elif i == len(sorted_cities_all) - 1:
                order = "Опорный город 3 порядка"
            else:
                count_above_avg = sum(1 for value, avg in zip(data["full_data"], avg_full_data) if value >= avg)
                order = "Опорный город 2 порядка" if count_above_avg / len(
                    avg_full_data) > 0.5 else "Опорный город 3 порядка"

            result.append({
                "Название города": city,
                "Порядок опорного города": order,
                "value": data["value"]
            })

        # Сортировка результата по порядку опорного города
        result = sorted(result, key=lambda x: order_priority[x["Порядок опорного города"]])

        return result

    @staticmethod
    def sort_variant_2(cities_values):
        # Шаг 1: Определение экстремумов по критериям
        max_city = None
        max_score = float('-inf')
        for city, data in cities_values.items():
            total_score = sum(data["full_data"])  # Сумма всех критериев
            if total_score > max_score:
                max_score = total_score
                max_city = city

        # Город с максимальными значениями (Опорный город 1 порядка)
        result = [{"Название города": max_city, "Порядок опорного города": "Опорный город 1 порядка",
                   "value": cities_values[max_city]["value"]}]

        # Исключаем лидера из дальнейшего анализа
        remaining_cities = {city: data for city, data in cities_values.items() if city != max_city}

        # Шаг 2: Первый фактор сравнения (среднее место относительно лидера)
        criteria_count = len(next(iter(cities_values.values()))["full_data"])  # Количество критериев
        rankings_1 = {}
        for city, data in remaining_cities.items():
            ranks = [
                sum(1 for other_city in remaining_cities if remaining_cities[other_city]["full_data"][i] > value) + 1
                for i, value in enumerate(data["full_data"])]
            avg_rank = sum(ranks) / criteria_count
            rankings_1[city] = avg_rank

        # Шаг 3: Второй фактор сравнения (площадь графика и ранг)
        rankings_2 = {}
        for city, data in remaining_cities.items():
            area = DataAnalysis.calculate_polygon_area(data["full_data"])  # Вычисляем площадь
            rankings_2[city] = area

        # Определяем ранги по площади
        sorted_by_area = sorted(rankings_2.items(), key=lambda x: x[1], reverse=True)
        area_ranks = {city: rank + 1 for rank, (city, _) in enumerate(sorted_by_area)}

        # Шаг 4: Общее значение (среднее между местами по двум факторам)
        overall_scores = {}
        for city in remaining_cities:
            overall_score = (rankings_1[city] + area_ranks[city]) / 2
            overall_scores[city] = overall_score

        # Сортировка оставшихся городов по общему значению
        sorted_remaining = sorted(
            overall_scores.items(),
            key=lambda x: x[1]
        )

        # Формирование результата
        for city, _ in sorted_remaining:
            result.append({
                "Название города": city,
                "Порядок опорного города": "Опорный город 2 порядка" if len(result) == 1 else "Опорный город 3 порядка",
                "value": cities_values[city]["value"]
            })

        return result
