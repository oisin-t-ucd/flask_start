from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

users = [
    {"name": "John", "age": 100, "job": "Teacher"},
    {"name": "Jane", "age": 100, "job": "Doctor"},
    {"name": "Dave", "age": 100, "job": "Engineer"},
]

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Get data from the form fields
        name = request.form.get("name")
        age = request.form.get("age")
        job = request.form.get("job")
        
        if name and age:
            users.append({"name": name, "age": int(age), "job": job})
    
    return render_template("index.html", users=users)


# New route to handle deletion
@app.route("/delete/<int:user_index>")
def delete_user(user_index):
    # Check if the index exists before trying to pop it
    if 0 <= user_index < len(users):
        users.pop(user_index)
    return redirect(url_for("index"))


@app.route("/<int:user_index>")
def user_profile(user_index):
    # Check if the user exists in our list
    if 0 <= user_index < len(users):
        user = users[user_index]
    else:
        user = None
    return render_template("user_profile.html", user=user)
    
    
@app.route("/about")
def about():
    return render_template("about.html")

if __name__ == "__main__":
    app.run(debug=True)