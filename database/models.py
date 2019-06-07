from database.database import db


class Mission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.Text)
    dateCreation = db.Column(db.Text) // date
    description = db.Column(db.Text)
    effectifMax = db.Column(db.Integer)
    coutJournalier = db.Column(db.Float)
