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
    def determinisation(auto) :
        """ Automate  -> Automate
        rend l'automate déterminisé d'auto
        """
        #EZ Clap https://tenor.com/view/pepe-clap-clapping-applause-gif-10184275

        #On crée l'état initial et l'ajoute à l'automate résultat
        compteID = 0
        listeInit = auto.getListInitialStates()
        etatInitial : State = State(compteID, True, False, str(listeInit))

        #L'état initial est aussi final si un de ses états l'est
        for etat in listeInit :
            if etat.fin:
                etatInitial.fin = True
                break

        #On crée l'automate résultat avec notre état initial
        autoRes = Automate(listStates = [etatInitial], listTransitions = [],label ="")

        #On récupère l'alphabet de l'automate
        alphabet = auto.alphabet()

        #On crée notre dico ID de l'ensemble d'états : liste des états contenus dans notre ensemble d'états
        dicoListe = {0 : listeInit}

        #Ensemble des états dont on doit calculer les transitions crées
        aTraiterEns = {etatInitial}
        #Ensemble des états déjà vu, donc à ne pas recalculer
        deja_vu = set()
        #Pour stocker tous les nouveaux états à calculer
        tempEtats = set()
        #Un état temp pour nos calculs
        etatTemp : State = etatInitial

        while aTraiterEns != set():
            #Tant qu'on a des nouveaux états à traiter
            for aTraiterEtat in aTraiterEns:
                for lettre in alphabet:
                    listeSucc = auto.succ(dicoListe[aTraiterEtat.id] ,lettre)
                    #Liste des successeurs

                    labelEtat = str(listeSucc) #Calcul du label de l'état

                    for etat in autoRes.listStates:
                        #On regarde si l'état avec le label correspondant existe déjà
                        if etat.label == labelEtat:
                            etatTemp = etat
                            break
                    if etatTemp.label != labelEtat:
                        #Si le label ne match pas, c'est qu'on n'a pas trouvé d'état correspondant
                        compteID+=1
                        #On incrémente l'ID et crée l'état
                        etatTemp : State = State(compteID, False, False, str(listeSucc))
                        dicoListe[compteID]=listeSucc
                        #On stocke la liste des états correspondants à l'ID dans notre dictionnaire
                        for etat in listeSucc:
                            #On rend l'état final s'il contient au moins un état final
                            if etat.fin:
                                etatTemp.fin = True
                                break


                    autoRes.addTransition(Transition(aTraiterEtat, lettre, etatTemp))
                    #On crée la transition de l'état aTraiter à l'état suivant
                    tempEtats.add(etatTemp)
                    #On ajoute le nouvel état à notre ensemble des successeurs à calculer

            deja_vu = deja_vu | aTraiterEns
            #Les ensembles qu'on a traité deviennent déjà vu
            aTraiterEns = tempEtats - deja_vu
            #Les prochains états à calculer sont les successeurs
            #moins ceux déjà visités
            tempEtats = set()


        return autoRes


        
            
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




