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


@app.route('/')
# API page acceuil
def layout():
    listOfShortName = get_all_short_name_engineers()
    # listOfShortName = get_all_engineers()
    return render_template("layout.html.jinja2",
                           listOfShortName=listOfShortName)

@app.route('/<shortName>/affaire/missions/<etat>/')
# API onglet missions d'un ingé d'affaire
def onglet_affaire_mission(shortName, etat):
    listOfMissionsToAssign = get_missions_a_affecter()
    listOfMissionsAssigned = get_missions_affecte()
    listOfMissionsClosed = get_missions_close()
    listOfAllMissions = get_all_missions()
    print(etat)
    if (etat == "aAffecter"):
        listToShow = listOfMissionsToAssign
    elif (etat == "affectees"):
        listToShow = listOfMissionsAssigned
    elif (etat == "closes"):
        listToShow = listOfMissionsClosed
    elif (etat == "toutes"):
        listToShow = listOfAllMissions
    else:
        error_page_404("tab doesn't exist - onglet_affaire_mission")
    return render_template("homepage_affaire_mission_grille.html.jinja2"
                           , shortName=shortName
                           , listToShow=listToShow
                           , listOfMissionsToAssignLength=len(listOfMissionsToAssign)
                           , listOfMissionsAssignedLength=len(listOfMissionsAssigned)
                           , listOfMissionsClosedLength=len(listOfMissionsClosed)
                           , listOfAllMissionsLength=len(listOfAllMissions)
                           )


@app.route('/<shortName>/affaire/missions/vue/<mission_name>/')
# API onglet missions d'un ingé d'affaire
def onglet_affaire_mission_vue(shortName, mission_name):
    mission = get_mission_by_titre(mission_name)
    return render_template("homepage_affaire_mission_vue.html.jinja2"
                           , shortName=shortName
                           , mission=mission
                           )

@app.route('/<shortName>/affaire/missions/vue/<mission>/edit/')
# API pour voir mission à postuler
def affaire_mission_edit(shortName, mission):
    return render_template("homepage_affaire_mission_edit.html.jinja2"
                           , shortName=shortName
                           , mission=mission
                           )

@app.route('/<shortName>/affaire/carrieres/')
# API onglet carrière d'un ingé d'affaire
def onglet_affaire_carriere(shortName):
    listOfEngineer = Ingenieur.query.all()
    return render_template("homepage_affaire_carriere_grille.html.jinja2",
                           shortName=shortName,
                           listOfEngineer=listOfEngineer)


@app.route('/<shortName>/affaire/carrieres/<shortNameCarriere>/<etat>/')
# API pour voir les carrières des ingés
def carriere_vue(shortName, shortNameCarriere, etat):
    engineerObserve = get_engineer_by_nom_court(shortNameCarriere)
    listOfMissionsOnGoing = get_mission_en_cours_of_inge(engineerObserve.id)
    listOfMissionsWaiting = get_mission_en_attente_of_inge(engineerObserve.id)
    listOfMissionsClosed = get_mission_termine_of_inge(engineerObserve.id)
    if (etat == "enCours"):
        listToShow = listOfMissionsOnGoing
    elif (etat == "termine"):
        listToShow = listOfMissionsWaiting
    elif (etat == "enAttente"):
        listToShow = listOfMissionsClosed
    else:
        error_page_404("tab doesn't exist")
    return render_template("homepage_affaire_carriere_vue_grille.html.jinja2",
                           shortName=shortName,
                           etat=etat,
                           engineerObserveFirstName=engineerObserve.prenom,
                           engineerObserveLastName=engineerObserve.nom_famille,
                           engineerObserveEmail=engineerObserve.email,
                           shortNameCarriere=shortNameCarriere
                           , listOfMissionsOnGoingLength=len(listOfMissionsOnGoing)
                           , listOfMissionsWaitingLength=len(listOfMissionsWaiting)
                           , listOfMissionsClosedLength=len(listOfMissionsClosed)
                           , listToShow=listToShow)

# ----------------------------------------------------------
# ----------------------------------------------------------
# ----------------------------------------------------------


@app.route('/<shortName>/etude/postuler/<etat>/')
# API onglet soit postuler d'un ingé d'étude
def onglet_etude(shortName, etat):
    engineerObserve = get_engineer_by_nom_court(shortName)
    listOfMissionsAvalable = get_mission_possible_of_inge(engineerObserve.id)
    listOfMissionsGoingOn = get_mission_en_cours_of_inge(engineerObserve.id)
    listOfMissionsWaiting = get_mission_en_attente_of_inge(engineerObserve.id)
    listOfMissionsClosed = get_mission_termine_of_inge(engineerObserve.id)
    if (etat == "disponibles"):
        listToShow = listOfMissionsAvalable
    elif (etat == "enAttente"):
        listToShow = listOfMissionsGoingOn
    elif (etat == "enCours"):
        listToShow = listOfMissionsWaiting
    elif (etat == "termine"):
        listToShow = listOfMissionsClosed
    else:
        error_page_404("tab doesn't exist")
    return render_template("homepage_etude_postuler_grille.html.jinja2",
                           shortName=shortName
                           , etat=etat
                           , listOfMissionsAvalableLength=len(listOfMissionsAvalable)
                           , listOfMissionsWaitingLength=len(listOfMissionsWaiting)
                           , listOfMissionsGoingOnLength=len(listOfMissionsGoingOn)
                           , listOfMissionsClosedLength=len(listOfMissionsClosed)
                           , listToShow=listToShow
                           )


# if (onglet == "suivi"):
#    return render_template("homepage_etude_suivi_grille.html.jinja2",
#                           shortName=shortName
#                           #,listOfMissionsAccepted=listOfMissionsAccepted,
#                           #listOfMissionsWaiting=listOfMissionsWaiting,
#                           #listOfMissionsUnsuccessful=listOfMissionsUnsuccessful,
#                           #listOfAllMissions=listOfAllMissions
#                           )

#@app.route('/<shortName>/affaire/missions/<etat>/<mission>/')
# API pour édit une mission
#def edit_mission(shortName, mission):
#    # Il faut varier les trucs en sortie en fonction de la mission
#    return render_template("homepage_affaire_mission_edit.html.jinja2",
#                           shortName=shortName)

@app.route('/<shortName>/etude/postuler/<etat>/<mission>/')
# API pour voir mission à postuler
def postuler(shortName, mission, etat):
    return render_template("homepage_etude_postuler_action_comp.html.jinja2"
                           ,shortName=shortName
                           ,etat=etat
                           ,mission=mission
                           )

@app.errorhandler(404)
def error_page_404(error):
    # return render_template("404.html.jinja2")
    return render_template("404_glitch.html.jinja2")



if __name__ == '_main_':
    app.run()
