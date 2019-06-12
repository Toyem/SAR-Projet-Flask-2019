from flask_sqlalchemy import SQLAlchemy
import inspect
import random


db = SQLAlchemy()


def init_database():
    db.create_all()
    #populate_database()


def populate_database():
    import database.models

    model_classes = [model_class for (model_name, model_class) in inspect.getmembers(database.models, inspect.isclass)]
    do_populate = sum([len(c.query.all()) for c in model_classes]) == 0

    if not do_populate:
        print("ATTENTION: Le fichier database/database.db (.db et non .py!) existe déjà, je n'ajoute rien dans la "
              "base de donnees. Supprimer ce fichier (database/database.db), avant de lancer le serveur web, pour que "
              "des donnees soient ajoutees.")
        return

    ##########################
    # Create d'ingenieurs
    ##########################
    PRENOMS = ["Antoine", "Jeremy", "Morgan", "Gilbert", "Patrick", "Julie", "Charlotte", "Margot"]
    NOM_DE_FAMILLES = ["Legrand", "Dupont", "Martin", "Lambert", "Guyadec", "Cornec"]
    BUREAUX = ["nantes", "brest", "rennes"]

    for i in range(0, 20):
        prenom = random.choice(PRENOMS)
        nom_famille = random.choice(NOM_DE_FAMILLES)
        nom_court = prenom.lower()[0] + nom_famille.lower()
        site = random.choice(BUREAUX)
        taux_journalier = round(random.uniform(240, 560), 2)
        statut = "disponible"
        estCommercial = bool(random.getrandbit(1))

        email = "%s.%s@%s_agency.bigcompany.fr" % (prenom.lower(),
                                                   nom_famille.lower(),
                                                   site.lower())
        new_engineer = database.models.Ingenieur(nom_court=nom_court,
                                                 prenom=prenom,
                                                 nom_famille=nom_famille,
                                                 site=site,
                                                 email=email,
                                                 taux_journalier=taux_journalier,
                                                 statut=statut,
                                                 estCommercial=estCommercial)

        db.session.add(new_engineer)
        try:
            db.session.commit()
        except Exception as e:
            print("[1] Je ne peux pas ajouter un ingenieur (ce qui peut etre normal) "
                  "a cause de : %s" % e)
            db.session.rollback()

    ##########################
    # Creation de competences
    ##########################
    SKILLS = ["developer", "management", "consultant", "motivated", "c++", "python", "web",
              "iot", "cloud", "linux", "windows", "office", "libreoffice"]

    for skill in SKILLS:
        new_skill = database.models.Competence(nom=skill)
        db.session.add(new_skill)

        try:
            db.session.commit()
        except Exception as e:
            print("[2] Je ne peux pas ajouter une competence (ce qui peut etre normal) "
                  "a cause de : %s" % e)
            db.session.rollback()

    ##########################################
    # Creation de missions + Responsables missions
    ##########################################
    ADJECTIFS = ["incredible", "revolutionary", "marvelous", "awesome", "next", "green", "sunny"]
    NOMS = ["revolution", "moon", "breakthrough", "landscape"]

    ingenieurs = database.models.Ingenieur.query.all()

    for i in range(0, 5):
        nouveau_titre = "%s %s" % (
            random.choice(ADJECTIFS),
            random.choice(NOMS)
        )
        responsable = random.choice(ingenieurs)
        description = "Description de la mission '%s'" % (nouveau_titre)
        prix_vente = random.randint(10000, 100000)
        effectifs_max = 4
        new_mission = database.models.Mission(titre=nouveau_titre,
                                              description=description,
                                              effectifs_max=effectifs_max,
                                              prix_vente=prix_vente,
                                              responsable_id=responsable.id)
        db.session.add(new_mission)

        try:
            db.session.commit()
        except Exception as e:
            print("[2] Je ne peux pas ajouter une mission (ce qui peut etre normal) "
                  "a cause de : %s" % e)
            db.session.rollback()

    ##########################################
    # Ajout de besoin en competence aux missions
    ##########################################
    missions = database.models.Mission.query.all()
    competences = database.models.Competence.query.all()

    for mission in missions:
        # Prendre 2 competences et pour chaque competence definir un besoin
        competences_choisies = random.sample(competences, 2)

        for competence in competences_choisies:
            besoin_en_ingenieurs = random.randint(15, 0)

            nouveau_besoin = database.models.Besoin(quantite_jour_homme=besoin_en_ingenieurs,
                                                    mission_id=mission.id,
                                                    competence_id=competence.id)
            db.session.add(nouveau_besoin)

            try:
                db.session.commit()
            except Exception as e:
                print("[3] Je ne peux pas ajouter un besoin competence sur une mission (ce qui peut etre normal) a cause de : %s" % e)
                db.session.rollback()


    ##########################################
    # Association de competences aux ingenieurs via des certifications
    ##########################################
    ingenieurs = database.models.Ingenieur.query.all()
    competences = database.models.Competence.query.all()

    for ingenieur in ingenieurs:
        competences_choisies = random.sample(competences, 4)
        for competence_choisie in competences_choisies:
            niveau = random.randint(10, 90)
            nouvelle_certification = database.models.Certification(niveau=niveau,
                                                                   ingenieur_id=ingenieur.id,
                                                                   competence_id=competence_choisie.id)

            db.session.add(nouvelle_certification)

            try:
                db.session.commit()
            except Exception as e:
                print("[3] Je ne peux pas ajouter une certification a un ingenieur (ce qui peut etre normal) "
                      "a cause de : %s" % e)
                db.session.rollback()

    ##########################################
    # Affectations d'ingenieurs aux missions
    ##########################################
    missions = database.models.Mission.query.all()

    from database.models import Ingenieur, Certification, Competence, Affectation
    from datetime import datetime

    # Un timestamp est une representation d'un couple date/heure. Une representation
    # courante est d'utiliser un entier representant le nombre de secondes ecoulees
    # depuis le 1er janvier 1970. Le nombre suivant represente le nombre de secondes
    # ecoulees entre le 1er janvier 1970 et le 07 juin 2019 à 13h12 et 50 secondes
    common_timestamp = 1559905910 # 07/06/2019 13:12:50

    for mission in missions:
        for besoin in mission.besoins:

            ingenieurs_avec_cette_competence = Ingenieur.query \
                .join(Certification) \
                .join(Competence) \
                .filter_by(id=besoin.competence.id) \
                .all()

            ingenieurs_affectes = random.sample(ingenieurs_avec_cette_competence, 2)

            for ingenieur_affecte in ingenieurs_affectes:

                duree_projet_en_semaine = random.randint(1, 24)
                decalage_par_rapport_a_common_timestamp_en_jours = random.randint(1, 365)
                date_debut_timestamp = common_timestamp \
                                       + decalage_par_rapport_a_common_timestamp_en_jours * 24 * 3600
                date_fin_timestamp = date_debut_timestamp + duree_projet_en_semaine * 7 * 24 * 3600

                nouvelle_affectation = Affectation(date_debut=datetime.fromtimestamp(date_debut_timestamp),
                                                   date_fin=datetime.fromtimestamp(date_fin_timestamp),
                                                   ingenieur_id=ingenieur_affecte.id,
                                                   mission_id=mission.id)

                db.session.add(nouvelle_affectation)

                try:
                    db.session.commit()
                except Exception as e:
                    print(
                        "[3] Je ne peux pas ajouter un besoin competence sur une mission (ce qui peut etre normal) a cause de : %s" % e)
                    db.session.rollback()

    ##########################################
    # Chaque ingenieur exprime deux souhaits
    ##########################################
    from database.models import Ingenieur, Certification, Competence, Affectation, Mission, Souhait, Besoin
    ingenieurs = Ingenieur.query.all()

    for ingenieur in ingenieurs:
        for i in range(0, 1):
            missions_avec_une_competence = Mission.query \
                .join(Besoin) \
                .join(Competence) \
                .join(Certification) \
                .filter(Certification.ingenieur_id==ingenieur.id) \
                .all()

            mission_souhaite = random.choice(missions_avec_une_competence)
            candidature =

            decalage_par_rapport_a_common_timestamp_en_jours = random.randint(1, 365)
            date_debut_timestamp = common_timestamp \
                                   + decalage_par_rapport_a_common_timestamp_en_jours * 24 * 3600
            nouveau_souhait = Souhait(date_candidature=date_candidature,
                                      ingenieur_id=ingenieur.id,
                                      mission_id=mission_souhaite.id)

            db.session.add(nouveau_souhait)

            try:
                db.session.commit()
            except Exception as e:
                print(
                    "[3] Je ne peux pas ajouter un souhait sur une mission (ce qui peut etre normal) a cause de : %s" % e)
                db.session.rollback()
