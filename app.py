from flask import Flask

from bp_movie.views import bp_movie

app = Flask(__name__)

app.register_blueprint(bp_movie)

app.run()
