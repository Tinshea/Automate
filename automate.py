# -*- coding: utf-8 -*-
from enum import auto
import itertools
import re
from transition import *
from state import *
import os
import copy
from itertools import permutations, product
from automateBase import AutomateBase


#Malek Bouzarkouna 28706508
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
        #methode utilisé : https://youtu.be/_hQQG1NJzzw
        if(Automate.estDeterministe(auto)):  # si l'automate est deterministe on renvoie une copie de l'automate
            return auto
        alphabet = auto.getAlphabetFromTransitions()
        Ls= [set(auto.getListInitialStates())]
        ListeTransition = []
        pro = [set(auto.getListInitialStates())]

        while len(pro)!=0:  # on reste tant que tous les ensembles etats ne sont pas traiter

            for state in pro:  # parcours la liste des états
                pro.remove(state)#on retire le cas que l'on va traité 
                for i in alphabet:  # parcours  l'alphabet
                    succ = set(auto.succ( state, i))

                    if succ not in Ls:  # si l'ensemble d'etats successeur n'est pas dans Liste_State on le rajoute dans la liste et on le met dans tmp pour le traiter plus tard
                        Ls.append(succ)
                        pro.append(succ)

                    init = False  # si tout les etats sont initiale il deviendra vrai

                    l1 = "{"
                    # creer l'etiquette(label) de l'ensemble de l'etat s
                    for k in state:
                        l1 += k.label+","
                        init = init and k.init  # verifie si tout les etats sont initiales 

                    # remplace le dernier "," par "}"
                    l1 = l1[:(len(l1)-1)]+"}"

        
                    etat = State(Ls.index(state), init,# L'etat initial
                                  State.isFinalIn(state), l1)

                    l2 = "{"
                    # creer l'etiquette(label) de l'ensemble de l'etat successeur
                    for k in succ:
                        l2 += k.label+","
                    l2 = l2[:(len(l2)-1)]+"}"

                    # si label vide 
                    if(l2 == "}"):
                        l2 = "Poubelle" #creation d'un etat Poubelle

                    
                    etat1 = State(Ls.index(succ),# L'etat successeur
                                  False, State.isFinalIn(succ), l2)

                    ListeTransition.append(
                        Transition(etat, i, etat1))

        return Automate(ListeTransition)
    
         
            
    @staticmethod
    def complementaire(auto,alphabet):
        """ Automate -> Automate
        rend  l'automate acceptant pour langage le complémentaire du langage de a
        """
        #methode utilisé : https://youtu.be/POXhkDUhfnQ

        #Il faut que notre automate soit complet et deteministe
        auto1=copy.deepcopy(auto)
        if not Automate.estComplet(auto1,alphabet):
            auto1=Automate.completeAutomate(auto1,alphabet)
                
        if not Automate.estDeterministe(auto1):
            auto1=Automate.determinisation(auto1)  

        #On remplace les etat finals en etat normaux et les etats normaux en finals 
        for j in auto1.listStates:
            j.fin=not j.fin
        
        return auto1
   
    @staticmethod
    def intersection (auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'intersection des langages des deux automates
        """
        #methode utilisé : https://youtu.be/buovn-iusmw

        #On fait le produit cartésien des étatde la l'auto0 et l'auto 1
        liste=list(product(auto0.listStates, auto1.listStates))
        alphabet = auto0.getAlphabetFromTransitions()
        listfinal = []
        # parcoure l'alphabet
        for i in alphabet:
            for auto0_s0, auto0_s1 in liste:
                # crée l'etat s , si s0 et s1 sont final alors on a un etat final , si s0 et s1 sont initial alors on a un etat initial et si on a les deux à un etat final initial
                s= State(liste.index((auto0_s0, auto0_s1)), (auto0_s0.init and auto0_s1.init),(auto0_s0.fin and auto0_s1.fin), "("+auto0_s0.label+","+auto0_s1.label+")")

                # on reparcoure la liste d'etats, si les transitions i sont dans auto0 et auto1 on ajoute la transition dans l
                for auto0_succ0, auto1_succ1 in liste:
                    # Si la transition est bien ds auto0 et dans auto1 on créer la transition
                    if( (Transition(auto0_s0, i,  auto0_succ0) in auto0.listTransitions) and (Transition(auto0_s1, i, auto1_succ1) in auto1.listTransitions)):
                        Sdest = State(liste.index(( auto0_succ0, auto1_succ1)), ( auto0_succ0.init and auto1_succ1.init), ( auto0_succ0.fin and auto1_succ1.fin),"("+ auto0_succ0.label+","+auto1_succ1.label+")")  # crée l'etat destination
                        listfinal.append(Transition(s, i, Sdest))

        return Automate(listfinal)


    @staticmethod
    def union(auto0, auto1):
        """ Automate x Automate -> Automate
        rend l'automate acceptant pour langage l'union des langages des deux automates
        """
        Liste_Transition = []

        if(len(set(auto0.listStates).intersection(auto1.listStates)) == 0):  # si S1 inter S2 = vide on créer directement l'automate avec l'ensemble des transition de chaque automates
            Liste_Transition = auto0.listTransitions + auto1.listTransitions
            return Automate(Liste_Transition)

        else:
            LS = list(product(auto0.listStates, auto1.listStates))
            alphabet = auto0.getAlphabetFromTransitions()
            for i in alphabet:
                for auto0_s0, auto1_s1 in LS:

                    State_Src = State(LS.index(
                        (auto0_s0,auto1_s1)), (auto0_s0.init and auto1_s1.init), (auto0_s0.fin or auto1_s1.fin), "("+auto0_s0.label+","+auto1_s1.label+")")
                    for etat_succ0, etat_succ1 in LS:

                        # si les transitions sont bien dans auto0 et dans auto1 alors on ajoute la transition dans Liste_Transition
                        if((Transition(auto1_s1, i, etat_succ0) in auto0.listTransitions) and (Transition(auto1_s1,i, etat_succ1) in auto1.listTransitions)):
                            State_dest = State(LS.index((etat_succ0, etat_succ1)), (etat_succ0.init and etat_succ1.init), (
                                etat_succ0.fin or etat_succ1.fin), "("+etat_succ0.label+","+etat_succ1.label+")")
                            Liste_Transition.append(Transition(
                                State_Src, i, State_dest))

            return Automate(Liste_Transition)
     
       
    @staticmethod
    def etoile(auto):
        """rend l'automate acceptant pour langage l'étoile du langage de l'automate"""
        cpy=copy.deepcopy(auto)
        #liste de toutes les transitions dans cpy.listTransition si transition.stateDest est dans la liste des états initiaux de cpy
        finalTransitions = [transition for transition in cpy.listTransitions if transition.stateDest in cpy.getListFinalStates()]

        for state in cpy.getListInitialStates():
            for transition in finalTransitions:
                cpy.addTransition(Transition(transition.stateSrc, transition.etiquette, state))

        cpy.addState(State(151,True,True,"j"))

        return cpy


