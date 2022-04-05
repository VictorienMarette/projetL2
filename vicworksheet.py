from sympy import true
from lib2to3.pytree import Node
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *
import inspect

"""d = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1,5:1}),
                    node(1, 'i1', {}, {2:1}),
                    node(2, 'n2', {0:1, 1:1}, {3:2}),
                    node(3, 'n3', {2:2}, {5:1}),
                    node(5, 'n4', {3:1,0:1}, {4:1}),
                    node(4, 'o4', {5: 1}, {})]
                    )
#d.display(verbose=True)"""
def sub_total(i1, i2,j1,j2, K):
    Xl = len(K)
    Yl = len(K[0])
    tot = 0
    tot2 = 0
    for i in range(i1,i2+1):
        for j in range(j1,j2+1):
            if K[i%(Xl-1)][j%(Yl-1)] == 1:
                tot += 1
            if K[i%(Xl-1)][j%(Yl-1)]:
                tot2 += 1
            
    return tot, tot2

K = K_map("1110001000111111")
sub_total(2, 2, 0, 1, K)
#print(K_to_f_propositionel(K))