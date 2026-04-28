from flask_restful import Resource, reqparse
import app.models as models

parser = reqparse.RequestParser()
parser.add_argument("name", type=str, required=True, help="Name is required")
parser.add_argument("birth_year", type=int, required=True, help="Birth year is required")


class AuthorList(Resource):
    def get(self):
        """
        Get all authors
        ---
        tags:
          - Authors
        responses:
          200:
            description: List of all authors
        """
        return list(models.authors_db.values()), 200

    def post(self):
        """
        Create a new author
        ---
        tags:
          - Authors
        parameters:
          - in: body
            name: body
            required: true
            schema:
              required:
                - name
                - birth_year
              properties:
                name:
                  type: string
                  example: Ivan Franko
                birth_year:
                  type: integer
                  example: 1856
        responses:
          201:
            description: Author created
        """
        args = parser.parse_args()
        aid = models.author_id_counter
        models.authors_db[aid] = {"id": aid, "name": args["name"], "birth_year": args["birth_year"]}
        models.author_id_counter += 1
        return models.authors_db[aid], 201


class AuthorDetail(Resource):
    def get(self, author_id):
        """
        Get author by ID
        ---
        tags:
          - Authors
        parameters:
          - in: path
            name: author_id
            type: integer
            required: true
        responses:
          200:
            description: Author found
          404:
            description: Author not found
        """
        author = models.authors_db.get(author_id)
        if not author:
            return {"message": "Author not found"}, 404
        return author, 200

    def put(self, author_id):
        """
        Update author by ID
        ---
        tags:
          - Authors
        parameters:
          - in: path
            name: author_id
            type: integer
            required: true
          - in: body
            name: body
            schema:
              properties:
                name:
                  type: string
                birth_year:
                  type: integer
        responses:
          200:
            description: Author updated
          404:
            description: Author not found
        """
        author = models.authors_db.get(author_id)
        if not author:
            return {"message": "Author not found"}, 404
        args = parser.parse_args()
        author.update({"name": args["name"], "birth_year": args["birth_year"]})
        return author, 200

    def delete(self, author_id):
        """
        Delete author by ID
        ---
        tags:
          - Authors
        parameters:
          - in: path
            name: author_id
            type: integer
            required: true
        responses:
          200:
            description: Author deleted
          404:
            description: Author not found
        """
        if author_id not in models.authors_db:
            return {"message": "Author not found"}, 404
        del models.authors_db[author_id]
        return {"message": "Author deleted"}, 200
