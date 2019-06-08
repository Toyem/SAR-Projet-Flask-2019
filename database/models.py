from database.database import db


class Ingenieur(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom_court = db.Column(db.Text, unique=True)
    email = db.Column(db.Text, unique=True)
    prenom = db.Column(db.Text)
    nom_famille = db.Column(db.Text)
    site = db.Column(db.Text)
    taux_journalier = db.Column(db.Float)
    certifications = db.relationship('Certification', backref='ingenieur', lazy='dynamic')
    souhaits = db.relationship('Souhait', backref='ingenieur', lazy='dynamic')
    affectations = db.relationship('Affectation', backref='ingenieur', lazy='dynamic')
    responsabilites_missions = db.relationship('Mission', backref='responsable', lazy='dynamic')


class Competence(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(64), unique=True)

    certifications = db.relationship('Certification', backref='competence', lazy='dynamic')
    besoins = db.relationship('Besoin', backref='competence', lazy='dynamic')


class Certification(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    ingenieur_id = db.Column(db.Integer, db.ForeignKey('ingenieur.id'))
    competence_id = db.Column(db.Integer, db.ForeignKey('competence.id'))


class Besoin(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quantite_jour_homme = db.Column(db.Integer)

    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'))
    competence_id = db.Column(db.Integer, db.ForeignKey('competence.id'))


#
# class Mission(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     nom = db.Column(db.Text)
#     dateCreation = db.Column(db.Text) # date
#     description = db.Column(db.Text)
#     effectifMax = db.Column(db.Integer)
#     coutJournalier = db.Column(db.Float)

class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titre = db.Column(db.String(64), unique=True)

    description = db.Column(db.Text, unique=True)

    prix_vente = db.Column(db.Integer)

    besoins = db.relationship('Besoin', backref='mission', lazy='dynamic')
    affectations = db.relationship('Affectation', backref='mission', lazy='dynamic')

    responsable_id = db.Column(db.Integer, db.ForeignKey('ingenieur.id'))

    souhaits = db.relationship('Souhait', backref='mission', lazy='dynamic')


class Affectation(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    date_debut = db.Column(db.DateTime, nullable=False)
    date_fin = db.Column(db.DateTime, nullable=False)

    ingenieur_id = db.Column(db.Integer, db.ForeignKey('ingenieur.id'))
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'))


class Souhait(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ingenieur_id = db.Column(db.Integer, db.ForeignKey('ingenieur.id'))
    mission_id = db.Column(db.Integer, db.ForeignKey('mission.id'))
