
from sympy import true
from lib2to3.pytree import Node
from modules.open_digraph import *
from modules.matrice import *
from modules.bool_circ import *
import inspect

#TD1

"""myGraph = open_digraph([0], [2], [node(0, 'i0', {}, {2:1}), node(2, 's', {0:1}, {})])
# print(myGraph) il ne se passe rien
n = node(0, 'i0', {}, {2:1})

# print(myGraph)
# print(dir(open_digraph))
# print(dir(node))
print(myGraph.get_nodes())

print("Je deteste python")

d0 = open_digraph([0], [1], [node(0, 'i', {}, {1:2}), node(1, 'j', {0:2}, {})])
d0.add_node('new', {}, {0:2})
print(d0)

mat = random_symetric_int_matrix(3, 3)
afficheMatrix(mat)
graph = graph_from_adjacency_matrix(mat)
print(graph)

g = open_digraph.random(5, 3, inputs=2, outputs=1, form='undirected')
print(g)"""

"""circ = bool_circ(open_digraph([0, 1, 2], [8], [node(0, 'x1', {}, {3:1}),
                             node(1, 'x2', {}, {4:1}),
                             node(2, 'x3', {}, {5:1}),
                             node(3, '&', {0:1, 4:1}, {7:1}),
                             node(4, '', {1:1}, {3:1, 5:1}),
                             node(5, '|', {2:1, 4:1}, {6:1}),
                             node(6, '~', {5:1}, {7:1}),
                             node(7, '|', {3:1, 6:1}, {8:1}),
                             node(8, 'out', {7:1}, {})]))"""

g = open_digraph([0,1,2], [8], [node(0, 'x1', {}, {3:1}),
                             node(1, 'x2', {}, {4:1}),
                             node(2, 'x3', {}, {5:1}),
                             node(3, '&', {0:1, 4:1}, {7:1}),
                             node(4, '', {1:1}, {3:1, 5:1}),
                             node(5, '|', {2:1, 4:1}, {6:1}),
                             node(6, '~', {5:1}, {7:1}),
                             node(7, '|', {3:1, 6:1}, {8:1}),
                             node(8, 'out', {7:1}, {})])
#print(circ.is_cyclic())
#circ.display()
gg = open_digraph([0], [2], [
            node(0, 'i', {}, {1:1}), 
            node(1, 'j', {0:1}, {2:1}), 
            node(2, 'k', {1:1}, {})])

"""circ.display()

d5 = open_digraph([0, 1], [4], [
                    node(0, 'i0', {}, {2:1}),
                    node(1, 'i1', {}, {2:1}),
                    node(2, 'n2', {0:1, 1:1}, {3:2}),
                    node(3, 'n3', {2:2}, {5:1}),
                    node(5, 'n4', {3:1}, {4:1}),
                    node(4, 'o4', {5: 1}, {})]
                    )
d5.save_as_dot_file("test.dot")
r = from_dot_file("test.dot")

g.shift_indices(10)
print(g)
g.display(verbose=True)
print(g.is_well_formed())
"""

#circ.display()
#g.display()
a = gg.copy()
a.icompose(g)
a.display(verbose=True)
print(a)
#n ,dic = a.connected_components()
l = a.get_connected_components()
print(l[0])
print(l[1])