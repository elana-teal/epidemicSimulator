import random

from outils import *
from habitation import *


AGE_MAX_BEBE = 3
AGE_MAX_ETUDES = 20
AGE_RETRAITE = 62


class Habitant:

    def __init__(self, age, simulation):
        self.age = age
        self.état = "naif"
        self.touché = False
        self.estSoigné = False
        self.casSévère = False
        self.simulation = simulation
        self.emploiDuTemps = EmploiDuTemps(age, simulation.ville)
        # détruire le personnage si l'emploi du temps n'est pas ok
        self.localisation = None
        self.duréeInfection = 0
        self.tauxSymptomes = 0
        self.couleur = "black"
        self.déplacement = "rapide"

    def déplacer(self, ville):
        if self.état == "mort":
            self.déplacement = "non"
            return
        jour, quartHeure = self.simulation.tempsGlobal()
        nouvelleLocalisation = self.emploiDuTemps.semaine[jour][quartHeure]
        if self.état == "symptomes":
            if not isinstance(nouvelleLocalisation, (Habitation, Hopital)):
                nouvelleLocalisation = self.localisation
            if self.tauxSymptomes > 70:
                if not isinstance(nouvelleLocalisation, Hopital):
                    nouvelleLocalisation = ville.demanderHopital(self.localisation)
                    if nouvelleLocalisation is None:
                        nouvelleLocalisation = self.localisation
            if isinstance(nouvelleLocalisation, Hopital):
                self.estSoigné = True
                self.casSévère = True
            else:
                self.estSoigné = False
        if isinstance(nouvelleLocalisation, Transport):
            prochaineDestination = self.emploiDuTemps.semaine[jour][quartHeure + 1]
            if not prochaineDestination.ouvert:
                nouvelleLocalisation = self.localisation
        if nouvelleLocalisation == self.localisation:
            self.déplacement = "lent"
            return
        if nouvelleLocalisation.ouvert:
            self.déplacement = "rapide"
            if not self.localisation is None:
                self.localisation.retirer(self)
            nouvelleLocalisation.ajouter(self)
            self.localisation = nouvelleLocalisation

    def peutContaminer(self):
        if self.état in ["infecté", "symptomes"]:
            return True
        return False

    def estContaminable(self):
        if self.état == "naif" and (not self.touché):
            return True
        return False

    def deviensContamine(self):
        if self.état == "naif":
            self.touché = True
            self.couleur = "yellow"
        else:
            raise Exception("Impossible de contaminer un individu non-naif !")

    def updateEtat(self):
        if self.état == "mort":
            self.localisation.retirer(self)
            self.estSoigné = False
            self.couleur = "grey"
            return
        elif self.état == "guéri":
            return
        if self.touché and self.état == "naif":
            self.état = "infecté"
            self.couleur = "orange"
        if self.état == "infecté":
            #évoluer avec une certaine probabilité vers symptomes
            self.tauxSymptomes = self.calculer_symptomes()
            self.duréeInfection += 1
            #TODO trouver un modèle de calcul
            SEUIL_DETECTION = 50
            if self.tauxSymptomes > SEUIL_DETECTION:
                self.état = "symptomes"
                self.couleur = "red"
        elif self.état == "symptomes":
            self.tauxSymptomes = self.calculer_symptomes()
            self.duréeInfection += 1
        if self.tauxSymptomes >= 100:
            self.état = "mort"
        elif self.tauxSymptomes < 0 and self.duréeInfection > 5:
            self.état = "guéri"
            self.couleur = "lightgreen"

    def calculer_symptomes(self):
        # Les valeurs du taux de symptomes vont de 0 à 100
        MAX = 80 # valeur du taux au maximum par défaut
        FIN = 15 # nombre de jours avant guérison
        FLUCTUATION = 8
        maxReel = MAX + self.age / 4
        a = -4 * maxReel / (FIN**2)
        SOIN = 15
        if self.estSoigné:
            m = len(self.localisation.medecin)
            p = len(self.localisation.patient)
            soin = SOIN * (m + 2) / p 
        else:
            soin = 0
        taux = a * self.duréeInfection * (self.duréeInfection - FIN) \
               + random.randint(-FLUCTUATION, FLUCTUATION) - soin
        return taux


class EmploiDuTemps:

    def __init__(self, age, ville):
        self.semaine = [["" for _ in range(quartHeure(24))] for _ in range(7)]
        self.ok = self.créer_emploi_du_temps(age, ville)

    def créer_emploi_du_temps(self, age, ville):
        maMaison = ville.demanderMaison()
        if maMaison is None:
            return False
        for j in range(7):
            for t in range(0, quartHeure(24)):
                self.semaine[j][t] = maMaison
        if age <= AGE_MAX_BEBE:
            pass #les bébés ne font rien
        elif age <= AGE_MAX_ETUDES:
            #école
            monEcole = ville.demanderEcole(maMaison)
            if not monEcole is None:
                for j in range(0, 5):
                    for t in range(quartHeure(8), quartHeure(18)):
                        self.semaine[j][t] = monEcole
            else:
                pass
        elif age <= AGE_RETRAITE:
            #travail
            monTravail = ville.demanderTravail(maMaison)
            if not monTravail is None:
                for j in range(0, 5):
                    for t in range(quartHeure(7), quartHeure(19)):
                        self.semaine[j][t] = monTravail
            else:
                pass
        if age > AGE_MAX_ETUDES:
            # manger, acheter, consommer, dépenser son argent...
            j = random.randint(0,6)
            h = random.randint(9, 18)
            d = random.randint(2, 8)
            monMagasin = ville.demanderCommerce(maMaison)
            if not monMagasin is None:
                for t in range(quartHeure(h), quartHeure(h, 15 * d)):
                    self.semaine[j][t] = monMagasin
            else:
                pass
        if age > AGE_MAX_BEBE:
            # s'amuser, loisirs
            for j in range(7):
                if random.randint(1, 3) == 1:
                    durée = random.randint(2, 18)
                    h = random.randint(8, 19)
                    monLoisir = ville.demanderLoisir(maMaison)
                    for t in range(quartHeure(h), quartHeure(h, 15 * durée)):
                        self.semaine[j][t] = monLoisir
        self.créer_transports(ville)
        return True

    def créer_transports(self, ville):
        dernierLieu = self.semaine[0][0]
        for j, jour in enumerate(self.semaine):
            for qh, lieu in enumerate(jour):
                if lieu != dernierLieu:
                    départ = ville.demanderTransport(dernierLieu)
                    dernierLieu = lieu
                    self.semaine[j][qh] = départ