from flask_app.config.mysqlconnection import connectToMySQL
from flask_app.models import user
from flask import flash

class Recipe:

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.date_made = data['date_made']
        self.under_30 = data['under_30']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.creator = None

    @classmethod
    def save(cls,data):
        query = "INSERT INTO recipes (name, description, instruction, date_made, under_30 , user_id) VALUES (%(name)s, %(description)s, %(instruction)s, %(date_made)s, %(under_30)s, %(user_id)s);"
        return connectToMySQL('recipe').query_db(query,data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id;"
        results = connectToMySQL('recipe').query_db(query)
        all_recipes = []

        for row in results:
            one_recipe = cls(row)

            one_recipe_author_info = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at'],
            }
            author = user.User(one_recipe_author_info)
            one_recipe.creator = author

            all_recipes.append(one_recipe)
            
        return all_recipes

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM recipes WHERE recipes.id = %(recipe_id)s;"
        db = connectToMySQL('recipe').query_db(query,data)

        return cls(db[0])

    @classmethod
    def select_one(cls, data):
        query = "SELECT * FROM recipes JOIN users ON recipes.user_id = users.id WHERE recipes.id = %(recipe_id)s;"
        results = connectToMySQL('recipe').query_db(query, data)
        if not results:
            return False
        results = results[0]
        one_recipe = cls(results)

        one_user_info = {
                'id' : results['users.id'],
                'first_name' : results['first_name'],
                'last_name' : results['last_name'],
                'email' : results['email'],
                'password' : results['password'],
                'created_at' :results['users.created_at'],
                'updated_at' : results['users.updated_at'],
            }
        one_recipe.creator = user.User(one_user_info)
        
        return one_recipe

        

    @classmethod
    def update(cls,data):
        query = "UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, date_made=%(date_made)s, under_30=%(under_30)s WHERE id = %(recipe_id)s;"
        return connectToMySQL('recipe').query_db(query,data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM recipes WHERE id = %(recipe_id)s;"
        return connectToMySQL('recipe').query_db(query,data)

    @staticmethod
    def validate_new_recipe(recipe):
        is_valid = True
        if len(recipe["name"]) <= 0 or len(recipe["description"]) <= 0 or len(recipe["instruction"]) <= 0 or len(recipe["date_made"]) <= 0 or len(recipe["under_30"]) <= 0:
            is_valid = False
            flash("All Fields Required")

        return is_valid