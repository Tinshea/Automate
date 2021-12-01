# -*- coding: utf-8 -*-
"""
Code modifiable.
"""

from automate import Automate
from state import State
from transition import Transition
from myparser import *



#Exo 2 Prise en main

#2.1 Creation d’automates

#1

s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, False, True)

t1 = Transition(s0,"a",s0)
t2 = Transition(s0,"b",s1)
t3 = Transition(s1,"a",s2)
t4 = Transition(s1,"b",s2)
t5 = Transition(s2,"a",s0)
t6 = Transition(s2,"b",s1)

print("Automate A")
auto = Automate([t1,t2,t3,t4,t5,t6])
print(auto)
auto.show("A_ListeTrans")

#2
auto1 = Automate([t1,t2,t3,t4,t5,t6], [s0,s1,s2])
print(auto1)
auto1.show("A_ListeTranscpy")
#l’automateauto1 est bien identique a l’automate auto

#3


#2.2 Premieres manipulations

#1
t = Transition(s0,"a",s1)
print(auto.removeTransition(t))
auto.removeTransition(t)
#la transition n'existait pas donc pas de modification
auto.show("A_ListeTrans+remove")

print(auto.addTransition(t))
auto.addTransition(t)
#la transition n'existait pas donc pas on a une transique de l'etat 0 a 1 a
auto.show("A_ListeTrans+add")

#2
auto.removeState(s1)
auto.addState(s1)
s2 = State(0, True, False)
auto.addState(s2)
print(auto)
auto.show("A_ListeTransstate")
#l'etat s1 n'a plus de transition il y'a plus de transition b 

#3
print("les transition de s1 sont")
auto1.getListTransitionsFrom(s1)
print(auto1.getListTransitionsFrom(s1))


#Exercice 3

#1 

print("les succ sont")
autosucc = Automate([t1,t2,t3,t4,t5,t6])
print(autosucc.succ([s0,s1,s2],'a'))
autosucc.show("test")


#2
print("accepté")
s0 = State(0, True, False)
s1 = State(1, False, False)
s2 = State(2, True, True)

t1 = Transition(s0,"a",s0)
t2 = Transition(s0,"b",s1)
t3 = Transition(s1,"a",s2)
t4 = Transition(s1,"b",s2)
t5 = Transition(s2,"a",s0)
t6 = Transition(s2,"b",s1)
t7 = Transition(s0,"a",s1)
autosaccept = Automate([t1,t2,t3,t4,t5,t6,t7])
print(autosaccept.accepte(autosaccept,"aabb"))
autosaccept.show("test2")
#3

print(autosucc.estComplet(auto,"ab"))