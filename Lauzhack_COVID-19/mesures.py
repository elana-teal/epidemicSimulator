from habitation import *

SENSIBILISATION_MAX = 5
SENSIBILISATION_MIN = 0
TEST_MAX = 5;

class Mesures:

    def __init__(self, ville):
        self.ville = ville
        self.batiments = []
        for lines in self.ville.batiments:
            for batiment in lines:
                self.batiments.append(batiment)

        self.quarantaine = False
        self.sensibilisation = 0
        self.test = 0

        self.loisirs = True
        self.ecoles = True
        self.travail = True

    def switchEcole(self, debutQarantaine = False):
        if not self.quarantaine or debutQarantaine:
            self.ecoles = not self.ecoles
            for batiment in self.batiments:
                if isinstance(batiment, Ecole):
                    batiment.ouvert = self.ecoles

    def switchLoisir(self, debutQarantaine = False):
        if not self.quarantaine or debutQarantaine:
            self.loisirs = not self.loisirs
            for batiment in self.batiments:
                if isinstance(batiment, Loisir):
                    batiment.ouvert = self.loisirs

    def switchTravail(self, debutQarantaine = False):
        if not self.quarantaine or debutQarantaine:
            self.travail = not self.travail
            for batiment in self.batiments:
                if isinstance(batiment, Travail):
                    batiment.ouvert = self.travail

    def switchQuarantaine(self):
        self.quarantaine = not self.quarantaine
        
        if self.ecoles == self.quarantaine:
            self.switchEcole(True)
        if self.loisirs == self.quarantaine:
            self.switchLoisir(True)
        if self.travail == self.quarantaine:
            self.switchTravail(True)
            
    def changerSensibilisation(self,nouvSensibilisation):
        nouvSensibilisation = int(nouvSensibilisation)
        if nouvSensibilisation <= SENSIBILISATION_MAX and nouvSensibilisation>=SENSIBILISATION_MIN:
            self.sensibilisation = nouvSensibilisation

    def augmenterTest(self):
        if self.test < TEST_MAX:
            self.test += 1

    def changementTauxContamination(self, tauxContamination):
        return tauxContamination / ((self.sensibilisation + 2.5)/2.5 )