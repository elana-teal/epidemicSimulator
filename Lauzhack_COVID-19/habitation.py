import random

TAUX_CONTAMINATION_HABITATION = 0.01
TAUX_CONTAMINATION_ECOLE= 0.02
TAUX_CONTAMINATION_HOPITAUX = 0.005
TAUX_CONTAMINATION_COMMERCE = 0.05
TAUX_CONTAMINATION_TRAVAIL = 0.02
TAUX_CONTAMINATION_LOISIR = 0.05
TAUX_CONTAMINATION_TRANSPORT = 0.1


class Batiment:

    def __init__(self, pos, capTravail=0, capAcceuil=0, tauxContamin=0):
        self.personnesPresentes = set()
        self.position = pos
        self.capaciteTravail = capTravail
        self.capaciteAcceuil = capAcceuil
        self.tauxContamination = tauxContamin
        self.ouvert = True
        self.couleur = "grey"
        self.lienImage = "rue.png"

    #retirer un bonhomme
    def retirer(self, personne):
        self.personnesPresentes.discard(personne)

    #ajouter un bonhomme
    def ajouter(self, personne):
         self.personnesPresentes.add(personne)

    #contamine les gens
    def update(self, mesures):
        nbPersonneContamine = 0
        for personne in self.personnesPresentes:
            if personne.peutContaminer():
                nbPersonneContamine += 1
        if len(self.personnesPresentes) == 0:
            tauxPersonneContamine = -1
        else:
            tauxPersonneContamine = nbPersonneContamine / len(self.personnesPresentes)

        risque = mesures.changementTauxContamination(self.tauxContamination) * tauxPersonneContamine

        for personne in self.personnesPresentes:
            if personne.estContaminable():
                aleatoire = random.randint(0,10000)/10000
                if aleatoire < risque:
                    personne.deviensContamine()

    def __repr__(self):
        return "{} : {} {}".format(type(self), *self.position)


class Rue(Batiment):

    def __init__(self, pos):
        super().__init__(pos)
        def f(*args):
            return
        self.update = f


class Habitation(Batiment):

    def __init__(self, pos):
        capAcceuil = random.randint(1, 7)
        super().__init__(pos, 0, capAcceuil, TAUX_CONTAMINATION_HABITATION)
        self.couleur = "orange"
        self.lienImage = "maison.png"
        self.lienImageVide = "maisonVide.png"
        

class Ecole(Batiment):

    def __init__(self, pos):
        capAcceuil = random.randint(20, 50)
        capTravail = 10
        super().__init__(pos, capTravail, capAcceuil, TAUX_CONTAMINATION_ECOLE)
        self.couleur = "cyan"
        self.lienImage = "ecole.png"


class Hopital(Batiment):

    def __init__(self, pos):
        capTravail = 20
        capAcceuil = float("inf")
        super().__init__(pos, capTravail, capAcceuil, TAUX_CONTAMINATION_HOPITAUX)
        self.couleur = "white"
        self.medecin = set()
        self.patient = set()
        self.lienImage = "hopital.png"

    def retirer(self, personne):
        super().retirer(personne)
        self.medecin.discard(personne)
        self.patient.discard(personne)

    def ajouter(self, personne):
        super().ajouter(personne)
        if personne.estSoigné:
            self.patient.add(personne)
        else:
            self.medecin.add(personne)


class Commerce(Batiment):

    def __init__(self, pos):
        capTravail = 15
        capAcceuil = 500
        super().__init__(pos, capTravail, capAcceuil, TAUX_CONTAMINATION_COMMERCE)
        self.couleur = "yellow"
        self.lienImage = "commerce.png"


class Travail(Batiment):

    def __init__(self, pos):
        capTravail = random.randint(50, 200)
        super().__init__(pos, capTravail, 0, TAUX_CONTAMINATION_TRAVAIL)
        self.couleur = "blue"
        self.lienImage = "entreprise.png"


class Loisir(Batiment):

    def __init__(self, pos):
        capTravail = random.randint(1, 10)
        capAcceuil = random.randint(150, 400)
        super().__init__(pos, capTravail, capAcceuil, TAUX_CONTAMINATION_LOISIR)
        self.couleur = "green"
        self.lienImage = "loisir.png"


class Transport(Batiment):

    def __init__(self, pos):
        capAcceuil = 10000
        super().__init__(pos, 0, capAcceuil, TAUX_CONTAMINATION_TRANSPORT)
        self.couleur = "brown"
        self.lienImage = "metro.png"


