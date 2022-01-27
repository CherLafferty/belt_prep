from flask import render_template, redirect, request, session, flash
from flask_bcrypt import Bcrypt


from flask_app import app
from flask_app.models.user import User

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    if "uid" in session:
        return redirect("/dashboard")

    return render_template("index.html")


@app.route("/register", methods = ['POST'])
def register():
    if not User.register_validate(request.form):
        return redirect("/")

    hash_pwd = bcrypt.generate_password_hash(request.form['password'])
    user_data = {
        **request.form,
        "password": hash_pwd
    }
    user = User.create(user_data)
    print(user)
    session["uid"] = user

    return redirect("/dashboard")


@app.route("/login", methods = ['POST'])
def login():
    if not User.login_validate(request.form):
        return redirect("/")

    user = User.get_by_email({"email": request.form['email']})

    session['uid'] = user.id

    return redirect("/dashboard")


@app.route("/users")
def display_users():
    if "uid" not in session:
        return redirect("/")
    print(session["uid"])
    return render_template(
        "users.html",
        all_users = User.get_all(),
        user = User.get_by_id({"id": session['uid']})
    )


@app.route("/logout")
def logout():
    session.clear()

    return redirect("/")