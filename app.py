import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, flash
from models import db, Task, Category

load_dotenv()

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "SECRET_KEY")
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///todos.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)
with app.app_context():
    db.create_all()
    if Category.query.count() == 0:
        default_categories = ["Personal", "Work", "Home", "Urgent"]
        for name in default_categories:
            db.session.add(Category(name=name))
        db.session.commit()

@app.route("/", methods=["GET", "POST"])
def index():
    categories = Category.query.order_by(Category.name).all()

    if request.method == "POST":
        task = request.form.get("task")
        priority = request.form.get("priority")
        status = request.form.get("status")
        category_id = request.form.get("category_id")

        category = Category.query.get(category_id) if category_id else None
        if task and priority and category:
            new_task = Task(task=task, priority=priority, status=status, category=category)
            db.session.add(new_task)
            db.session.commit()
            flash("Task added successfully.")
        else:
            flash("Please provide a task, priority, and valid category.")

    todos = Task.query.order_by(Task.id).all()
    return render_template("index.html", todos=todos, categories=categories)

@app.route("/delete/<int:todo_index>", methods=["POST"])
def delete_todo(todo_index):
    todo = Task.query.get(todo_index)
    if todo:
        db.session.delete(todo)
        db.session.commit()
        flash("Task deleted successfully.")
    return redirect(url_for("index"))

@app.route("/edit/<int:todo_index>")
def edit_todo(todo_index):
    todo = Task.query.get(todo_index)
    if not todo:
        return redirect(url_for('index'))

    categories = Category.query.order_by(Category.name).all()
    return render_template('edit_todo.html', todo=todo, todo_index=todo_index, categories=categories)

@app.route("/update/<int:todo_index>", methods=["POST"])
def update_todo(todo_index):
    todo = Task.query.get(todo_index)
    if not todo:
        return redirect(url_for('index'))

    task = request.form.get('task')
    priority = request.form.get('priority')
    status = request.form.get('status')
    category_id = request.form.get('category_id')

    category = Category.query.get(category_id) if category_id else None
    if task and priority and category:
        todo.task = task
        todo.priority = priority
        todo.status = status
        todo.category = category
        db.session.commit()
        flash("Task updated successfully.")
    else:
        flash("Please provide a valid category when updating the task.")

    return redirect(url_for('index'))

@app.route("/todo/<int:todo_index>")
def todo_detail(todo_index):
    todo = Task.query.get(todo_index)
    if not todo:
        return redirect(url_for('index'))

    return render_template('todo_detail.html', todo=todo, todo_index=todo_index)

@app.route("/search")
def search():
    categories = Category.query.order_by(Category.name).all()
    search_params = {
        'task': request.args.get('task', '').strip(),
        'priority': request.args.get('priority', '').strip(),
        'category_id': request.args.get('category_id', '').strip(),
        'index': request.args.get('index', '').strip(),
    }

    query = Task.query
    if search_params['task']:
        query = query.filter(Task.task.ilike(f"%{search_params['task']}%"))

    if search_params['priority']:
        query = query.filter(Task.priority.ilike(search_params['priority']))

    if search_params['category_id']:
        try:
            category_id = int(search_params['category_id'])
            query = query.filter_by(category_id=category_id)
        except ValueError:
            query = query.filter(Task.id < 0)

    if search_params['index']:
        try:
            todo_id = int(search_params['index'])
            query = query.filter_by(id=todo_id)
        except ValueError:
            query = query.filter(Task.id < 0)

    filtered_todos = query.order_by(Task.id).all()
    total_todos = Task.query.count()

    return render_template(
        "search.html",
        filtered_todos=filtered_todos,
        total_todos=total_todos,
        search_params=search_params,
        categories=categories,
    )

if __name__ == "__main__":
    debug_flag = str(os.environ.get("DEBUG", False)).lower() in ("1", "true", "yes")
    app.run(debug=debug_flag)
