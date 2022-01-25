from modules.open_digraph import *
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