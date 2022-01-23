from upemtk import *
from random import randint
from time import sleep

##### constantes utilisée pour le jeu #####
dimension_fenetre = 400
nb_cases = 40
assert(dimension_fenetre % nb_cases==0)
taille_case = dimension_fenetre // nb_cases
###########################################

def perdu():
    texte(dimension_fenetre//2,dimension_fenetre//2,"Perdu!","red","center")
    attente_clic()

def gagne():
    texte(dimension_fenetre//2,dimension_fenetre//2,"Gagné!","red","center")
    attente_touche()

def mise_a_jour_direction(direction):
    nouvelle_dir=direction
    ev=donne_evenement()
    type_ev=type_evenement(ev)
    if type_ev=="Touche":
        t=touche(ev)
        if t=="Right":
            nouvelle_dir='droite'
        elif t=="Left":
            nouvelle_dir='gauche'
        if t=="Up":
            nouvelle_dir='haut'
        elif t=="Down":
            nouvelle_dir='bas'
    return nouvelle_dir

def ready():
    texte(dimension_fenetre//2,dimension_fenetre//2,"Tapez sur une touche !","red","center")
    attente_touche()
    efface_tout()

#### À vous de jouer !
def affiche_case(c,couleur):
    rectangle(c[0]*taille_case,c[1]*taille_case,c[0]*taille_case+taille_case-1,c[1]*taille_case+taille_case-1,couleur,couleur)


def affiche_cases(l, couleur):
    """
    affiche en couleur toutes les cases de la liste l
    """
    for i in range(len(l)):
        affiche_case(l[i],couleur)


def affiche_serpent(serpent):
    """
    affiche le serpent avec le corps en vert et la tête en bleu
    """
    affiche_cases(serpent,"green")
    affiche_case(serpent[-1],"blue")



def nouveau_serpent(taille):
    """
    renvoie un serpent de longueur taille, centré (en hauteur et en largeur) et en position horizontale
    """
    serpent = []
    y = (nb_cases//2)
    x = (nb_cases//2)-taille//2
    for i in range(taille):
        serpent.append((x+i,y))
    return serpent


def deplace_serpent(serpent, direction):
    """
    renvoie le serpent après un pas de déplacement dans la direction renseignée
    """
    new_serpent = serpent[1:].copy()
    if direction == 'haut':
        new_serpent.append((new_serpent[-1][0],new_serpent[-1][1]-1))
            
        return new_serpent

    if direction == 'bas':
        new_serpent.append((new_serpent[-1][0],new_serpent[-1][1]+1))
        return new_serpent

    if direction == 'gauche':
        new_serpent.append((new_serpent[-1][0]-1,new_serpent[-1][1]))
        return new_serpent

    if direction == 'droite':
        new_serpent.append((new_serpent[-1][0]+1,new_serpent[-1][1]))
        return new_serpent

def est_sorti(serpent):
    """
    renvoie True si le serpent est sorti de la fenêtre et False sinon
    """
    x = serpent[-1][0]
    y = serpent[-1][1]
    if x > 40 or x < 0 or y > 40 or y<0:
        return True
    return False

def a_mordu(serpent):
    """
    renvoie True si le serpent s'est mordu la queue (i.e la tête apparait dans le corps) 
    et False sinon
    """
    if serpent[-1] in serpent[:-1]:
        return True
    return False

def creer_pommes(nbPommes):
    """
    renvoie une liste de nbPommes cases
    """
    pommes = [(randint(0,40),randint(0,40)) for i in range(nbPommes)]
    return pommes

def affiche_pommes(pommes):
    """
    affiche les pommes en rouge
    """
    affiche_cases(pommes, "red")

def mange_pommes(pommes, serpent):
    """
    renvoie la listes de pommes sans les pommes touchées par le serpent
    remarque: c'est la tête du serpent qui mange la pomme...
    """
    for elem in pommes:
        if serpent[-1] == elem:
            pommes.remove(elem)
            return (pommes,True)
    return (pommes,False)

if __name__ == '__main__':

    cree_fenetre(dimension_fenetre,dimension_fenetre)

    ready()
    serpent = nouveau_serpent(10)
    affiche_serpent(serpent)
    pommes = creer_pommes(randint(8,15))
    affiche_pommes(pommes)

    ### creer et afficher le serpent ###
    direction = "droite"
    temps = 0
    



    while True:
        direction = mise_a_jour_direction(direction)
        if temps % 1800 == 0:

            
            pommes = mange_pommes(pommes, serpent)[0]
            efface_tout()
            sleep(0.020)
            serpent = deplace_serpent(serpent,direction)
            affiche_serpent(serpent)
            affiche_pommes(pommes)
            if mange_pommes(pommes, serpent)[1]:
                a=serpent[0][0]
                b=serpent[0][1]
                serpent.insert(0,(a,b))
                serpent.insert(0,(a,b))
                serpent.insert(0,(a,b))





        if a_mordu(serpent) or est_sorti(serpent):
            perdu()
            attente_clic()
            break
        if len(pommes) == 0:
            gagne()
            sleep(1)
            break
        temps = temps + 1
        mise_a_jour()





    ferme_fenetre()