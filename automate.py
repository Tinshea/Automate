# -*- coding: utf-8 -*-
from enum import auto
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
        if len(auto.getListInitialStates()) !=1:
            return False

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
        autocpy=copy.deepcopy(auto)#on copie l automate
        s = State(len(auto.listStates), False, False)#on cree un etat poubelle
        for j in auto.listStates: #On prend la liste d etat de l'automate
            for i in alphabet:
                 # on regarde si dans chaque etat on a un etat accesible pour chaque lettre de l'alphabet  
                if auto.succElem(j,i)==[]: #si il rend la liste vide cela veut dire qu'il n'a pas trouvé de sucesseur 
                     t = Transition(j,i,s)#on cree la transition manquante
                     autocpy.addState(s) #on ajoute l etat poubelle a lautomate
                     autocpy.addTransition(t)#et on ajouete la transition manquante
                     autocpy.addTransition(Transition(s,i,s))
        return autocpy

       

    @staticmethod
    def determinisation(auto):
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        if Automate.estDeterministe(auto):
            return auto
        # auto_d : Automate
        auto_d = copy.deepcopy(auto)
        # list_Tous_Etat: List[set(States)]
        list_Tous_Etat = [list(auto_d.getListInitialStates())] #recuperer tout les etats
        # list_transition : List[Transition]
        list_transition = [] #liste de transition
        #set_etat : set(State)
        for set_etat in list_Tous_Etat:
            #lettre: str
            for lettre in auto_d.getAlphabetFromTransitions():
                #verifie si la liste des successeurs n'est pas vide pour tous les etats pour la lettre donnée en parametre et qu'elle n'est pas dans la liste List_Tous_Etat
                if ((len(auto_d.succ(set_etat, lettre))) != [] and (list(auto_d.succ(set_etat, lettre))) not in list_Tous_Etat): 
                    list_Tous_Etat.append(list(auto_d.succ(set_etat, lettre))) #ajout de la liste successeur a la liste list_Tous_Etat
                # Etat_In: Bool
                Etat_In = False
                # Etat_Fin: Bool
                Etat_Fin = False
                if list(set_etat) == auto_d.getListInitialStates(): #met a jour etat s'il est initiale ou finale
                    Etat_In = True
                if list(set_etat) == auto_d.getListFinalStates():
                    Etat_Fin = True
                # Etat_Old: State
                Etat_Old = State((list_Tous_Etat.index(list(set_etat))), Etat_In, Etat_Fin) #creation de l'etat Etat_Old
                Etat_In = False
                Etat_Fin = False
                #etat : State
                for etat in auto_d.succ(set_etat, lettre): 
                    if etat in auto_d.getListFinalStates(): #met a jour etat
                        Etat_Fin = True
                # Etat_New: State
                Etat_New = State((list_Tous_Etat.index(list(auto_d.succ(set_etat, lettre)))), Etat_In, Etat_Fin) #creation de l'etat Etat_New
                # t: Transition
                t = Transition(Etat_Old, lettre, Etat_New) #creation de la transition
                if t not in list_transition:
                    list_transition.append(t) #ajoute la transition t dans la liste list_transition si t n'est pas dans la liste
        #auto_finale : Automate
        auto_f = Automate(list_transition)
        return auto_f


        
            
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        auto1=auto
        if not Automate.estComplet(auto1,alphabet):
            auto1=Automate.completeAutomate(auto1,alphabet)
                
        if not Automate.estDeterministe(auto1):
            auto1=Automate.determinisation(auto1)  

        for j in auto1.listStates:
            if j.fin ==False:
                j.fin=True
            else : 
                j.fin=False
        
        return auto1
   
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




