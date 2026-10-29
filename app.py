from flask import Flask, render_template, url_for, request, redirect
from views import views
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from script import _run_scraper_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # /// - relative path
db = SQLAlchemy(app)


class Recipe(db.Model):
    __tablename__ = "recipes"
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    name = db.Column(db.String(200))
    ingredients = db.relationship("IngredientsList", back_populates="recipe")
    date_added = db.Column(db.DateTime, default=datetime.now)

    # initialize the object
    def __init__(self, content):
        self.content = content

    # Every time a new element is made it will return recipe and id of that recipe that's been created
    def __repr__(self):
        return f"<Recipe {self.id}>"


class IngredientsList(db.Model):
    __tablename__ = "ingredients"
    id = db.Column(db.Integer, primary_key=True)
    ingredient = db.Column(db.String(200), nullable=False)
    recipe_id = db.Column(db.Integer, db.ForeignKey("recipes.id"))
    recipe = db.relationship("Recipe", back_populates="ingredients")

    # initialize the object
    def __init__(self, ingredient):
        self.ingredient = ingredient

    # date_added = db.Column(db.DateTime, default=datetime.now)

    # Every time a new element is made it will return recipe and id of that recipe that's been created
    def __repr__(self):
        return f"<Ingredient {self.id}>"


@app.route("/", methods=["POST", "GET"])
# python decorator - decorate or add functionality to function we will add
# Can also send data to db
def index():
    if request.method == "POST":
        recipe_content = request.form["content"]
        new_recipe = Recipe(content=recipe_content)
        # print(Recipe)
        recipe_ingredients = _run_scraper_(recipe_content)
        try:
            db.session.add(new_recipe)
            # db.session.add(recipe_ingredients)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was an issue adding your recipe: {e}"
    else:
        # Looks at db contents in order of when they were created and return all
        recipes = Recipe.query.order_by(Recipe.date_added).all()
        return render_template("index.html", recipes=recipes)


@app.route("/delete/<int:id>")
def delete(id):
    recipe_to_delete = Recipe.query.get_or_404(id)

    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was an issue adding your recipe: {e}"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == "POST":
        recipe.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was an issue adding your recipe: {e}"
    else:
        return render_template("update.html", recipe=recipe)


@app.route("/view_recipe/<int:id>", methods=["GET", "POST"])
def view_recipe(id):
    recipe = Recipe.query.get_or_404(id)
    if request.method == "POST":
        recipe.content = request.form["content"]
        try:
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was an issue opening your recipe: {e}"
    else:
        return render_template("view_recipe.html", recipe=recipe)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)
