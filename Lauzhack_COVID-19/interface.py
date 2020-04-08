from tkinter import *
from matplotlib import pyplot as plt
from matplotlib import colors as mcolors

from simulation import *
from musique import *

import statistics


FRAME_TIME = 800

TAILLE_BATIMENT = 80
TAILLE_HABITANT = 10
DX = 8

JOURS_SEMAINE = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]


class Application(Tk):

    def __init__(self, titre):
        super().__init__()
        super().title(titre)


        self.largeurEcran = self.winfo_screenwidth()
        self.hauteurEcran = self.winfo_screenheight()
        geometry = "{}x{}".format(round(self.largeurEcran * 0.8), round(self.hauteurEcran * 0.8))
        self.geometry(geometry)

        self.simulation = Simulation()

        self.musique = Musique()
        self.musique.commencer()

        self.simuler = False

        self.canvasFrame = Frame(self)
        self.canvasFrame.grid(row=1, column=0)
        self.canvas = Canvas(self.canvasFrame,
                             width=900,
                             height=700,
                             background="grey")

        self.popUpExiste = False
        self.canvas.bind('<Button-1>', self.clic_détecté)

        self.canvas.grid(row=0, column=0)
        self.vsb = Scrollbar(self.canvasFrame, orient="vertical", command=self.canvas.yview)
        self.vsb.grid(row=0, column=0, sticky="nse")
        self.hsb = Scrollbar(self.canvasFrame, orient="horizontal", command=self.canvas.xview)
        self.hsb.grid(row=0, column=0, sticky="ews")
        self.canvas.config(xscrollcommand=self.hsb.set, yscrollcommand=self.vsb.set)

        self.paletteCommandes = Frame(self)
        self.paletteCommandes.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.lancerSimulationBtn = Button(self.paletteCommandes,
                                          text="Lancer simulation",
                                          command=self.switch_simulation)
        self.lancerSimulationBtn.grid(row=1, column=3)

#
        self.radiobuttonFrame = Frame(self.paletteCommandes)
        self.radiobuttonFrame.grid(row=1, column=1, rowspan=3)
        self.varAfficherImage = IntVar()
        self.varAfficherImage.set(0)
        self.afficherImage = self.varAfficherImage.get()
        vals = [0, 1, 2]
        etiqs = ['Couleur', 'Image 2D', 'Image 3D']
        for i in range(3):
             self.b = Radiobutton(self.radiobuttonFrame, variable=self.varAfficherImage,command=self.switch_affichage, text=etiqs[i], value=vals[i])
             self.b.grid(row=i+1, column=1, sticky="nsew")

#
        self.afficherImage = 0
        self.modeDeVueChangé = False

        self.infoHeure = Label(self.paletteCommandes,
                               text="Jour 0, la simulation n'a pas encore commencé.")
        self.infoHeure.grid(row=0, column=0, columnspan=3, padx=20)
        self.infoPopulation = Label(self.paletteCommandes,
                                    text="Population")
        self.infoPopulation.grid(row=0, column=3, columnspan=2, padx=20)

        self.vitesseSimulation = Scale(self.paletteCommandes,
                                       orient="horizontal",
                                       from_=1, to=20,
                                       label="Vitesse simulation",
                                       length=200)
        self.vitesseSimulation.grid(row=1, column=4)
        self.vitesseSimulation.set(5)

        self.switchMusiqueBtn = Button(self.paletteCommandes,
                                    text="Musique",
                                    command=self.musique.switch)
        self.switchMusiqueBtn.grid(row=1, column=0)


        self.tauxSensibilisationScale = Scale(self.paletteCommandes,
                                       orient="horizontal",
                                       from_=0, to=5,
                                       label="Sensibilisation",
                                       length=200,
                                       command = self.simulation.mesures.changerSensibilisation)
        self.tauxSensibilisationScale.grid(row=1, column=5, padx=20)
        self.tauxSensibilisationScale.set(0)


        self.tripleSwitch = Frame(self.paletteCommandes)
        self.tripleSwitch.grid(row=0, column=6, rowspan=2)

        self.switchQuarantaineBtn = Button(self.tripleSwitch,
                                    text="Quarantaine",
                                    command=self.switchQuarantaine)
        self.switchQuarantaineBtn.grid(row=0, column=0, sticky="nsew")

        self.switchEcoleBtn = Button(self.tripleSwitch,
                                    text="Arrêter Ecole",
                                    command=self.switchEcole)
        self.switchEcoleBtn.grid(row=1, column=0, sticky="nsew")

        self.switchTravailBtn = Button(self.tripleSwitch,
                                    text="Arrêter Travail",
                                    command=self.switchTravail)
        self.switchTravailBtn.grid(row=2, column=0, sticky="nsew")

        self.switchLoisirBtn = Button(self.tripleSwitch,
                                    text="Arrêter Loisir",
                                    command=self.switchLoisir)
        self.switchLoisirBtn.grid(row=3, column=0, sticky="nsew")

        self.afficherMaisonBtn = Button(self.paletteCommandes,
                                    text="Cacher Maison",
                                    command=self.switchAffichageMaison)
        self.afficherMaisonBtn.grid(row=1, column=2)
        self.afficherMaison = True

        self.switchGraphiqueBtn = Button(self.paletteCommandes,
                                         text="Cacher statistiques",
                                         command=self.switch_graphique)
        self.switchGraphiqueBtn.grid(row=1, column=7, padx=20)
        self.afficherGraphique = True


        self.simulationFini = False
        #graphique
        self.actualiserAffichage = True

        self.graphique = Canvas(self,
                                width=600,
                                height=700,
                                background="white")
        self.graphique.grid(row=1, column=1)
        self.graphiqueAChangé = False

        self.protocol("WM_DELETE_WINDOW", self.quitter)
        self.bind("<Configure>", self.redimensionner)

        self.simulation.calculer_statistiques()
        self.tracer_graphique()

        self.avancer_simulation()

    def redimensionner(self, event):
        self.largeurEcran = self.winfo_width()
        self.hauteurEcran = self.winfo_height()
        hauteurDisponible = self.hauteurEcran - self.paletteCommandes.winfo_height()
        if self.afficherGraphique:
            self.canvas.config(width=int(self.largeurEcran * 0.6), height=hauteurDisponible * 1)
            self.graphique.config(width=int(self.largeurEcran * 0.4), height=hauteurDisponible * 1)
        else:
            self.canvas.config(width=self.largeurEcran * 1, height=hauteurDisponible * 1)
            self.graphique.config(width=0, height=0)
        self.graphiqueAChangé = True

    def quitter(self):
        self.musique.arreter()
        self.after_cancel(self.dernièreTache)
        self.destroy()
        self.quit()

    def tracer_graphique(self):
        GRAPHES = ["axeMalades", "axeMaladesDéclarés", "axeHospitalisés", 
                   "axeMorts", "axeGuéris"]
        COULEURS = ["red", "yellow", "blue", "black", "green"]
        for y, c in zip([getattr(self.simulation, attr) for attr in GRAPHES], COULEURS):
            plt.plot(self.simulation.axeTemps, y, "xkcd:"+c)
        plt.xlabel("Temps en jours")
        plt.ylabel("Nombre de personnes")
        plt.title("Statistiques de la ville")
        plt.legend(["cas réels", "cas officiels", "cas sévères", "morts", "guéris"])
        plt.savefig("graphe.png")
        plt.clf()
        self.graphique.delete("all")
        self.__imageDuGraphique = dimensionner("graphe.png", int(self.graphique.cget("width")))
        self.graphique.create_image(0, 0, anchor="nw", image=self.__imageDuGraphique)

    def dessiner_ville(self):
        scale = 1

        if self.actualiserAffichage:
            self.actualiserAffichage = False
            self.canvas.delete("batiment")
            self.images = []
            for y in range(self.simulation.ville.largeur):
                for x in range(self.simulation.ville.longueur):
                    batiment = self.simulation.ville.batiments[x][y]
                    x0, y0 = grille_vers_canvas(batiment.position, self.afficherImage, TAILLE_BATIMENT*scale)
                    x1, y1 = x0 + TAILLE_BATIMENT, y0 + TAILLE_BATIMENT
                    
                    
                    if self.afficherImage == 1:
                        im = dimensionner("ressource/"+batiment.lienImage, TAILLE_BATIMENT)
                        self.canvas.create_rectangle(x0, y0, x1, y1, tags="batiment")
                        self.canvas.create_image(x0, y0, image=im, anchor="nw", tags="batiment")
                        self.images.append(im)
                    elif self.afficherImage == 0:
                        self.canvas.create_rectangle(x0, y0, x1, y1,fill=batiment.couleur, tags="batiment")
                    else:
                        if isinstance(batiment,Habitation) and not self.afficherMaison:
                            im = dimensionner("ressource2/"+batiment.lienImageVide, TAILLE_BATIMENT)
                        else:
                            im = dimensionner("ressource2/"+batiment.lienImage, TAILLE_BATIMENT)
                        self.canvas.create_image(x0, y0, image=im, anchor="nw", tags="batiment")
                        self.images.append(im)

        self.canvas.delete("habitant")
        for habitant in self.simulation.habitants:
            posBat = grille_vers_canvas(habitant.localisation.position, self.afficherImage, TAILLE_BATIMENT*scale)
            if habitant.déplacement == "rapide" or self.modeDeVueChangé:
                modeRapide = True
            elif habitant.déplacement == "non":
                continue
            else:
                modeRapide =  False
            déplacer_habitant(habitant, posBat, modeRapide, self.afficherImage, TAILLE_BATIMENT)
            facteur = 1
            if self.afficherImage == 2:
                facteur = 0.5
            p2 = [v + TAILLE_HABITANT * facteur for v in habitant.position]
            self.canvas.create_oval(*habitant.position, *p2,
                                    fill=habitant.couleur, tags="habitant")
        
        if self.popUpExiste:
            self.canvas.lower("habitant", "popup")
        j, qh = self.simulation.jour, self.simulation.quartHeure
        js = JOURS_SEMAINE[j % 7]
        h, m = [str(v) for v in heureJournée(qh)]
        h = "0"+h if len(h) == 1 else h
        m = "0"+m if len(m) == 1 else m
        info = "{jour} {date} jours après le début de l'épidémie, {heure}:{min}" \
               .format(jour=js, date=j, heure=h, min=m)
        self.infoHeure.config(text=info)
        population = len(self.simulation.habitants)
        malades = self.simulation.axeMalades[-1]
        info = "Population : {} malades / {} habitants ({}%)" \
               .format(malades, population, round(100 * malades / population, 2))
        self.infoPopulation.config(text=info)
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        if self.graphiqueAChangé and self.afficherGraphique:
            self.tracer_graphique()
            self.graphiqueAChangé = False
        if self.simulation.axeMalades[-1] < 5 and self.simulation.axeGuéris[-1] > 5 and self.simulation.jour>5:
            self.statistiques_finales()
            self.lancerSimulationBtn.config(text = "Recommencer Simulation")
            self.simuler = False
            self.simulationFini = True
        else:
            self.canvas.delete("texte")
        self.modeDeVueChangé = False
        
    def statistiques_finales(self):
        nonTouchés = []
        morts = []
        guéris = []
        sévère = []
        for habitant in self.simulation.habitants:
            if habitant.état == "naif":
                nonTouchés.append(habitant.age)
            elif habitant.casSévère:
                sévère.append(habitant.age)
                if habitant.état == "mort":
                    morts.append(habitant.age)
                else:
                    guéris.append(habitant.age)
            else:
                guéris.append(habitant.age)
        def stats_age(data):
            if len(data) == 0:
                return "[]"
            maxi = max(data)
            mini = min(data)
            med = statistics.median(data)
            message = "[{} | {} | {}]".format(mini, med, maxi)
            return message
        popTotale = len(self.simulation.habitants)
        nt = len(nonTouchés)
        g = len(guéris)
        m = len(morts)
        t = popTotale - nt
        s = len(sévère)
        durée = self.simulation.jour
        message = """
Population initiale : {pop} {ap}
Durée de la simulation : {durée} jours

Résultats de l'épidémie :

Non-touchés : {nt} ({ntp}%) {ant}
Touchés : {t} ({tp}%) {at}
    Guéris : {g} ({gp}%) {ag}
    Cas sévères : {s} ({sp}%) {acs}
        Dont Morts  : {m} ({mp}%) {am}

Les proportions sont données par rapport à la population totale.
Entre crochets sont indiqués les ages des personnes de la catégorie concernée
au format : [age min | age médian | age max]
""".format(pop=popTotale,
           durée=durée,
           nt=nt,
           ntp=round(100*nt/popTotale, 2),
           t=t,
           tp=round(100*t/popTotale, 2),
           g=g,
           gp=round(100*g/popTotale, 2),
           s=s,
           sp=round(100*s/popTotale, 2),
           m=m,
           mp=round(100*m/popTotale, 2),
           ap=stats_age([h.age for h in self.simulation.habitants]),
           ant=stats_age(nonTouchés),
           at=stats_age([h.age for h in self.simulation.habitants if h.touché]),
           ag=stats_age(guéris),
           acs=stats_age(sévère),
           am=stats_age(morts))
        self.canvas.delete("all")
        self.canvas.create_text(0, 0, anchor="nw", text=message, fill="white",tags="texte")

    def switch_simulation(self):
        if self.simulationFini:
            self.simulationFini = False
            self.simulation = Simulation()
            self.actualiserAffichage = True
            self.modeDeVueChangé = True
            self.texteBouton()
            self.tauxSensibilisationScale.set(0)

        self.simuler = not self.simuler
        if self.simuler:
            texte = "Stopper simulation"
        else:
            texte = "Lancer simulation"
        self.lancerSimulationBtn.config(text=texte)

    def avancer_simulation(self):
        if self.simuler:
            self.simulation.simuler()
            self.dessiner_ville()
            if self.simulation.nouveauJour and self.afficherGraphique:
                self.tracer_graphique()
        self.dernièreTache = self.after(round(FRAME_TIME / self.vitesseSimulation.get()), self.avancer_simulation)

    def switch_affichage(self):
        self.actualiserAffichage = True
        self.modeDeVueChangé = True
        self.afficherImage = self.varAfficherImage.get()
        self.canvas.delete("popup")
        self.popUpExiste = False

    def switch_graphique(self):
        self.actualiserAffichage = True

        self.afficherGraphique = not self.afficherGraphique
        if self.afficherGraphique:
            texte = "Cacher statistiques"
        else:
            texte = "Afficher statistiques"
        self.switchGraphiqueBtn.config(text=texte)
        self.redimensionner(None)

    def switchQuarantaine(self):
        self.simulation.mesures.switchQuarantaine()
        self.texteBouton()

    def switchEcole(self):
        self.simulation.mesures.switchEcole()
        self.texteBouton()

    def switchLoisir(self):
        self.simulation.mesures.switchLoisir()
        self.texteBouton()

    def switchTravail(self):
        self.simulation.mesures.switchTravail()
        self.texteBouton()

    def texteBouton(self):
        self.switchEcoleBtn.config(text=("Fermer"if self.simulation.mesures.ecoles else"Rouvrir")+" Ecole")
        self.switchTravailBtn.config(text=("Fermer"if self.simulation.mesures.travail else"Rouvrir")+" Travail")
        self.switchLoisirBtn.config(text=("Fermer"if self.simulation.mesures.loisirs else"Rouvrir")+" Loisir")
        self.switchQuarantaineBtn.config(text=("Fin q"if self.simulation.mesures.quarantaine else"Q")+"uarantaine")

        if self.simulation.mesures.quarantaine:
            self.switchEcoleBtn.config(text="/")
            self.switchTravailBtn.config(text="/")
            self.switchLoisirBtn.config(text="/")

    def switchAffichageMaison(self):
        self.actualiserAffichage = True
        self.afficherMaison = not self.afficherMaison
        self.afficherMaisonBtn.config(text="Afficher Maison"if not self.afficherMaison else"Cacher Maison")


    def clic_détecté(self, event):
        self.canvas.delete("popup")
        self.popUpExiste = False
        xc, yc = self.canvas.canvasx(event.x), self.canvas.canvasy(event.y)
        if self.afficherImage == 2:
            xc -= TAILLE_BATIMENT / 3
            yc -= TAILLE_BATIMENT / 3
        grille = canvas_vers_grille((xc, yc), self.afficherImage, TAILLE_BATIMENT)
        x, y = grille
        if (x < 0 or y < 0):
            return
        try:
            bat = self.simulation.ville.batiments[x][y]
            x, y = xc + TAILLE_BATIMENT / 4, yc - TAILLE_BATIMENT / 4
            self.encadré_info(x, y, bat)
        except IndexError:
            bat = None

    def encadré_info(self, x, y, batiment):
        pop = len(batiment.personnesPresentes)
        catégorie = batiment.__class__.__name__
        statut = "Ouvert" if batiment.ouvert else "Fermé"
        info = "{}\nPopulation : {}\nStatut : {}" \
                .format(catégorie, pop, statut)
        popUp = self.canvas.create_text(x, y, anchor="sw", text=info, tags="popup")
        rect=self.canvas.create_rectangle(self.canvas.bbox(popUp), fill="white", tags="popup")
        self.canvas.tag_lower(rect,popUp)
        self.popUpExiste = True
