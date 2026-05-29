from flask_restful import Resource, reqparse
import app.models as models

parser = reqparse.RequestParser()
parser.add_argument("title", type=str, required=True, help="Title is required")
parser.add_argument("author_id", type=int, required=True, help="Author ID is required")
parser.add_argument("year", type=int, required=True, help="Year is required")
parser.add_argument("genre", type=str, required=True, help="Genre is required")


class BookList(Resource):
    def get(self):
        """
        Get all books
        ---
        tags:
          - Books
        responses:
          200:
            description: List of all books
        """
        return list(models.books_db.values()), 200

    def post(self):
        """
        Create a new book
        ---
        tags:
          - Books
        parameters:
          - in: body
            name: body
            required: true
            schema:
              required:
                - title
                - author_id
                - year
                - genre
              properties:
                title:
                  type: string
                  example: Zakhar Berkut
                author_id:
                  type: integer
                  example: 1
                year:
                  type: integer
                  example: 1883
                genre:
                  type: string
                  example: historical
        responses:
          201:
            description: Book created
          404:
            description: Author not found
        """
        args = parser.parse_args()
        if args["author_id"] not in models.authors_db:
            return {"message": "Author not found"}, 404
        bid = models.book_id_counter
        models.books_db[bid] = {
            "id": bid,
            "title": args["title"],
            "author_id": args["author_id"],
            "year": args["year"],
            "genre": args["genre"],
        }
        models.book_id_counter += 1
        return models.books_db[bid], 201


class BookDetail(Resource):
    def get(self, book_id):
        """
        Get book by ID
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
        responses:
          200:
            description: Book found
          404:
            description: Book not found
        """
        book = models.books_db.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        return book, 200

    def put(self, book_id):
        """
        Update book by ID
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
          - in: body
            name: body
            schema:
              properties:
                title:
                  type: string
                author_id:
                  type: integer
                year:
                  type: integer
                genre:
                  type: string
        responses:
          200:
            description: Book updated
          404:
            description: Book not found
        """
        book = models.books_db.get(book_id)
        if not book:
            return {"message": "Book not found"}, 404
        args = parser.parse_args()
        book.update({
            "title": args["title"],
            "author_id": args["author_id"],
            "year": args["year"],
            "genre": args["genre"],
        })
        return book, 200

    def delete(self, book_id):
        """
        Delete book by ID
        ---
        tags:
          - Books
        parameters:
          - in: path
            name: book_id
            type: integer
            required: true
        responses:
          200:
            description: Book deleted
          404:
            description: Book not found
        """
        if book_id not in models.books_db:
            return {"message": "Book not found"}, 404
        del models.books_db[book_id]
        return {"message": "Book deleted"}, 200
