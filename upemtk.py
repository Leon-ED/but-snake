#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Fichier upemtk.py
# BibliothÃ¨que graphique simplifiÃ©e utilisant le module tkinter
# DÃ©rivÃ© de iutk.py, IUT de Champs-sur-Marne, 2013-2014

from tkinter import *
from tkinter import font
import subprocess
import sys
# from tkinter import _tkinter
from time import *
# import os

__all__ = ['ignore_exception', 'auto_update', 'cree_fenetre',
           'ferme_fenetre', 'mise_a_jour', 'ligne', 'fleche',
           'polygone', 'rectangle', 'cercle', 'point', 'marque',
           'image', 'texte', 'longueur_texte', 'hauteur_texte',
           'efface_tout', 'efface', 'efface_marque', 'attente_clic',
           'attente_touche', 'attente_touche_jusqua', 'attente_clic_ou_touche', 'clic',
           'capture_ecran', 'donne_evenement', 'type_evenement',
           'clic_x', 'clic_y', 'touche', 'TypeEvenementNonValide',
           'FenetreNonCree', 'FenetreDejaCree']


class CustomCanvas:
    """
    Classe qui encapsule tous les objets tkinter nÃ©cessaires Ã  la crÃ©ation
    d'un canevas.
    """

    def __init__(self, width, height):
        # width and height of the canvas
        self.width = width
        self.height = height

        # root Tk object
        self.root = Tk()

        # canvas attached to the root object
        self.canvas = Canvas(self.root, width=width,
                             height=height, highlightthickness=0)

        # binding of the different events
        self.root.protocol("WM_DELETE_WINDOW", self.event_quit)
        self.canvas.bind("<Button-1>", self.event_handler_button1)
        right_button = "<Button-3>"  # d'aprÃ¨s la doc le bouton droit le 3
        if sys.platform.startswith("darwin"):  # sous mac c'est le bouton 2
            right_button = "<Button-2>"
        self.canvas.bind(right_button, self.event_handler_button2)
        self.canvas.bind_all("<Key>", self.event_handler_key)
        self.canvas.bind("<Motion>", self.event_handler_motion)
        self.canvas.pack()

        # eventQueue stores the list of events received
        self.eventQueue = []

        # font for the texte functions
        self.set_font("Purisa", 24)

        # marque
        self.tailleMarque = 5

        # update
        self.root.update()

    def set_font(self, _font, size):
        self.tkfont = font.Font(self.canvas, font=(_font, size))
        self.tkfont.height = self.tkfont.metrics("linespace")

    def update(self):
        # sleep(_tkinter.getbusywaitinterval() / 1000)
        self.root.update()

    def event_handler_key(self, event):
        self.eventQueue.append(("Touche", event))

    def event_handler_button2(self, event):
        self.eventQueue.append(("ClicDroit", event))

    def event_handler_button1(self, event):
        self.eventQueue.append(("ClicGauche", event))

    def event_handler_motion(self, event):
        self.eventQueue.append(("Deplacement", event))

    def event_quit(self):
        self.eventQueue.append(("Quitte", ""))


__canevas = None
__img = dict()


# ############################################################################
# Exceptions
#############################################################################

class TypeEvenementNonValide(Exception):
    pass


class FenetreNonCree(Exception):
    pass


class FenetreDejaCree(Exception):
    pass


#############################################################################
# Initialisation, mise Ã  jour et fermeture
#############################################################################
def ignore_exception(function):
    def dec(*args, **kwargs):
        try:
            return function(*args, **kwargs)
        except Exception:
            exit(0)
    return dec


def auto_update(function):
    def dec(*args, **kwargs):
        global __canevas
        retval = function(*args, **kwargs)
        __canevas.canvas.update()
        return retval
    return dec


def cree_fenetre(largeur, hauteur):
    """
    CrÃ©e une fenÃªtre de dimensions ``largeur`` x ``hauteur`` pixels.
    """
    global __canevas
    if __canevas is not None:
        raise FenetreDejaCree(
            'La fenÃªtre a dÃ©jÃ  Ã©tÃ© crÃ©e avec la fonction "cree_fenetre".')
    __canevas = CustomCanvas(largeur, hauteur)


def ferme_fenetre():
    """
    DÃ©truit la fenÃªtre.
    """
    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenÃªtre n'a pas Ã©tÃ© crÃ©e avec la fonction \"cree_fenetre\".")
    __canevas.root.destroy()
    __canevas = None


def mise_a_jour():
    """
    Met Ã  jour la fenÃªtre. Les dessins ne sont affichÃ©s qu'aprÃ¨s 
    l'appel Ã   cette fonction.
    """
    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenÃªtre n'a pas Ã©tÃ© crÃ©e avec la fonction \"cree_fenetre\".")
    __canevas.update()


#############################################################################
# Fonctions de dessin
#############################################################################


# Formes gÃ©omÃ©triques

def ligne(ax, ay, bx, by, couleur='black', epaisseur=1, tag=''):
    """
    Trace un segment reliant le point ``(ax, ay)`` au point ``(bx, by)``.

    :param float ax: abscisse du premier point
    :param float ay: ordonnÃ©e du premier point
    :param float bx: abscisse du second point
    :param float by: ordonnÃ©e du second point
    :param str couleur: couleur de trait (dÃ©faut 'black')
    :param float epaisseur: Ã©paisseur de trait en pixels (dÃ©faut 1)
    :param str tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_line(
        ax, ay, bx, by,
        fill=couleur,
        width=epaisseur,
        tag=tag)


def fleche(ax, ay, bx, by, couleur='black', epaisseur=1, tag=''):
    """
    Trace une flÃ¨che du point ``(ax, ay)`` au point ``(bx, by)``.

    :param float ax: abscisse du premier point
    :param float ay: ordonnÃ©e du premier point
    :param float bx: abscisse du second point
    :param float by: ordonnÃ©e du second point
    :param str couleur: couleur de trait (dÃ©faut 'black')
    :param float epaisseur: Ã©paisseur de trait en pixels (dÃ©faut 1)
    :param str tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette)
    :return: identificateur d'objet
    """
    global __canevas
    x, y = (bx - ax, by - ay)
    n = (x**2 + y**2)**.5
    x, y = x/n, y/n    
    points = [bx, by, bx-x*5-2*y, by-5*y+2*x, bx-x*5+2*y, by-5*y-2*x]
    return __canevas.canvas.create_polygon(
        points, 
        fill=couleur, 
        outline=couleur,
        width=epaisseur,
        tag=tag)


def polygone(points, couleur='black', remplissage='', epaisseur=1, tag=''):
    """
    Trace un polygone dont la liste de points est fournie.

    :param list points: liste de couples (abscisse, ordonnee) de points
    :param str couleur: couleur de trait (dÃ©faut 'black')
    :param float epaisseur: Ã©paisseur de trait en pixels (dÃ©faut 1)
    :param str tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_polygon(
        points, 
        fill=remplissage, 
        outline=couleur,
        width=epaisseur,
        tag=tag)


def rectangle(ax, ay, bx, by,
              couleur='black', remplissage='', epaisseur=1, tag=''):
    """
    Trace un rectangle noir ayant les point ``(ax, ay)`` et ``(bx, by)``
    comme coins opposÃ©s.

    :param float ax: abscisse du premier coin
    :param float ay: ordonnÃ©e du premier coin
    :param float bx: abscisse du second coin
    :param float by: ordonnÃ©e du second coin
    :param str couleur: couleur de trait (dÃ©faut 'black')
    :param str remplissage: couleur de fond (dÃ©faut transparent)
    :param float epaisseur: Ã©paisseur de trait en pixels (dÃ©faut 1)
    :param str tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_rectangle(
        ax, ay, bx, by,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)


def cercle(x, y, r, couleur='black', remplissage='', epaisseur=1, tag=''):
    """ 
    Trace un cercle de centre ``(x, y)`` et de rayon ``r`` en noir.

    :param float x: abscisse du centre
    :param float y: ordonnÃ©e du centre
    :param float r: rayon
    :param str couleur: couleur de trait (dÃ©faut 'black')
    :param str remplissage: couleur de fond (dÃ©faut transparent)
    :param float epaisseur: Ã©paisseur de trait en pixels (dÃ©faut 1)
    :param str tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_oval(
        x - r, y - r, x + r, y + r,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)


def arc(x, y, r, ouverture=90, depart=0, couleur='black', remplissage='',
        epaisseur=1, tag=''):
    """
    Trace un arc de cercle de centre ``(x, y)``, de rayon ``r`` et
    d'angle d'ouverture ``ouverture`` (dÃ©faut : 90 degrÃ©s, dans le sens
    contraire des aiguilles d'une montre) depuis l'angle initial ``depart``
    (dÃ©faut : direction 'est').

    :param float x: abscisse du centre
    :param float y: ordonnÃ©e du centre
    :param float r: rayon
    :param float ouverture: abscisse du centre
    :param float depart: ordonnÃ©e du centre
    :param str couleur: couleur de trait (dÃ©faut 'black')
    :param str remplissage: couleur de fond (dÃ©faut transparent)
    :param float epaisseur: Ã©paisseur de trait en pixels (dÃ©faut 1)
    :param str tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette)
    :return: identificateur d'objet
    """
    global __canevas
    return __canevas.canvas.create_arc(
        x - r, y - r, x + r, y + r,
        extent=ouverture,
        start=init,
        style=ARC,
        outline=couleur,
        fill=remplissage,
        width=epaisseur,
        tag=tag)



def point(x, y, couleur='black', epaisseur=1, tag=''):
    """
    Trace un point aux coordonnÃ©es ``(x, y)`` en noir.

    :param float x: abscisse
    :param float y: ordonnÃ©e
    :param str couleur: couleur du point (dÃ©faut 'black')
    :param float epaisseur: Ã©paisseur de trait en pixels (dÃ©faut 1)
    :param str tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette)
    :return: identificateur d'objet
    """
    return ligne(x, y, x + epaisseur, y + epaisseur,
                 couleur, epaisseur, tag)


# Marques

def marque(x, y, couleur="red"):
    """
    Place la marque sur la position (x, y) qui peut Ãªtre effacÃ© en appelant
    ``efface_marque()`` ou ``efface('marque')``. Une seule marque peut Ãªtre
    prÃ©sente simultanÃ©ment.

    :param float x: abscisse
    :param float y: ordonnÃ©e
    :param str couleur: couleur de trait (dÃ©faut 'black')
    :return: ``None``
    """
    global __canevas
    efface_marque()
    __canevas.marqueh = ligne(
        x - __canevas.tailleMarque, y,
        x + __canevas.tailleMarque, y, couleur, tag='marque')
    __canevas.marquev = ligne(
        x, y - __canevas.tailleMarque,
        x, y + __canevas.tailleMarque, couleur, tag='marque')


# Image

def image(x, y, fichier, ancrage='center', tag=''):
    """
    Affiche l'image contenue dans ``fichier`` avec ``(x, y)`` comme centre. Les
    valeurs possibles du point d'ancrage sont ``'center'``, ``'nw'``, etc.

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnÃ©e du point d'ancrage
    :param str fichier: nom du fichier contenant l'image
    :param ancrage: position du point d'ancrage par rapport Ã  l'image
    :param str tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette)
    :return: identificateur d'objet
    """
    global __canevas
    global __img
    img = PhotoImage(file=fichier)
    img_object = __canevas.canvas.create_image(
        x, y, anchor=ancrage, image=img, tag=tag)
    __img[img_object] = img
    return img_object


# Texte

def texte(x, y, chaine,
          couleur='black', ancrage='nw', police="Purisa", taille=24, tag=''):
    """
    Affiche la chaÃ®ne ``chaine`` avec ``(x, y)`` comme point d'ancrage (par
    dÃ©faut le coin supÃ©rieur gauche).

    :param float x: abscisse du point d'ancrage
    :param float y: ordonnÃ©e du point d'ancrage
    :param str couleur: couleur de trait (dÃ©faut 'black')
    :param ancrage: position du point d'ancrage (dÃ©faut 'nw')
    :param police: police de caractÃ¨res (dÃ©faut : 'Purisa')
    :param taille: taille de police (dÃ©faut 24)
    :param tag: Ã©tiquette d'objet (dÃ©faut : pas d'Ã©tiquette
    :return: identificateur d'objet
    """
    global __canevas
    __canevas.set_font(police, taille)
    return __canevas.canvas.create_text(
        x, y,
        text=chaine, font=__canevas.tkfont, tag=tag,
        fill=couleur, anchor=ancrage)


def longueur_texte(chaine):
    """
    Donne la longueur en pixel nÃ©cessaire pour afficher ``chaine``.

    :param str chaine: chaÃ®ne Ã  mesurer
    :return: longueur de la chaÃ®ne en pixels (int)
    """
    global __canevas
    return __canevas.tkfont.measure(chaine)


def hauteur_texte():
    """
    Donne la hauteur en pixel nÃ©cessaire pour afficher du texte.

    :return: hauteur en pixels (int)
    """
    global __canevas
    return __canevas.tkfont.height


#############################################################################
# Effacer
#############################################################################

def efface_tout():
    """
    Efface la fenÃªtre.
    """
    global __canevas
    global __img
    __img.clear()
    __canevas.canvas.delete("all")


def efface(objet):
    """
    Efface ``objet`` de la fenÃªtre.

    :param: objet ou Ã©tiquette d'objet Ã  supprimer
    :type: ``int`` ou ``str``
    """
    global __canevas
    if objet in __img:
        del __img[objet]
    __canevas.canvas.delete(objet)


def efface_marque():
    """
    Efface la marque crÃ©Ã©e par la fonction :py:func:``marque``.
    """
    efface('marque')


#############################################################################
# Utilitaires
#############################################################################


def attente_clic():
    """Attend que l'utilisateur clique sur la fenÃªtre et renvoie un triplet ``(
    x, y, type_clic)``, oÃ¹ ``x`` et ``y`` sont l'abscisse et l'ordonnÃ©e du
    point cliquÃ©, et type_clic une chaÃ®ne valant ``'ClicGauche'`` ou
    ``'ClicDroit'`` selon le type de clic effectuÃ©.

    :return: un triplet ``(x, y, 'ClicDroit')``, ``(x, y,
    'ClicGauche')``
    """
    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if type_ev == "ClicDroit" or type_ev == "ClicGauche":
            return clic_x(ev), clic_y(ev), type_ev
        mise_a_jour()


def attente_touche():
    """
    Attend que l'utilisateur appuie sur une touche.
    """
    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if type_ev == "Touche":
            return touche(ev)
        mise_a_jour()

def attente_touche_jusqua(milliseconds):
    """
    Attend que l'utilisateur clique sur la fenÃªtre pendant le temps indiquÃ©
    """
    t1=time()+milliseconds/1000
    while time()<t1:
        ev=donne_evenement()
        typeEv=type_evenement(ev)
        if typeEv=="Touche":
            return touche(ev)
        mise_a_jour()
    return None


def attente_clic_ou_touche():
    """
    Attend que l'utilisateur clique sur la fenÃªtre ou appuie sur une touche.
    La fonction renvoie un triplet de la forme ``(x, y, type)`` si l'Ã©vÃ©nement
    est un clic de souris de type ``type`` et de coordonnÃ©es ``(x, y)``, ou (-1,
    touche, type) si l'Ã©vÃ©nement est un appui sur la touche ``val``.

    :return: ``(x, y, 'ClicDroit')``, ``(x, y, 'ClicGauche')`` ou
    ``(-1, val,\ 'Touche')``

    """
    while True:
        ev = donne_evenement()
        type_ev = type_evenement(ev)
        if "Clic" in type_ev:
            return clic_x(ev), clic_y(ev), type_ev
        elif type_ev == "Touche":
            return -1, touche(ev), type_ev
        mise_a_jour()


def clic():
    """
    Attend que l'utilisateur clique sur la fenÃªtre, sans rÃ©cupÃ©rer les
    dÃ©tails de l'Ã©vÃ©nement.
    """
    attente_clic()


def capture_ecran(file):
    """
    Fait une capture d'Ã©cran sauvegardÃ©e dans ``file.png``.
    """
    global __canevas
    __canevas.canvas.postscript(file=file + ".ps", height=__canevas.height,
                                width=__canevas.width, colormode="color")
    subprocess.call(
        "convert -density 150 -geometry 100% -background white -flatten",
        file + ".ps", file + ".png", shell=True)
    subprocess.call("rm", file + ".ps", shell=True)


#############################################################################
# Gestions des Ã©vÃ¨nements
#############################################################################

def donne_evenement():
    """ 
    Renvoie l'Ã©vÃ©nement associÃ© Ã  la fenÃªtre.
    """
    global __canevas
    if __canevas is None:
        raise FenetreNonCree(
            "La fenÃªtre n'a pas Ã©tÃ© crÃ©e avec la fonction \"cree_fenetre\".")
    if len(__canevas.eventQueue) == 0:
        return "RAS", ""
    else:
        return __canevas.eventQueue.pop()


def type_evenement(evenement):
    """ 
    Renvoie une chaÃ®ne donnant le type de ``evenement``. Les types
    possibles sont 'ClicDroit', 'ClicGauche', 'Deplacement', 'Touche' ou 'RAS'.
    """
    nom, ev = evenement
    return nom


def clic_x(evenement):
    """ 
    Renvoie la coordonnÃ©e X associÃ© Ã  ``evenement`` qui doit Ãªtre de type
    'ClicDroit' ou 'ClicGauche' ou 'Deplacement'
    """
    nom, ev = evenement
    if not (nom == "ClicDroit" or nom == "ClicGauche" or nom == "Deplacement"):
        raise TypeEvenementNonValide(
            'On ne peut pas utiliser "clic_x" sur un Ã©vÃ¨nement de type', nom)
    return ev.x


def clic_y(evenement):
    """ 
    Renvoie la coordonnÃ©e Y associÃ© Ã  ``evenement``, qui doit Ãªtre de type
    'ClicDroit' ou 'ClicGauche' ou 'Deplacement'.
    """
    nom, ev = evenement
    if not (nom == "ClicDroit" or nom == "ClicGauche" or nom == "Deplacement"):
        raise TypeEvenementNonValide(
            'On ne peut pas utiliser "clic_y" sur un Ã©vÃ¨nement de type', nom)
    return ev.y


def touche(evenement):
    """ 
    Renvoie une string correspondant Ã  la touche associÃ© Ã  ``evenement``
    qui doit Ãªtre de type 'Touche'.
    """
    nom, ev = evenement
    if not (nom == "Touche"):
        raise TypeEvenementNonValide(
            'On peut pas utiliser "touche" sur un Ã©vÃ¨nement de type', nom)
    return ev.keysym