from flask import Flask, render_template, url_for, request, redirect
from views import views
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from script import _run_scraper_

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"  # /// - relative path
db = SQLAlchemy(app)


class Todo(db.Model):
    # initialize the object
    def __init__(self, content):
        self.content = content

    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.now)

    # Every time a new element is made it will return recipe and id of that recipe that's been created
    def __repr__(self):
        return f"<Recipe {self.id}>"


@app.route("/", methods=["POST", "GET"])
# python decorator - decorate or add functionality to function we will add
# Can also send data to db
def index():
    if request.method == "POST":
        recipe_content = request.form["content"]
        new_recipe = Todo(content=recipe_content)

        try:
            db.session.add(new_recipe)
            db.session.commit()
            return redirect("/")
        except Exception as e:
            return f"There was an issue adding your recipe: {e}"
    else:
        # Looks at db contents in order of when they were created and return all
        recipes = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", recipes=recipes)


@app.route("/delete/<int:id>")
def delete(id):
    recipe_to_delete = Todo.query.get_or_404(id)

    try:
        db.session.delete(recipe_to_delete)
        db.session.commit()
        return redirect("/")
    except Exception as e:
        return f"There was an issue adding your recipe: {e}"


@app.route("/update/<int:id>", methods=["GET", "POST"])
def update(id):
    recipe = Todo.query.get_or_404(id)
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
    recipe = Todo.query.get_or_404(id)
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
