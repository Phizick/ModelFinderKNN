import json
from flask import Flask, request

app = Flask(__name__)


def load_tours_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data


def filter_tours_by_tags(tours, tag_list):
    filtered_tours = []
    for tour in tours:
        dict_data = tour.get("dictionary_data", {})
        tour_tags = dict_data.get("tags", [])

        # Проверяем наличие совпадающих тегов
        is_matching_tags = any(tag in tour_tags for tag in tag_list)

        if is_matching_tags:
            filtered_tours.append(tour)

    return filtered_tours


@app.route('/get_recommended_tours', methods=['POST'])
def get_recommended_tours():
    # Получаем список тегов из POST запроса
    tag_list = request.json.get('tags', [])

    # Загружаем данные всех туров
    tours_file_path = "./data/tours.json"
    all_tours = load_tours_data(tours_file_path)

    # Фильтруем туры по тегам
    filtered_tours = filter_tours_by_tags(all_tours, tag_list)

    # Сортируем туры по количеству совпадающих тегов и возвращаем список результатов
    sorted_tours = sorted(filtered_tours, key=lambda x: len(set(x.get("dictionary_data", {}).get("tags", [])) & set(tag_list)), reverse=True)
    recommended_tours = sorted_tours[:15]

    # Формируем список результатов
    result = []
    for tour in recommended_tours:
        result.append(tour["dictionary_data"])

    # Возвращаем список результатов в формате JSON
    return json.dumps(result)


if __name__ == '__main__':
    app.run()