import json
import pandas as pd


def get_hotel_recommendations(chosen_hotel_id, n_recommendations=5):
    # загрузка данных из файла
    with open('./data/hotels.json', 'r', encoding='utf-8') as f:
        data = json.load(f)

    # создание DataFrame из данных
    df = pd.json_normalize(data, record_path='dictionary_data')
    df['_id'] = df['_id'].apply(lambda x: x["$oid"])

    # задание списка желаемых характеристик
    recommended_features = ['price', 'breakfast_included', 'food_rating']

    # Извлечение идентификатора выбранного отеля
    chosen_hotel = df.loc[df["_id"].apply(lambda x: x["$oid"]) == chosen_hotel_id].iloc[0]
    chosen_hotel_features = chosen_hotel[recommended_features].values
    chosen_hotel_id = chosen_hotel["_id"]["$oid"]

    # вычисление расстояния между выбранным отелем и всеми остальными
    df['distance'] = df[recommended_features].sub(chosen_hotel_features).abs().sum(axis=1)

    # сортировка всех отелей по убыванию расстояния
    sorted_df = df.sort_values(by='distance')

    # исключение выбранного отеля
    sorted_df = sorted_df[sorted_df['_id'] != chosen_hotel_id]

    # выбор топ-N рекомендуемых отелей
    recommended_hotels = sorted_df.iloc[:n_recommendations]

    return recommended_hotels

chosen_hotel_id = '62a20003b076bd79ea7e4e73'
recommended_hotels = get_hotel_recommendations(chosen_hotel_id, n_recommendations=5)

print(recommended_hotels)
