#packages
from flask import Flask, render_template, redirect, url_for, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy

#configuration
app = Flask('app')
app.secret_key = "hello"
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(days=7)

#database
db = SQLAlchemy(app)


class users(db.Model):
  _id = db.Column("id", db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100))
  email = db.Column(db.String(150))

  def __init__(self, name, email):
    self.name = name
    self.email = email

#routes
@app.route('/')
def hello():
  flash("hello", "info")
  return render_template('index.html')


@app.route('/view')
def view():
  return render_template('view.html', values=users.query.all())


@app.route('/login', methods=['POST', 'GET'])
def login():
  user = None
  if request.method == "POST":
    session.permanent = True
    user = request.form["name"]
    session["user"] = user
    found_user = users.query.filter_by(name=user).first()
    if found_user:
      session["email"] = found_user.email
    else:
      usr = users(user, "")
      db.session.add(usr)
      db.session.commit()

    flash("Login Successful !")
    return redirect(url_for("user"))
  else:
    if user in session:
      flash("Already Logged in !")
      return redirect(url_for("user"))
    return render_template("login.html")


@app.route('/user')
def user():
  email = None
  user = None
  if "user" in session:
    user = session["user"]
    if request.method == "POST":
      email = request.form["email"]
      session["email"] = email
    else:
      if email in session:
        session["email"] = email
        found_user = users.query.filter_by(name=user).first()
        found_user.email = email
        db.session.commit()
        flash("Email was saved !")
    return render_template("user.html", email=email)
  else:
    return render_template(url_for("login"))


@app.route("/logout")
def logout():
  session.pop("user", None)
  session.pop("email", None)
  return redirect(url_for("login"))

app.run(host='0.0.0.0', port=8080, debug=True)
