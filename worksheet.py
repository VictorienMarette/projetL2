from modules.open_digraph import *
from modules.matrice import *
import inspect

#TD1

myGraph = open_digraph([0], [2], [node(0, 'i0', {}, {2:1}), node(2, 's', {0:1}, {})])
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

g = open_digraph.random(5, 3, inputs=2, outputs=1, form='oriented')
print(g)

d = open_digraph([0], [3], [node(0, 'i0', {}, {1:1}),
                            node(1, 'L-A', {0:1}, {2:3}),
                            node(2, 'Victorien', {1:3}, {3:1}),
                            node(3, 'Jolan', {2:1}, {})])
d.save_as_dot_file("test.dot", verbose=True)
