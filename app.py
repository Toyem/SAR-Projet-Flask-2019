from flask import Flask
from flask import render_template
from database.database import init_database
import flask
from database.functions import *

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database/database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.config["SECRET_KEY"] = "secret_key1234"  -> kesako


db.init_app(app)  # (1) flask prend en compte la base de donnee
with app.test_request_context():  # (2) bloc execute a l'initialisation de Flask
    init_database()


# ------------------------------------------
# ---------Page Accueil---------------------
# ------------------------------------------

@app.route('/')
# API page accueil
def layout():
    listOfEngineer = get_all_engineers()
    listOfAffair = get_all_engineers_affaire()
    return render_template("layout.html.jinja2",
                           listOfEngineer=listOfEngineer,
                           listOfAffair=listOfAffair)


# ------------------------------------------
# ---------Ingé AFFAIRE---------------------
# ------------------------------------------

@app.route('/<id>/affaire/missions/<etat>/')
# API onglet missions d'un ingé d'affaire
def onglet_affaire_mission(id, etat):
    listOfMissionsToAssign = get_missions_a_affecter()
    listOfMissionsAssigned = get_missions_affecte()
    listOfMissionsClosed = get_missions_close()
    listOfAllMissions = get_all_missions()
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
                           , etat=etat
                           , id=id
                           , listToShow=listToShow
                           , listOfMissionsToAssignLength=len(listOfMissionsToAssign)
                           , listOfMissionsAssignedLength=len(listOfMissionsAssigned)
                           , listOfMissionsClosedLength=len(listOfMissionsClosed)
                           , listOfAllMissionsLength=len(listOfAllMissions)
                           )


@app.route('/delete_mission/<id>/<missionId>/')
def delete_mission(id, missionId):
    mission = get_mission_by_id(missionId)
    remove_object_from_db(mission)
    return flask.redirect(flask.url_for("onglet_affaire_mission", id=id, etat="aAffecter"))


@app.route('/<id>/affaire/missions/vue/<missionId>/')
# API onglet missions d'un ingé d'affaire
def affaire_mission_vue(id, missionId):
    mission = get_mission_by_id(missionId)
    competences = get_competence_of_mission(missionId)
    equipeForme = get_participants_actuels_of_mission(missionId)
    postulants = get_postulant_by_mission(missionId)
    coutTT = get_cout_of_mission(missionId)
    return render_template("homepage_affaire_mission_vue.html.jinja2"
                           , id=id
                           , mission=mission
                           , competences=competences
                           , equipeForme=equipeForme
                           , postulants=postulants
                           , coutTT=coutTT
                           )


@app.route('/clore_mission/<id>/<missionId>/')
def clore_mission(id, missionId):
    clore_mission_in_bd(missionId)
    return flask.redirect(flask.url_for("onglet_affaire_mission", id=id, etat="aAffecter"))


@app.route('/<id>/affaire/missions/vue/<missionId>/edit/')
def affaire_mission_edit_get_mission(id, missionId):
    print("passage 1")
    # API pour voir mission à postuler
    mission = get_mission_by_id(missionId)
    is_new_mission = False
    return affaire_mission_edit(id, mission, is_new_mission, "")


@app.route('/<id>/affaire/missions/vue/<missionId>/edit/')
def affaire_mission_edit(id, mission, is_new_mission, error):
    print("passage 2")
    # competences = get_competence_of_mission(mission.id)
    allCompetences = get_all_competence()
    competencesMission = get_competence_of_mission(mission.id)

    return render_template("homepage_affaire_mission_edit.html.jinja2"
                           , id=id
                           , mission=mission
                           , competences=allCompetences
                           , competencesMission=competencesMission
                           , is_new_mission=is_new_mission
                           , error=error
                           )


@app.route('/<id>/affaire/carrieres/')
# API onglet carrière d'un ingé d'affaire
def onglet_affaire_carriere(id):
    listOfEngineer = get_all_engineers()
    return render_template("homepage_affaire_carriere_grille.html.jinja2",
                           id=id,
                           listOfEngineer=listOfEngineer)


@app.route('/<id>/affaire/carrieres/<idCarriere>/<etat>/')
# API pour voir les carrières des ingés
def carriere_vue(id, idCarriere, etat):
    engineerObserve = get_engineer_by_id(idCarriere)
    listOfMissionsOnGoing = get_mission_en_cours_of_inge(idCarriere)
    listOfMissionsWaiting = get_mission_en_attente_of_inge(idCarriere)
    listOfMissionsClosed = get_mission_termine_of_inge(idCarriere)
    if (etat == "enCours"):
        listToShow = listOfMissionsOnGoing
    elif (etat == "termine"):
        listToShow = listOfMissionsClosed
    elif (etat == "enAttente"):
        listToShow = listOfMissionsWaiting
    else:
        error_page_404("tab doesn't exist")
    return render_template("homepage_affaire_carriere_vue_grille.html.jinja2",
                           id=id,
                           etat=etat,
                           engineerObserveFirstName=engineerObserve.prenom,
                           engineerObserveLastName=engineerObserve.nom_famille,
                           engineerObserveEmail=engineerObserve.email,
                           idCarriere=idCarriere
                           , listOfMissionsOnGoingLength=len(listOfMissionsOnGoing)
                           , listOfMissionsWaitingLength=len(listOfMissionsWaiting)
                           , listOfMissionsClosedLength=len(listOfMissionsClosed)
                           , listToShow=listToShow)


# ---------------------
# --------POST---------
# ---------------------

@app.route("/process_form_acceptation/<id>/<missionId>/", methods=["POST"])
def process_form_acceptation(id, missionId):
    return flask.redirect(flask.url_for("affaire_mission_vue", id=id, missionId=missionId))


@app.route("/process_form_data/<id>/<missionId>/<is_new_mission>/", methods=["POST"])
def process_form_data(id, missionId, is_new_mission):
    mission = get_mission_by_id(missionId)
    try:
        mission.titre = flask.request.form["foo_titre"]
        mission.description = flask.request.form["mission_description"]
        mission.effectifs_max = int(flask.request.form["mission_effectif_max"])
        mission.prix_vente = float(flask.request.form["mission_prix_vente"])
        datetime_object = datetime.strptime(flask.request.form["mission_date_creation"], '%Y-%m-%d %H:%M:%S')
        mission.date_creation = datetime_object
        listOfAllFormName = flask.request.form.to_dict().keys()
        listOfCompetencesEdit = []
        for formName in listOfAllFormName:
            if formName[:11] == "competence_":
                listOfCompetencesEdit.append(formName[11:])
        update_besoin(mission.id, listOfCompetencesEdit)
        save_object_to_db(mission)
        error = ""
        return flask.redirect(flask.url_for("affaire_mission_vue", id=id, missionId=mission.id))
    except:
        error = "Un des champ est mal rempli"
        return affaire_mission_edit(id, mission, is_new_mission, error)
    # mission.effectifs_max = int(flask.request.form["mission_effectif_max"])
    # mission.prix_vente = float(flask.request.form["mission_prix_vente"])
    #
    # datetime_object = datetime.strptime(flask.request.form["mission_date_creation"], '%Y-%m-%d %H:%M:%S')
    # mission.date_creation = datetime_object
    # listOfAllFormName = flask.request.form.to_dict().keys()
    # listOfCompetencesEdit=[]
    # for formName in listOfAllFormName:
    #     if formName[:11] == "competence_":
    #         listOfCompetencesEdit.append(formName[11:])
    # update_besoin(mission.id,listOfCompetencesEdit)
    # save_object_to_db(mission)


@app.route('/<id>/affaire/missions/vue/0/edit/', methods=["POST"])
def process_new_mission(id):
    print("is ok ?")
    mission = new_mission(id)
    is_new_mission = True
    # mission = get_mission_by_id(mission_id)
    return affaire_mission_edit(id, mission, is_new_mission, "")


# ----------------------------------------------------
# ---------------------Ingé ETUDE---------------------
# ----------------------------------------------------


@app.route('/<id>/etude/postuler/<etat>/')
# API onglet soit postuler d'un ingé d'étude
def onglet_etude(id, etat):
    engineerObserve = get_engineer_by_id(id)
    listOfMissionsAvalable = get_mission_possible_of_inge(id)
    listOfMissionsGoingOn = get_mission_en_cours_of_inge(id)
    listOfMissionsWaiting = get_mission_en_attente_of_inge(id)
    listOfMissionsClosed = get_mission_termine_of_inge(id)
    if (etat == "disponibles"):
        listToShow = listOfMissionsAvalable
    elif (etat == "enAttente"):
        listToShow = listOfMissionsWaiting
    elif (etat == "enCours"):
        listToShow = listOfMissionsGoingOn
    elif (etat == "termine"):
        listToShow = listOfMissionsClosed
    else:
        error_page_404("tab doesn't exist")
    return render_template("homepage_etude_postuler_grille.html.jinja2",
                           id=id
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

# @app.route('/<shortName>/affaire/missions/<etat>/<mission>/')
# API pour édit une mission
# def edit_mission(shortName, mission):
#    # Il faut varier les trucs en sortie en fonction de la mission
#    return render_template("homepage_affaire_mission_edit.html.jinja2",
#                           shortName=shortName)

@app.route('/<id>/etude/postuler/<etat>/vue/<missionId>/')
# API pour voir mission à postuler
def postuler_vue(id, missionId, etat):
    mission = get_mission_by_id(missionId)
    competences = get_competence_of_mission(missionId)
    if (etat == "disponibles"):
        dates = []
        enable = ""
    elif (etat == "enAttente"):
        dates = get_date_candidat_souhait(id, missionId)
        enable = "disabled"
    elif (etat == "enCours" or etat == "termine"):
        dates = get_date_fin_date_fin_affectation(id, missionId)
        enable = "disabled"
    else:
        error_page_404("tab doesn't exist")
    return render_template("homepage_etude_postuler_vue.html.jinja2"
                           , etat=etat
                           , id=id
                           , mission=mission
                           , competences=competences
                           , dates=dates
                           , enable=enable
                           )


@app.route('/<id>/etude/postuler/<etat>/vue/<missionId>/edit/')
# API pour voir mission à postuler
def postuler_edit(id, missionId, etat):
    # if formulaireSuccess != True:
    #    formulaireSuccess = False
    mission = get_mission_by_id(missionId)
    coupleCompetencesLvl = get_couple_compe_lvl_of_mission_inge(missionId, id)
    return render_template("homepage_etude_postuler_action_comp.html.jinja2"
                           , etat=etat
                           , id=id
                           , mission=mission
                           , coupleCompetencesLvl=coupleCompetencesLvl
                           )


# ---------------------
# --------POST---------
# ---------------------

@app.route("/process_form_postuler/<id>/<missionId>/<etat>", methods=["POST"])
def process_form_postuler(id, missionId, etat):
    listOfAllFormName = flask.request.form.to_dict().keys()
    listeOfTuplesCompetencesLevel = []
    for formName in listOfAllFormName:
        if formName[:11] == "competence_":
            listeOfTuplesCompetencesLevel.append((formName[11:], flask.request.form[formName]))
    postuler(id, missionId, listeOfTuplesCompetencesLevel)
    formulaireSuccess = True

    return flask.redirect(flask.url_for("onglet_etude", id=id, etat=etat))


# ----------------------------------------------------
# --------------------------Error---------------------
# ----------------------------------------------------

@app.errorhandler(404)
def error_page_404(error):
    # return render_template("404.html.jinja2")
    return render_template("404_glitch.html.jinja2")


if __name__ == '_main_':
    app.run()
