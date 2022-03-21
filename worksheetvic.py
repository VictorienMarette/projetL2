from sympy import true
from lib2to3.pytree import Node
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *
import inspect

g = open_digraph([0,1,2], [8], [node(0, 'x1', {}, {3:1}),
                             node(1, 'x2', {}, {4:1}),
                             node(2, 'x3', {}, {5:1}),
                             node(3, '&', {0:1, 4:1}, {7:1}),
                             node(4, '', {1:1}, {3:1, 5:1}),
                             node(5, '|', {2:1, 4:1}, {6:1}),
                             node(6, '~', {5:1}, {7:1}),
                             node(7, '|', {3:1, 6:1}, {8:1}),
                             node(8, 'out', {7:1}, {})])

d4 = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1,5:1}),
                    node(1, 'i1', {}, {2:1}),
                    node(2, 'n2', {0:1, 1:1}, {3:2}),
                    node(3, 'n3', {2:2}, {5:1}),
                    node(5, 'n4', {3:1,0:1}, {4:1}),
                    node(4, 'o4', {5: 1}, {})]
                    )

n = d4.distances_la_plus_longue(0,3)
n = print(n)