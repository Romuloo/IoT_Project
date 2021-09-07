from functools import wraps

from flask import Flask, render_template, url_for, redirect, session, flash
from flask_dance.contrib.facebook import make_facebook_blueprint, facebook
import json

from flask_sqlalchemy import SQLAlchemy

alive = 0
data = {}

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pass?@localhost/sd3a_iot'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from . import myDB

# Facebook id and secret
facebookID = "550486829613429"
facebookSecret = "3124cbe71e7ed076604ae7f8c5baf380"

facebook_blueprint = make_facebook_blueprint(client_id=facebookID, client_secret=facebookSecret)
app.register_blueprint(facebook_blueprint, url_prefix="/facebook_login")


@app.route("/facebook_login")
def facebook_login():
    if not facebook.authorized:
        print("Not authorized. Redirecting ...")
        return redirect(url_for('facebook.login'))

    account_info = facebook.get("/me")
    if account_info.ok:
        print("Access_token: ", facebook.access_token)
        me = account_info.json()
        session['logged_in'] = True
        session['facebook_token'] = facebook.access_token
        session['user'] = me['name']
        session['user_id'] = me['id']
        return redirect(url_for('main'))

def clear_user_session():
    session['logged_in'] = None
    session['facebook_token'] = None
    session['user'] = None
    session['user_id'] = None


@app.route('/')
def login():
    clear_user_session()
    return render_template("login.html")


@app.route('/logout')
def logout():
    myDB.user_logout(session['user_id'])
    clear_user_session()
    flash("You just logged out")
    return redirect(url_for("login"))


def LoginRequired(f):
    @wraps(f)
    def wrapper(*args, **kargs):
        if session['logged_in']:
            return f(*args, **kargs)
        flash("Please login first")
        return redirect(url_for("login"))
    return wrapper


@app.route("/main")
@LoginRequired
def main():
    flash(session["user"])
    myDB.add_user_and_login(session['user'], int(session['user_id']))
    myDB.view_all()
    return render_template("index.html")


@app.route("/keep_alive", methods=["GET"])
def keep_alive():
    global alive, data
    alive += 1
    keep_alive_count = str(alive)
    data['keep_alive'] = keep_alive_count
    parsed_json = json.dumps(data)
    print(str(parsed_json))
    return str(parsed_json)


if __name__ == '__main__':
    app.run()


