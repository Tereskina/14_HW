import json
import sqlite3

from flask import jsonify


def get_value_from_db(sql):
    """
    Получение данных из sql
    """
    with sqlite3.connect("netflix.db") as connection:
        connection.row_factory = sqlite3.Row

        result = connection.execute(sql).fetchall()

    return result


def search_by_title(title):
    """
    Поиск самого свежего фильма по его названию
    """
    sql = f"""
            SELECT title, country, release_year, listed_in, description
            FROM netflix
            WHERE title = '{title}'
            ORDER BY release_year DESC 
            LIMIT 1
            """

    executed_query = get_value_from_db(sql)

    list_by_title_dict: list[dict] = []

    for film in executed_query:
        list_by_title_dict.append({"title": film[0],
                                   "country": film[1],
                                   "release_year": film[2],
                                   "genre": film[3],
                                   "description": film[4].rstrip('\n')})

    return jsonify(list_by_title_dict)


def search_from_year_to_year(year1, year2):
    """
    Поиск фильмов по диапазону лет выпуска
    """
    sql = f"""
            SELECT title, release_year
            FROM netflix
            WHERE type="Movie"
            AND release_year BETWEEN {year1} AND {year2}
            LIMIT 100
            """

    executed_query = get_value_from_db(sql)
    list_result_year_dict: list[dict] = []

    for film in executed_query:
        list_result_year_dict.append(
            {"title": film[0],
             "release_year": film[1]}
        )

    return jsonify(list_result_year_dict)


def search_by_rating(age_rating):
    """
    Поиска фильмов по рейтингу возрастных ограничений
    """

    rating_dict = {
        "children": ("G", ''),
        "family": ("G", "PG", "PG-13"),
        "adult": ("R", "NC-17")
    }

    sql = f"""
            SELECT title, rating, description
            FROM netflix
            WHERE rating IN {rating_dict[age_rating]}
            """

    list_by_rating = []
    for film in get_value_from_db(sql):
        list_by_rating.append({
            "title": film[0],
            "rating": film[1],
            "description": film[2].rstrip('\n')
        })

    return jsonify(list_by_rating)


def search_by_genre(genre):
    """
    Поиск 10 самых свежих фильмов по жанру
    """
    sql = f"""
        SELECT title, description
        FROM netflix
        WHERE listed_in LIKE '{genre}'
        ORDER BY release_year DESC
        LIMIT 10
        """

    list_by_genre = []
    for film in get_value_from_db(sql):
        list_by_genre.append({
            "title": film[0],
            "description": film[1].rstrip('\n')
        })

    return jsonify(list_by_genre)


def search_by_actors(actor1, actor2):
    """
    Поиск актёров, которые снимались вместе с 2-мя заданными актёрами 2 или более раз
    """


    sql = (f"""
        SELECT "cast"
        FROM netflix
        WHERE "cast" LIKE '%{actor1}%' AND "cast" LIKE '%{actor2}%'
        """)

    with sqlite3.connect("../netflix.db") as connection:
        connection.row_factory = sqlite3.Row

    list_of_actors = []

    for film in connection.execute(sql).fetchall():
        list_of_actors.extend(film[0].split(', '))

    searched_actors = list({actor for actor in list_of_actors if list_of_actors.count(actor) >= 2} - {actor1, actor2})

    return searched_actors


# print(search_by_actors('Rose McIver', 'Ben Lamb'))


def search_by_request(type_, year, genre):
    """
    Поиск по типу картину, году выпуска и жанру
    """
    sql = f"""
        SELECT title, description
        FROM netflix
        WHERE type = '{type_}'
        AND release_year = '{year}'
        AND listed_in LIKE '%{genre}%'
        """

    with sqlite3.connect("../netflix.db") as connection:
        connection.row_factory = sqlite3.Row

    multi_request_list = []
    for film in connection.execute(sql).fetchall():
        multi_request_list.append(
            {"title": film[0],
             "description": film[1]
             })

    return json.dumps(multi_request_list, ensure_ascii=False, indent=4)


# print(search_by_request('Movie', 2014, 'Dramas'))
