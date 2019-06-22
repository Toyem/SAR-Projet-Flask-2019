from database.models import *
from app import db


# ----------------------------------------------------------
# ----------------------MISSIONS----------------------------
# ----------------------------------------------------------
def get_all_missions():
    return Mission.query.all()


def get_all_mission_ids():
    return [m.id for m in Mission.query.all()]


def get_mission_by_id(mission_id):
    return Mission.query.filter_by(id=mission_id).first()


def get_mission_by_titre(mission_titre):
    return Mission.query.filter_by(titre=mission_titre).first()


def get_postulant_by_mission(id_mission):
    return Souhait.query.filter_by(id_mission=id_mission).all().length


def get_participants_actuels_of_mission(mission_id):
    mission = get_mission_by_id(mission_id)
    id_inges = mission.affectations
    participants = [get_engineer_by_id(id) for id in list(id_inges)]
    return participants


# ----------------------------------------------------------
# ----------------------INGE ETUDE--------------------------
# ----------------------------------------------------------
def get_all_engineers():
    return Ingenieur.query.all()


def get_all_full_name_engineers(): #TO delete ?
    return Ingenieur.query(Ingenieur.prenom, Ingenieur.nom_famille).all()


def get_all_short_name_engineers():
    return [inge.nom_court for inge in get_all_engineers()]


def get_engineer_by_id(engineer_id):
    return Ingenieur.query.filter_by(id=engineer_id).first()


def get_engineer_by_nom_court(nom_court):
    return Ingenieur.query.filter_by(nom_court=nom_court).first()


def get_engineer_by_nom_prenom(nom, prenom):
    return Ingenieur.query.filter_by(nom=nom, prenom=prenom).first()


def get_mission_en_cours_of_inge(inge_id):
    inge = get_engineer_by_id(inge_id)
    id_missions = inge.affectations
    missions = [get_mission_by_id(id) for id in id_missions]
    missions_en_cours = []
    for m in missions:
        affectations = get_all_affectations_inge_mission(inge_id, m.id)
        ajouter = False
        if m.statut == "ouverte":
            for a in affectations:
                if a.date_fin >= db.func.now():
                   ajouter = True
        if ajouter:
            missions_en_cours.append(m)
    return missions_en_cours


def get_mission_termine_of_inge(inge_id): #verifier
    return [n for (n,) in Affectation.query.with_entities(Affectation.ingenieur_id).filter_by(ingenieur_id=inge_id)
        .filter(Affectation.date_fin > db.func.now()).all()]


def get_mission_en_attente_of_inge(inge_id): #verifier
    missions = []
    souhaits = [s.mission_id for s in Souhait.query.filter_by(ingenieur_id=inge_id).all()]
    for id in souhaits:
        missions.append(get_mission_by_id(id))
    return missions


def get_mission_possible_of_inge(inge_id):
    missions = Mission.query.filter_by(statut="ouverte").all()
    inge = get_engineer_by_id(inge_id)
    visibles = []
    for m in missions:
        cout_actuel = 0
        inges = get_participants_actuels_of_mission(m)
        for eid in inges:
            cout_actuel += get_engineer_by_id(eid).taux_journalier
        if cout_actuel + inge.taux_journalier < m.prix_vente:
            visibles.append(m)
    return visibles


# ----------------------------------------------------------
# ----------------------INGE AFFAIRE------------------------
# ----------------------------------------------------------
def get_all_engineers_affaire():
    return Ingenieur.query.filter_by(estCommercial=True).all()


def get_missions_a_affecter():
    missions_ids = db.session.query(Souhait.mission_id).distinct().all()
    missions_ids = [id for (id,) in missions_ids]
    missions = []
    for id in missions_ids:
        missions.append(get_mission_by_id(id))
    return missions


def get_missions_affecte():
    missions = [m for m in Mission.query.all() if m.statut == "ouverte" and len(list(m.souhaits)) == 0]
    return missions


def get_missions_close():
    return Mission.query.filter_by(statut='close').all()


# ----------------------------------------------------------
# ----------------------Competences-------------------------
# ----------------------------------------------------------
def get_competence_by_id(cid):
    return Competence.query.filter_by(id=cid).first()


def get_competence_of_mission(mission_id):
    compe_ids = [n for (n,) in Besoin.query.with_entities(Besoin.competence_id).filter_by(mission_id=mission_id).all()]
    competences = []
    for cid in compe_ids:
        competences.append(get_competence_by_id(cid))
    return competences


# ----------------------------------------------------------
# ----------------------A TRIER-----------------------------
# ----------------------------------------------------------
def get_all_affectations_inge_mission(inge_id, mission_id):
    return Affectation.query.filter_by(ingenieur_id=inge_id, mission_id=mission_id).all()


def add_skill_to_engineer(engineer_id, skill_id):
    engineer = Ingenieur.query.filter_by(id=engineer_id).first()
    skill = Competence.query.filter_by(id=skill_id).first()

    has_already_the_skill = skill.id in [skill_entry.skill.id for skill_entry in engineer.skill_entries]

    if not has_already_the_skill:
        new_skill_entry = Certification(engineer_id=engineer.id,
                                        skill_id=skill.id)
        db.session.add(new_skill_entry)
        db.session.commit()

        return True
    return False


def save_object_to_db(db_object):
    db.session.add(db_object)
    db.session.commit()


def remove_object_from_db(db_object):
    db.session.delete(db_object)
    db.session.commit()