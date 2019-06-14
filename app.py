from flask import Flask
from flask import render_template
from database.database import db, init_database

from database.models import *
from database.functions import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SECRET_KEY"] = "secret_key1234"  -> kesako


db.init_app(app)  # (1) flask prend en compte la base de donnee
with app.test_request_context():  # (2) bloc execute a l'initialisation de Flask
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


@app.route('/Name/<classe>')
def classe(classe):
    if(classe == "affaire"):
        return render_template("homepage_affaire_mission_grille.html.jinja2", classe=classe)
    if (classe == "etude"):
        return render_template("homepage_etude_postuler_grille.html.jinja2", classe=classe)

@app.route('/Name/affaire/<onglet>')
def onglet_affaire(onglet):
    if (onglet == "missions"):
        return render_template("homepage_affaire_mission_grille.html.jinja2")
    if (onglet == "carrieres"):
        return render_template("homepage_affaire_carriere_grille.html.jinja2")


@app.route('/Name/etude/<onglet>')
def onglet_etude(onglet):
    if (onglet == "postuler"):
        return render_template("homepage_etude_postuler_grille.html.jinja2")
    if (onglet == "suivi"):
        return render_template("homepage_etude_suivi_grille.html.jinja2")

@app.route('/Name/affaire/missions/<mission>')
def edit_mission(mission):
    # Il faut varier les trucs en sortie en fonction de la mission
    return render_template("homepage_affaire_mission_edit.html.jinja2")

@app.route('/Name/affaire/carriere/<name>')
def carriere_vue(name):
    return render_template("homepage_affaire_carriere_vue_grille.html.jinja2")

@app.route('/Name/etude/postuler/<mission>')
def postuler(mission):
    return render_template("homepage_etude_postuler_action_comp.html.jinja2")


if __name__ == '_main_':
    app.run()