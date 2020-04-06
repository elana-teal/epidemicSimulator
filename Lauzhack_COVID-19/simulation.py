import random
##
from outils import *
from mesures import *
from ville import *
from habitant import *

MAX_HABITANTS = 1000


class Simulation:

    def __init__(self):
        self.nouveauJour = False
        self.jour = 0
        self.quartHeure = 0

        self.ville = Ville()
        self.mesures = Mesures(self.ville)
        self.habitants = []

        self.axeTemps = [0]
        self.axeMalades = [0]
        self.axeMaladesDéclarés = [0]
        self.axeHospitalisés = [0]
        self.axeMorts = [0]
        self.axeGuéris = [0]

        self.remplir_ville()

    def calculer_statistiques(self):
        malades = 0
        maladesDéclérés = 0
        hospitalisés = 0
        morts = 0
        guéris = 0
        for habitant in self.habitants:
            if habitant.état == "infecté":
                malades += 1
            elif habitant.état == "symptomes":
                malades += 1
                maladesDéclérés += 1
                if habitant.estSoigné:
                    hospitalisés += 1
            elif habitant.état == "mort":
                morts += 1
            elif habitant.état == "guéri":
                guéris += 1
        self.axeTemps.append(self.jour)
        self.axeMalades.append(malades)
        self.axeMaladesDéclarés.append(maladesDéclérés)
        self.axeHospitalisés.append(hospitalisés)
        self.axeMorts.append(morts)
        self.axeGuéris.append(guéris)

    def remplir_ville(self):
        habitant = Habitant(20, self)
        habitant.deviensContamine()
        while habitant.emploiDuTemps.ok and len(self.habitants) < MAX_HABITANTS:
            self.habitants.append(habitant)
            age = random.randint(1, 70)
            if age > 60:
                while random.randint(1, 5) == 1:
                    age += random.randint(1, 5)
            habitant = Habitant(age, self)

    def simuler(self):
        self.incrémenter_temps()
        if self.nouveauJour:
            self.calculer_statistiques()
        for habitant in self.habitants:
            habitant.déplacer(self.ville)
            if self.nouveauJour:
                habitant.updateEtat()
        self.ville.update(self.mesures)

    def incrémenter_temps(self):
        self.quartHeure += 15
        self.nouveauJour = False
        if quartHeure(0, self.quartHeure) == quartHeure(24):
            self.jour += 1
            self.quartHeure = 0
            self.nouveauJour = True

    def tempsGlobal(self):
        j = self.jour % 7
        qh = quartHeure(0, self.quartHeure)
        return j, qh