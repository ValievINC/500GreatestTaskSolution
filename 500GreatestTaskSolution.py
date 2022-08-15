import xml.etree.ElementTree as ET
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter


# Создание датафрейма из xml-документа.
def get_dataframe(xml_data):
    root = ET.XML(xml_data)
    data = []
    cols = []
    for i, child in enumerate(root):
        data.append([subchild.text for subchild in child])
        cols.append(child.tag)
    df = pd.DataFrame(data).T
    df.columns = cols
    return df


# Универсальный каунтер. Считает самые популярные элементы строки.
def count(data, cnt):
    counter = Counter(data).most_common(cnt)
    keys = []
    values = []
    for i in range(cnt):
        keys.append(counter[i][0])
        values.append(counter[i][1])
    return keys, values


# Нахождение топа 11 самых упоминаемых групп.
# Составление диаграммы.
def get_mentions_count(df):
    bands_data = df.iloc[3]
    bands_counts = 11
    names, counts = count(bands_data, bands_counts)     # Собираем имена и количество упоминания имён
    plt.figure(figsize=(11.5, 7))
    plt.barh(names, counts)
    plt.savefig('Top11_bands.png')
    plt.show()


# Нахождения топа 7 жанров.
# Составление диаграммы
def get_genre_pie(df):
    genres_data = df.iloc[4].to_numpy()
    genres_counts = 7
    genres_names, counts = count(genres_data, genres_counts)       # Собираем имена и количество упоминания имён
    total = sum(Counter(genres_data).values())  # Общее количество всех жанров
    others = total - sum(counts)    # Считает количество тех жанров, что не попадают в топ
    counts.append(others)   # Добавляем эти жанры в список топа
    genres_names.append('Others')   # Добавляем общее название тех жанров, что не попали в топ
    plt.figure(figsize=(10, 8))
    plt.pie(counts, labels=genres_names, autopct='%1.1f%%', pctdistance=1.1, labeldistance=1.2)
    plt.savefig('genres_pie.png')
    plt.show()


# Составление CSV таблицы
def get_csv(df, genre):
    genres_data = df.iloc[5].to_numpy()
    bands = []
    # Чисто поиск групп и альбомов, играющих в поджанре
    for k in range(len(genres_data)):
        if genre in genres_data[k]:
            bands.append(df.iloc[[3, 2], [k]].to_numpy().ravel())
    new_df = pd.DataFrame(bands, columns=['Band', 'Album'])
    new_df.to_csv('list.csv', index=False)


xml_data = open('500Greatest.xml', 'r').read()  # Read file
dataframe = get_dataframe(xml_data)
get_mentions_count(dataframe)
get_genre_pie(dataframe)
get_csv(dataframe, "Alternative Rock")
