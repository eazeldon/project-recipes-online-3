import os
from flask import Flask, render_template, redirect, request, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId 

app = Flask(__name__)
app.config["MONGO_DBNAME"] = 'recipes_book'
app.config["MONGO_URI"] = 'mongodb+srv://cakes:CakeSusr@myfirstcluster-ctiu9.mongodb.net/task_manager?retryWrites=true&w=majority'


mongo = PyMongo(app)



@app.route('/')
@app.route('/get_tasks')
def get_tasks():
    return render_template("tasks.html",  tasks=mongo.db.tasks.find()) 

@app.route('/add_task')
def add_task():
   return render_template('addtask.html', categories=mongo.db.categories.find())

@app.route('/home')
def home():
    return render_template("home.html")
                           


@app.route('/recipes')
def recipes():
    return render_template("recipes.html" , recipes=mongo.db.recipes.find())
                           


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/products')
def products():
    return render_template("products.html")


@app.route('/statistic')
def statistic():
    return render_template("statistic.html")



@app.route('/get_categories')
def get_categories():
    return render_template('categories.html',
                           categories=mongo.db.categories.find())


@app.route('/delete_recipies/<recipies_id>')
def delete_recipies(recipies_id):
    mongo.db.recipes.remove({'_id': ObjectId(recipies_id)})
    return redirect(url_for('recipes'))

 
@app.route('/delete_category/<category_id>')
def delete_category(category_id):
    mongo.db.categories.remove({'_id': ObjectId(category_id)})
    return redirect(url_for('get_categories'))


@app.route('/edit_category/<category_id>')
def edit_category(category_id):
    return render_template('editcategory.html',
    category=mongo.db.categories.find_one({'_id': ObjectId(category_id)}))

                   
                   
@app.route('/edit_recipies/<recipies_id>')
def edit_recipies(recipies_id):
    return render_template('editrecipes.html',
    recipies=mongo.db.recipes.find_one({'_id': ObjectId(recipies_id)})

@app.route('/update_category/<category_id>', methods=['POST'])
def update_category(category_id):
     mongo.db.categories.update(
        {'_id': ObjectId(category_id)},
        {'category_name': request.form.get('category_name')})
    return redirect(url_for('get_categories'))



@app.route('/update_recipies/<recipies_id>', methods=['POST'])
def update_recipies(recipies_id):
     mongo.db.recipes.update(
        {'_id': ObjectId(recipies_id)},
        {'recipies_name': request.form.get('recipies_name')})
    return redirect(url_for('recipes'))


@app.route('/insert_recipies', methods=['POST'])
def insert_recipies():
    recipies_doc = {'recipies_name': request.form.get('recipies_name')}
    mongo.db.recipes.insert_one(recipies_doc)
    return redirect(url_for('recipes'))                   

@app.route('/insert_category', methods=['POST'])
def insert_category():
    category_doc = {'category_name': request.form.get('category_name')}
    mongo.db.categories.insert_one(category_doc)
    return redirect(url_for('get_categories'))


@app.route('/add_category')
def add_category():
    return render_template('addcategory.html')
 

                           
@app.route('/add_recipies')
def add_recipies():
    return render_template('addrecipies.html')



 
                           
if __name__ == '__main__':
    app.run(host=os.environ.get('IP'),
            port=int(os.environ.get('PORT')),
            debug=True)
