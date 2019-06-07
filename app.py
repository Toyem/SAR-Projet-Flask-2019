from flask import Flask
from flask import render_template
from database.database import db, init_database

from database.models import Mission


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config["SECRET_KEY"] = "secret_key1234"  -> kesako


db.init_app(app) # (1) flask prend en compte la base de donnee
with app.test_request_context(): # (2) bloc execute a l'initialisation de Flask
    init_database()

def save_object_to_db(db_object):
    db.session.add(db_object)
    db.session.commit()

def remove_object_from_db(db_object):
    db.session.delete(db_object)
    db.session.commit()

def find_mission_by_id(id):
    return Mission.query.filter_by(id=id).first()

@app.route('/')
def layout():
    return render_template("layout.html.jinja2")


if __name__ == '__main__':
    app.run()

