from sympy import true
from lib2to3.pytree import Node
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *
import inspect

r = bool_circ.int_to_bbc(10, 4)
g = bool_circ.encodeur()
d = bool_circ.desencodeur()
"""g.icompose(r)
#d.icompose(g)
g.display()
g.evaluate()
g.display()"""
r2 = bool_circ.int_to_bbc(25, 7)
d.icompose(r2)
d.display()
d.evaluate()
d.display()

# On a pas fait la derniere question car bug et examen demain a 8h, desole