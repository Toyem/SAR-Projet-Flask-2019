from database.models import *
from app import db

# GET ALL
def get_all_missions():
    return Mission.query.all()

def get_all_engineers():
    return Ingenieur.query.all()


# GET ALL Specific
def get_missions_a_affecter(): #doit être filtré par le prix (par exemple)
    return Mission.query.all()


def get_missions_affecte(): #doit être filtré par les souhaits
    return Affectation.query.all()


def get_all_short_name_engineers():
    return [n for (n,) in db.session.query(Ingenieur.nom_court).all()]


def get_missions_close():
    return Mission.query.filter_by(statut='close').all()


def get_all_engineers_affaire():
    return Ingenieur.query.filter_by(estCommercial=True).all()


def get_all_short_name_engineers():
    return Ingenieur.query(Ingenieur.nom_court).all()


def get_all_full_name_engineers():
    return Ingenieur.query(Ingenieur.prenom, Ingenieur.nom_famille).all()


def get_engineers_in_site(site_name):
    return Ingenieur.query.filter_by(site=site_name).all()


# GET BY (first)
def get_mission_by_id(mission_id):
    return Mission.query.filter_by(id=mission_id).first()


def get_engineer_by_id(engineer_id):
    return Ingenieur.query.filter_by(id=engineer_id).first()

def get_engineer_by_short_name(engineer_short_name):
    return Ingenieur.query.filter_by(nom_court=engineer_short_name).first()


def get_engineer_by_nom_court(nom_court):
    return Ingenieur.query.filter_by(nom_court=nom_court).first()


def get_engineer_by_nom_prenom(nom, prenom):
    return Ingenieur.query.filter_by(nom=nom, prenom=prenom).first()


# ADD
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
