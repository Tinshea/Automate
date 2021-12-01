# -*- coding: utf-8 -*-
import re
from transition import *
from state import *
import os
import copy
from itertools import permutations, product
from automateBase import AutomateBase



class Automate(AutomateBase):
        
    def succElem(self, state, lettre):
        """State x str -> list[State]
        rend la liste des états accessibles à partir d'un état
        state par l'étiquette lettre
        """
        successeurs = []
        # t: Transitions
        for t in self.getListTransitionsFrom(state):
            if t.etiquette == lettre and t.stateDest not in successeurs:
                successeurs.append(t.stateDest)
        return successeurs


    def succ (self, listStates, lettre):
        """list[State] x str -> list[State]
        rend la liste des états accessibles à partir de la liste d'états
        listStates par l'étiquette lettre
        """
        tableau = []
        for i in listStates:
                tableau+=self.succElem(i,lettre)
        return list(set(tableau))
        




    """ Définition d'une fonction déterminant si un mot est accepté par un automate.
    Exemple :
            a=Automate.creationAutomate("monAutomate.txt")
            if Automate.accepte(a,"abc"):
                print "L'automate accepte le mot abc"
            else:
                print "L'automate n'accepte pas le mot abc"
    """
    @staticmethod
    def accepte(auto,mot) :
        """ Automate x str -> bool
        rend True si auto accepte mot, False sinon
        """
        #parcours la liste 
        L=auto.getListInitialStates()
        for i in mot:
           L=auto.succ(L,i) #permet de voir les etats possible avec une lettre 
    
        for j in L: # regarde si parmis L il y a un etat final
            if j.fin:
                return True

        return False 


    @staticmethod
    def estComplet(auto,alphabet) :
        """ Automate x str -> bool
         rend True si auto est complet pour alphabet, False sinon
        """

        for j in auto.listStates: #On prend la liste d etat de l'automate
            for i in alphabet:
                 # on regarde si dans chaque etat on a un etat accesible pour chaque lettre de l'alphabet  
                if auto.succElem(j,i)==[]: #si il rend la liste vide cela veut dire qu'il n'a pas trouvé de sucesseur 
                    return False
        return True 


        
    @staticmethod
    def estDeterministe(auto) :
        """ Automate  -> bool
        rend True si auto est déterministe, False sinon
        """
        #on recupere l'alphabet de l automate
        alphabet=set()
        for k in auto.listTransitions:
            alphabet.add(k.etiquette)
            
        for j in auto.listStates: #On prend la liste d etat de l'automate
            for i in alphabet:
                 L=auto.succElem(j,i) #on recupere le/les succeseurs d'un état state par l'étiquette lettre
                 if len(L)>=2: #si il a 2 ou plus de 2 succceuseur c'est qu'il n'est pas determinste
                    return False
        return True 


        

       
    @staticmethod
    def completeAutomate(auto,alphabet) :
        """ Automate x str -> Automate
        rend l'automate complété d'auto, par rapport à alphabet
        """
        
        s0 = State(0, True, False)
        t1 = Transition(s0,"a",s0)
        return

       

    @staticmethod
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """


        return
        
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
              
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        return

    @staticmethod
    def union (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        return
        

   
       

    @staticmethod
    def concatenation (auto1, auto2):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage la concaténation des langages des deux automates
        """
        return
        
       
    @staticmethod
    def etoile (auto):
        """ Automate  -> Automate
        rend l'automate acceptant pour langage l'étoile du langage de a
        """
        return




