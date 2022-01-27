from flask import flash

from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user


class Recipe:
    db = "recipes"

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under_thirty = data['under_thirty']
        self.date_made = data['date_made']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user = user.User.get_by_id({"id": data["user_id"]})

    # Create
    @classmethod
    def create(cls, data):
        query = """
        INSERT INTO recipes (user_id, name, description, instructions, under_thirty, date_made, created_at, updated_at)
        VALUES (%(user_id)s, %(name)s, %(description)s, %(instructions)s, %(under_thirty)s, %(date_made)s, NOW(), NOW());
        """
        return connectToMySQL(cls.db).query_db(query, data)

    # Read
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes;"
        results = connectToMySQL(cls.db).query_db(query)
        print(results)
        recipes = []
        for row in results:
            recipes.append(cls(row))

        return recipes

    # Read Many
    
        # Read One
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query, data)
        print(result)
        if len(result) < 1:
            return False

        return cls(result[0])

    # Update
    @classmethod
    def update(cls, data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instructions=%(instructions)s,under_thirty=%(under_thirty)s, updated_at=NOW() WHERE id=%(id)s;"

        return connectToMySQL(cls.db).query_db(query, data)

    # Delete
    @classmethod
    def delete(cls, data):
        query = "DELETE FROM recipes WHERE id = %(id)s;"

        connectToMySQL(cls.db).query_db(query, data)

    # Validator
    @staticmethod
    def validator(post_data):
        is_valid = True

        if len(post_data['name']) < 3:
            flash("Name must be at least 3 characters.")
            is_valid = False

        if len(post_data['description']) < 3:
            flash("Description must be at least 3 characters.")
            is_valid = False

        if len(post_data['instructions']) < 3:
            flash("Instructions must be at least 3 characters.")
            is_valid = False
        
        return is_valid


