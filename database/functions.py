from database.models import *
from database.database import db
from datetime import datetime


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
    return [get_engineer_by_id(s.ingenieur_id) for s in Souhait.query.filter_by(mission_id=id_mission).all()]


def get_participants_actuels_of_mission(mission_id):
    mission = get_mission_by_id(mission_id)
    id_inges = [a.ingenieur_id for a in list(mission.affectations)]
    participants = [get_engineer_by_id(id) for id in id_inges]
    return participants


def get_cout_of_mission(mission_id):
    coutTT = 0
    for inge in get_participants_actuels_of_mission(mission_id):
        coutTT += inge.taux_journalier
    return coutTT


def get_date_fin_date_fin_affectation(inge_id, mission_id):
    a = Affectation.query.filter_by(ingenieur_id=inge_id, mission_id=mission_id).first()
    return [("Date de début",a.date_debut),("Date de fin",a.date_fin)]


def get_date_candidat_souhait(inge_id, mission_id):
    s = Souhait.query.filter_by(ingenieur_id=inge_id, mission_id=mission_id).first()
    return [("Date de candidature",s.date_candidature)]


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


def get_mission_en_cours_of_inge(inge_id): #def de clore avec ouverte
    inge = get_engineer_by_id(inge_id)
    id_missions = [a.mission_id for a in list(inge.affectations)]
    missions = [get_mission_by_id(id) for id in id_missions]
    missions_en_cours = []
    for m in missions:
        affectations = get_all_affectations_inge_mission(inge_id, m.id)
        ajouter = False
        if m.statut == "ouverte":
            for a in affectations:
                if a.date_fin >= datetime.now():
                   ajouter = True
        if ajouter:
            missions_en_cours.append(m)
    return missions_en_cours


def get_mission_termine_of_inge(inge_id): #def de clore avec ouverte
    inge = get_engineer_by_id(inge_id)
    id_missions = [a.mission_id for a in list(inge.affectations)]
    missions = [get_mission_by_id(id) for id in id_missions]
    missions_termines = []
    for m in missions:
        affectations = get_all_affectations_inge_mission(inge_id, m.id)
        ajouter = True
        if m.statut == "ouverte":
            for a in affectations:
                if a.date_fin >= datetime.now():
                   ajouter = False
        if ajouter:
            missions_termines.append(m)
    return missions_termines


def get_mission_en_attente_of_inge(inge_id):
    souhaits = [s.mission_id for s in Souhait.query.filter_by(ingenieur_id=inge_id).all()]
    missions = [get_mission_by_id(id) for id in souhaits]
    return missions


def get_mission_possible_of_inge(inge_id):
    missions = Mission.query.filter_by(statut="ouverte").all()
    inge = get_engineer_by_id(inge_id)
    visibles = []
    for m in missions:
        if not ((inge in get_participants_actuels_of_mission(m.id)) or (inge in get_postulant_by_mission(m.id))):
            cout_actuel = 0
            participants = get_participants_actuels_of_mission(m.id)
            for p in participants:
                cout_actuel += p.taux_journalier
            if cout_actuel + inge.taux_journalier < m.prix_vente:
                visibles.append(m)
    return visibles


# ----------------------------------------------------------
# ----------------------INGE AFFAIRE------------------------
# ----------------------------------------------------------
def get_all_engineers_affaire():
    return Ingenieur.query.filter_by(estCommercial=True).all()


def get_missions_a_affecter(): #TODO
    missions_ids = [s.mission_id for s in Souhait.query.all()]
    missions = set()
    for id in missions_ids:
        missions.add(get_mission_by_id(id))
    return missions


def get_missions_affecte():
    missions = [m for m in Mission.query.all() if m.statut == "ouverte" and len(list(m.souhaits)) == 0]
    return missions


def get_missions_close():
    return Mission.query.filter_by(statut='close').all()


# ----------------------------------------------------------
# ----------------------Competences-------------------------
# ----------------------------------------------------------
def get_all_competence():
    return Competence.query.all()


def get_competence_by_id(cid):
    return Competence.query.filter_by(id=cid).first()


def get_competence_of_mission(mission_id):
    mission = get_mission_by_id(mission_id)
    compe_ids = [b.competence_id for b in list(mission.besoins)]
    compes = [Competence.query.filter_by(id=cid).first() for cid in compe_ids]
    return compes


# ----------------------------------------------------------
# ----------------------A TRIER-----------------------------
# ----------------------------------------------------------
def get_all_affectations_inge_mission(inge_id, mission_id):
    return Affectation.query.filter_by(ingenieur_id=inge_id, mission_id=mission_id).all()


def get_lvl_compe_inge(inge_id, compe_id):
    certif = Certification.query.filter_by(ingenieur_id=inge_id, competence_id=compe_id).first()
    if certif is None:
        lvl = 0
    else:
        lvl = certif.niveau
    return lvl


def get_couple_compe_lvl_of_mission_inge(mission_id,inge_id):
    competences = get_competence_of_mission(mission_id)
    list_couple = []
    for c in competences:
        lvl = get_lvl_compe_inge(inge_id, c.id)
        list_couple.append([c, lvl])
    return list_couple


# ----------------------------------------------------------
# ----------------------Edition-----------------------------
# ----------------------------------------------------------
def update_competence_of_inge(inge_id, liste_comp):
    for (cid, lvl) in liste_comp:
        certif = Certification.query.filter_by(ingenieur_id=inge_id, competence_id=cid).first()
        if certif is None:
            certif = Certification(ingenieur_id=inge_id, competence_id=cid, niveau=lvl)
        else:
            certif.niveau = lvl
        save_object_to_db(certif)


def postuler(inge_id, mission_id, liste_comp):
    update_competence_of_inge(inge_id, liste_comp)
    new_souhait = Souhait(date_candidature=datetime.now(), mission_id=mission_id, ingenieur_id=inge_id)
    save_object_to_db(new_souhait)


def update_besoin(mission_id, compe_list):
    for b in Besoin.query.filter_by(mission_id=mission_id).all():
        remove_object_from_db(b)
    for cid in compe_list:
        new_b = Besoin(mission_id=mission_id, competence_id=cid)
        save_object_to_db(new_b)


def new_mission(inge_id):

    date_now = datetime.now()
    date_now.strftime('%Y-%m-%d %H:%M:%S')
    new_m = Mission(statut="ouverte", date_creation=date_now, responsable_id=inge_id)
    save_object_to_db(new_m)
    return new_m


def clore(mission_id): #todo
    return


def save_object_to_db(db_object):
    db.session.add(db_object)
    db.session.commit()


def remove_object_from_db(db_object):
    db.session.delete(db_object)
    db.session.commit()