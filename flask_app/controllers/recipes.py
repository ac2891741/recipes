from flask import render_template, redirect, request, session, flash
from flask_app import app
from flask_app.models.recipe import Recipe
from flask_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route("/new_recipe")
def new_recipe():
    if 'user_id' not in session:
        return redirect('/')
    return render_template('create_recipe.html')

@app.route('/create_new_recipe', methods=['POST'])
def creating_new_recipe():
    if not Recipe.validate_new_recipe(request.form):
        return redirect('/new_recipe')
    data = {
        'name' :  request.form['name'],
        'description' : request.form['description'],
        'instruction' : request.form['instruction'],
        'date_made' : request.form['date_made'],
        'under_30' : request.form['under_30'],
        'user_id' : session['user_id']
    }
    Recipe.save(data)
    return redirect("/dashboard")

@app.route('/dashboard/edit_recipe/<int:recipe_id>')
def edit_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/')
    data = {
        'recipe_id' : recipe_id
    }
    return render_template('edit_recipe.html', recipe = Recipe.get_one(data))


@app.route('/recipes/edit/process/<int:recipe_id>', methods=['POST'])
def update_edited_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect ('/')
    if not Recipe.validate_new_recipe(request.form):
        return redirect(f'/dashboard/edit_recipe/{recipe_id}')

    data ={
        "recipe_id" : request.form['recipe_id'],
        "name" : request.form['name'],
        "description": request.form['description'],
        "instruction": request.form['instruction'],
        "date_made": request.form['date_made'],
        "under_30": request.form['under_30']
    }

    Recipe.update(data)
    # dojo_id = request.form['dojo_id']
    return redirect("/dashboard")

@app.route('/dashboard/view_recipe/<int:recipe_id>')
def view_recipe(recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'recipe_id':recipe_id,
    }
    return render_template('view_recipe.html', recipe = Recipe.select_one(data))

@app.route('/dashboard/destroy/<int:recipe_id>')
def destroy(recipe_id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        'recipe_id': recipe_id,
    }
    Recipe.destroy(data)
    return redirect("/dashboard")