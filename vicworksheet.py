from sympy import true
from lib2to3.pytree import Node
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *
import inspect

g = bool_circ.encodeur()
d = bool_circ(open_digraph([],[0,1,2,3], [node(0,0,{},{}),node(1,1,{},{}), node(2,0,{},{}), node(3,1,{},{})]))
g.icompose(d)
g.display()
#g.evaluate()
#g.display()