from database.models import *
from app import db


def get_all_engineers():
    return Ingenieur.query.all()

def get_all_name_engineers() :
    return Ingenieur.query(Ingenieur.nom_famille).all().first()


def get_engineer_by_id(engineer_id):
    return Ingenieur.query.filter_by(id=engineer_id).first()


def get_engineers_in_site(site_name):
    return Ingenieur.query.filter_by(site=site_name).all()


def add_skill_to_engineer(engineer_id, skill_id):
    engineer = Ingenieur.query.filter_by(id=engineer_id).first()
    skill = Competence.query.filter_by(id=skill_id).first()

    has_already_the_skill = skill.id in [skill_entry.skill.id for skill_entry in engineer.skill_entries]

    if not has_already_the_skill:
        new_skill_entry = database.models.ComptenceIndividuelle(engineer_id=engineer.id,
                                                                skill_id=skill.id)
        db.session.add(new_skill_entry)
        db.session.commit()

        return True
    return False
