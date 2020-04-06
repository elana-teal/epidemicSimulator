from habitation import *


class Ville:

    def __init__(self):
        with open("CarteVille.txt", "r") as fichier:
            contenu = fichier.read().split("\n")

            self.longueur = len(contenu[0])
            self.largeur = len(contenu)

            self.typeBatiment = [[None for _ in range(self.largeur)] for _ in range(self.longueur)]
            self.batiments = [[None for _ in range(self.largeur)] for _ in range(self.longueur)]

            for y, line in enumerate(contenu):
                for x, caractere in enumerate(line):
                    self.batiments[x][y] = self.trouverBatiment(caractere, (x,y))
                    self.typeBatiment[x][y] = caractere


    def trouverBatiment(self, lettre, position):
        if lettre == 'M':
            return Habitation(position)
        if lettre == 'H':
            return Hopital(position)
        if lettre == 'T':
            return Travail(position)
        if lettre == "C":
            return Commerce(position)
        if lettre == "E":
            return Ecole(position)
        if lettre == "B":
            return Transport(position)
        if lettre == "L":
            return Loisir(position)
        if lettre == "R":
            return Rue(position)

    def demander(self, lettre, pos, chercheTravail):

        mini = (self.largeur+self.longueur)*2
        posMin = None

        #optimisation possible : parcourir des listes sérapées par rapport aux batiments
        for y in range(self.largeur):
            for x in range(self.longueur):
                
                if lettre.find(self.typeBatiment[x][y])>=0:
                    if ( chercheTravail and self.batiments[x][y].capaciteTravail>0 ) or ( not chercheTravail and self.batiments[x][y].capaciteAcceuil>0):
                        score = self.distanceManhattan(pos,(x,y))*random.randint(50,100)/100
                        if score<mini:
                            mini = score
                            posMin = (x,y)
        if posMin == None:
            return None
        if chercheTravail :
            self.batiments[posMin[0]][posMin[1]].capaciteTravail -= 1
        else:
            self.batiments[posMin[0]][posMin[1]].capaciteAcceuil -= 1
        return self.batiments[posMin[0]][posMin[1]]

    @staticmethod
    def distanceManhattan(posA, posB):
        return abs(posA[0]-posB[0])+abs(posA[1]-posB[1]);

    def demanderMaison(self):
        pos = random.randint(0, self.longueur - 1), random.randint(0, self.largeur - 1)
        return self.demander('M', pos, False)

    def demanderEcole(self, batiment):
        return self.demander('E', batiment.position, False)

    def demanderTravail(self, batiment):
        return self.demander('T', batiment.position, True)

    def demanderCommerce(self, batiment):
        return self.demander("C", batiment.position, False)

    def demanderLoisir(self, batiment):
        return self.demander('L', batiment.position, False)

    def demanderTransport(self, batiment):
        return self.demander("B", batiment.position, False)

    def demanderHopital(self, batiment):
        return self.demander("H", batiment.position, False)

    def update(self, mesures):
        for y in range(self.largeur):
            for x in range(self.longueur):
                self.batiments[x][y].update(mesures)
