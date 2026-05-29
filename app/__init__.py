from flask import Flask
from flask_restful import Api
from flasgger import Swagger


def create_app():
    app = Flask(__name__)

    app.config["SWAGGER"] = {
        "title": "Library API",
        "description": "REST API для управління бібліотекою книг",
        "version": "1.0.0",
        "uiversion": 3,
    }
    Swagger(app)

    api = Api(app)

    from app.resources.books import BookList, BookDetail
    from app.resources.authors import AuthorList, AuthorDetail

    api.add_resource(AuthorList,   "/api/authors")
    api.add_resource(AuthorDetail, "/api/authors/<int:author_id>")
    api.add_resource(BookList,     "/api/books")
    api.add_resource(BookDetail,   "/api/books/<int:book_id>")

    return app
