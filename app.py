from flask import Flask
from flask import render_template
#from database.database import db, init_database

#from database.models import *
#from database.functions import *


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#app.config["SECRET_KEY"] = "secret_key1234"  -> kesako


#db.init_app(app) # (1) flask prend en compte la base de donnee
#with app.test_request_context(): # (2) bloc execute a l'initialisation de Flask
#    init_database()

@app.route('/')
def layout():
    return render_template("layout.html.jinja2")

@app.route('/Name/<int:index>/<classe>')
def classe(index, classe):
    if(classe == "affaire"):
        return render_template("homepage_affaire_carriere_grille.html.jinja2")
    if (classe == "etude"):
        return render_template("homepage_etude_postuler_grille.html.jinja2")

@app.route('/affaire/<onglet>') #On ne réccupère plus le nom du mec dans l'url !!!!
def onglet_affaire(onglet):
    if (onglet == "missions"):
        return render_template("homepage_affaire_carriere_grille.html.jinja2")
    if (onglet == "carrieres"):
        return render_template("homepage_affaire_mission_grille.html.jinja2")

@app.route('/etude/<onglet>') #On ne réccupère plus le nom du mec dans l'url !!!!
def onglet_etude(onglet):
    if (onglet == "postuler"):
        return render_template("homepage_etude_postuler_grille.html.jinja2")
    if (onglet == "suivi"):
        return render_template("homepage_etude_suivi_grille.html.jinja2")

@app.route('/Rene_etude')
def Rene_etude():
    return render_template("homepage_etude_postuler_grille.html.jinja2")


if __name__ == '__main__':
    app.run()

