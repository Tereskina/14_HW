from flask import Blueprint

from bp_movie.utils import search_by_title, search_from_year_to_year, search_by_rating, search_by_genre

bp_movie = Blueprint('bp_movie', __name__)


@bp_movie.route('/movie/<title>')
def page_movie_description(title):
    return search_by_title(title)


@bp_movie.route('/movie/<int:year1>/to/<int:year2>/')
def page_movie_year_to_year(year1, year2):
    return search_from_year_to_year(year1, year2)


@bp_movie.route('/rating/<rating>')
def page_rating(rating):
    return search_by_rating(rating)


@bp_movie.route('/genre/<genre>')
def page_genre(genre):
    return search_by_genre(genre)
