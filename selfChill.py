import json


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


def get_recommended_tours(file_path, tag_list, top_n=15):
    all_tours = load_tours_data(file_path)
    filtered_tours = filter_tours_by_tags(all_tours, tag_list)

    # Сортируем туры по количеству совпадающих тегов и возвращаем топ-N результатов
    sorted_tours = sorted(filtered_tours, key=lambda x: len(set(x.get("dictionary_data", {}).get("tags", [])) & set(tag_list)), reverse=True)
    return sorted_tours[:top_n]


# Пример использования
tours_file_path = "./data/tours.json"
tags = ["611a817f57f8c10019f8c8eb", "611a84fe57f8c10019f8c905", "611a7d6d57f8c10019f8c8d7"]

recommended_tours = get_recommended_tours(tours_file_path, tags)
for tour in recommended_tours:
    print(tour["dictionary_data"]["title"])
