import os
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for, session

# load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-key")

DEFAULT_USERS = [
    {"name": "John", "age": 100, "job": "Teacher"},
    {"name": "Jane", "age": 100, "job": "Doctor"},
    {"name": "Dave", "age": 100, "job": "Engineer"},
]

@app.route("/", methods=["GET", "POST"])
def index():
    # print(undefined)
    if 'users' not in session:
        session['users'] = DEFAULT_USERS.copy()
    
    if request.method == "POST":
        # Get data from the form fields
        name = request.form.get("name")
        age = request.form.get("age")
        job = request.form.get("job")
        
        if name and age:
            users_list = session['users']
            users_list.append({"name": name, "age": int(age), "job": job})
            session['users'] = users_list
    
    return render_template("indexa.html", users=session['users'])


# New route to handle deletion
@app.route("/delete/<int:user_index>", methods=["POST"])
def delete_user(user_index):
    if 'users' in session and 0 <= user_index < len(session['users']):
        users_list = session['users']
        users_list.pop(user_index)
        session['users'] = users_list
    return redirect(url_for("index"))


@app.route("/<int:user_index>")
def user_profile(user_index):
    if 'users' in session and 0 <= user_index < len(session['users']):
        user = session['users'][user_index]
    else:
        user = None
    return render_template("user_profile.html", user=user)


@app.route("/edit/<int:user_index>")
def edit_user(user_index):
    if 'users' not in session or not (0 <= user_index < len(session['users'])):
        return redirect(url_for('index'))

    user = session['users'][user_index]
    return render_template('edit_user.html', user=user, user_index=user_index)


@app.route("/update/<int:user_index>", methods=["POST"])
def update_user(user_index):
    if 'users' not in session or not (0 <= user_index < len(session['users'])):
        return redirect(url_for('index'))

    name = request.form.get('name')
    age = request.form.get('age')
    job = request.form.get('job')

    if name and age:
        users_list = session['users']
        users_list[user_index] = {"name": name, "age": int(age), "job": job}
        session['users'] = users_list

    return redirect(url_for('index'))


@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)
    debug_flag = str(os.environ.get("DEBUG", "False")).lower() in ("1", "true", "yes")