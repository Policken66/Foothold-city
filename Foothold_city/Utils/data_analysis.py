import numpy as np
import pandas as pd


class DataAnalysis:

    @staticmethod
    def fill_data(data, criteria_names):
        """
        Заполняет NaN значения в списке на основе ближайших левого и правого значений.
        :param data: Список числовых значений, который может содержать NaN.
        :param criteria_names: Список названий критериев (для определения, какие критерии были дополнены).
        :return: Кортеж из двух элементов:
            1. Список с заполненными значениями вместо NaN.
            2. Список названий критериев, которые были дополнены.
        """
        n = len(data)
        filled_data = data.copy()  # Создаем копию списка для изменения
        filled_criteria = []  # Список для хранения названий дополненных критериев

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

                # Добавляем название критерия в список дополненных
                filled_criteria.append(criteria_names[i])

        return filled_data, filled_criteria

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
                order = "Опорный город 4 порядка"
            else:
                # Инициализируем счётчик
                count_above_avg = 0

                # Проходим по парам значений из двух списков
                for value, avg in zip(data["full_data"], avg_full_data):
                    # Проверяем условие
                    if value >= avg:
                        count_above_avg += 1  # Увеличиваем счётчик, если условие выполнено
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
        # Шаг 3: Убираем из расчета город с максимальной и минимальной площадью
        sorted_areas = sorted(cities_values.items(), key=lambda x: x[1]["value"])
        min_city, max_city = sorted_areas[0][0], sorted_areas[-1][0]
        remaining_cities = {city: data for city, data in cities_values.items() if city not in [min_city, max_city]}

        print("remaining_cities")
        print(remaining_cities)

        # Шаг 4: Определяем экстремумы для каждого критерия (всегда 0 и 10)
        criteria_count = len(next(iter(cities_values.values()))["full_data"])
        extremes = [(0, 10)] * criteria_count

        print("extremes")
        print(extremes)

        # Шаг 5: Фактор 1
        factor_1_scores = {}
        for city, data in remaining_cities.items():
            # Шаг 5.1: Сравниваем города по каждому критерию
            criterion_scores = []
            for value, (min_val, max_val) in zip(data["full_data"], extremes):
                # Чем ближе значение к максимуму, тем меньше баллов
                score = max_val - value
                criterion_scores.append(score)

            # Шаг 5.3: Суммируем баллы для каждого города по всем критериям
            total_score = sum(criterion_scores)
            factor_1_scores[city] = total_score

        print("factor_1_scores")
        print(factor_1_scores)

        # Шаг 5.4: Присваиваем баллы за удаление от первого места
        sorted_factor_1 = sorted(factor_1_scores.items(), key=lambda x: x[1])
        factor_1_ranks = {city: rank for rank, (city, _) in enumerate(sorted_factor_1)}

        print("factor_1_ranks")
        print(factor_1_ranks)

        # Шаг 6: Фактор 2
        factor_2_scores = {}
        for city, data in remaining_cities.items():
            # Шаг 6.1: Сравниваем города по площади графиков
            area = data["value"]

            # Шаг 6.2: Присваиваем баллы за удаление от первого места
            factor_2_scores[city] = area

        # Присваиваем баллы за удаление от первого места
        sorted_factor_2 = sorted(factor_2_scores.items(), key=lambda x: x[1], reverse=True)
        factor_2_ranks = {city: rank for rank, (city, _) in enumerate(sorted_factor_2)}

        print("factor_2_ranks")
        print(factor_2_ranks)

        # Шаг 7: Рассчитываем среднее арифметическое между факторами
        overall_scores = {
            city: (factor_1_ranks[city] + factor_2_ranks[city]) / 2 for city in remaining_cities
        }

        # Формируем результат
        result = [{"Название города": max_city, "Порядок опорного города": "Опорный город 1 порядка",
                   "value": cities_values[max_city]["value"]}]

        for city, _ in sorted(overall_scores.items(), key=lambda x: x[1]):
            result.append({
                "Название города": city,
                "Порядок опорного города": "Опорный город 2 порядка" if len(result) == 1 else "Опорный город 3 порядка",
                "value": overall_scores[city]
            })

        result.append({"Название города": min_city, "Порядок опорного города": "Опорный город 4 порядка",
                       "value": cities_values[min_city]["value"]})

        return result
