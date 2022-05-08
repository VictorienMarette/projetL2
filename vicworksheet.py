from sympy import true
from lib2to3.pytree import Node
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *
import inspect

g = bool_circ.encodeur()
d = bool_circ.int_to_bbc(10,4)
#d.display()
g.icompose(d)
g.evaluate()
g.display()