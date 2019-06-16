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
    listOfShortName = get_all_short_name_engineers()
    #listOfShortName = get_all_engineers()
    return render_template("layout.html.jinja2",
                           listOfShortName=listOfShortName)

@app.route('/<shortName>/affaire/<onglet>/')
def onglet_affaire(shortName,onglet):
    if (onglet == "missions"):
        listOfMissionsToAssign = ["misions"]
        return render_template("homepage_affaire_mission_grille.html.jinja2",
                               shortName=shortName
                               ,listOfMissionsToAssign=listOfMissionsToAssign
                               #,listOfMissionsAssigned=listOfMissionsAssigned
                               #,listOfMissionsClosed=listOfMissionsClosed
                               #,listOfAllMissions=listOfAllMissions
                                )
    if (onglet == "carrieres"):
        listOfEngineer = Ingenieur.query.all()
        return render_template("homepage_affaire_carriere_grille.html.jinja2",
                               shortName=shortName,
                               listOfEngineer=listOfEngineer)


@app.route('/<shortName>/etude/<onglet>/')
def onglet_etude(shortName, onglet):
    if (onglet == "postuler"):
        return render_template("homepage_etude_postuler_grille.html.jinja2",
                               shortName=shortName
                               #,listOfMissionsAvalable=listOfMissionsAvalable,
                               #listOfMissionsNotAvalable=listOfMissionsNotAvalable,
                               #listOfAllMissions=listOfAllMissions
                                )
    if (onglet == "suivi"):
        return render_template("homepage_etude_suivi_grille.html.jinja2",
                               shortName=shortName
                               #,listOfMissionsAccepted=listOfMissionsAccepted,
                               #listOfMissionsWaiting=listOfMissionsWaiting,
                               #listOfMissionsUnsuccessful=listOfMissionsUnsuccessful,
                               #listOfAllMissions=listOfAllMissions
                                )

@app.route('/<shortName>/affaire/missions/<mission>/')
def edit_mission(shortName, mission):
    # Il faut varier les trucs en sortie en fonction de la mission
    return render_template("homepage_affaire_mission_edit.html.jinja2",
                           shortName=shortName)

@app.route('/<shortName>/affaire/carrieres/<shortNameCarriere>/')
def carriere_vue(shortName,shortNameCarriere):
    engineerObserve = get_engineer_by_short_name(shortNameCarriere)
    return render_template("homepage_affaire_carriere_vue_grille.html.jinja2",
                           shortName=shortName,
                           engineerObserveFirstName=engineerObserve.prenom,
                           engineerObserveLastName=engineerObserve.nom_famille,
                           engineerObserveEmail=engineerObserve.email)

@app.route('/<shortName>/etude/postuler/<mission>/')
def postuler(shortName, mission):
    return render_template("homepage_etude_postuler_action_comp.html.jinja2",
                           shortName=shortName)

@app.errorhandler(404)
def error_page_404(error):
    #return render_template("404.html.jinja2")
    return render_template("404_glitch.html.jinja2")



if __name__ == '_main_':
    app.run()