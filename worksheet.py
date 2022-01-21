from modules.open_digraph import *

#TD1

#Exercice 4

myGraph = open_digraph([0], [2], [node(0, 'i0', {}, {2:1}), node(2, 's', {0:1}, {})])
# print(myGraph) il ne se passe rien
n = node(0, 'i0', {}, {2:1})

print(myGraph)