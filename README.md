# epidemicSimulator


##Inspiration

We wanted to create a simulation of an epidemic in a simcity-like city. The objective is to sensitize the player to the impact of the containment and prevention measures.

Nous avons voulu recréer une petite simulation / visualisation d'une épidémie qui se propage à l'échelle d'une ville. L'objectif est de faire prendre conscience de l'impact des mesures de confinement et de préventions.
##

What it does

Our software modelise the progagation of an epidemic in a small city. The city is made of different kind of buidings (houses, working places, schools, shops, hospitals, recreation centres, transport places). Each inhabitant has a planing that determins where he goes during the day : children go to school, adults go to work or go shoping... A contaminated person can contaminate people in the same buiding. The player can visualize the evolution of the simulation (eg: number of infected people in the city) with a graph. The player can close building to slow down the propagation of the epidemic. He can also sensitize the population to decrease the propagation speed.

Il s'agit d'une simulation d'une épidémie à l'échelle d'une ville. La ville est modélisée par des batiments de différentes couleurs (maisons, lieux de travail, écoles, centres commerciaux, hopitaux, loisir, transports). Les habitants se déplacent d'un batiment à un autre en suivant un emploi du temps défini au début de la simulation. Ainsi, les enfants vont à l'école tandis que les adultes se rendent au travail ou vont faire les courses. Une personne infectée peut propager le virus aux personnes présentes dans le même batiment. L'utilisateur peut visualiser sur un graphique l'évolution du nombre de cas en temps réel. L'utilisateur peut également prendre des mesures (fermer des batiments) pour ralentir la propagation de la maladie. Il peut aussi sensibiliser la population pour diminuer la vitesse de propagation.


##How I built it

Our software is coded in python3 with tkinter (graphic interface) and matplotlib (graphs). The simulation is available in a zip file on our submission. The script to run is "main.py". Note that you need python3 with the following modules installed : pillow, matplotlib, pygame.

La simulation est programmée en python avec le module tkinter pour l'interface graphique et matplotlib pour les graphiques. La simulation est disponible dans un fichier zip avec notre soumission. Le script a lancer est "main.py". Notez que vous aurez besoin de python 3 avec les modules suivants installés : pillow, matplotlib, pygame.
