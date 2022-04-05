from sre_parse import Verbose
from tkinter.filedialog import Open
from tokenize import String
from modules.matrice import *
from modules.open_digraph import *
<<<<<<< HEAD
import math
=======
from math import log2
>>>>>>> 7e5b141fca7d49de6ea6fa099879e879d1741a2c
import random
import os

class bool_circ(open_digraph): # a subclass of open_digraph

    def __init__(self, g):
        """
        g : open_digraph
        """
        super().__init__(g.inputs.copy(), g.outputs.copy(), g.nodes.values())

    def is_well_formed(self):

        # Condition sur les degrees
        for theNode in self.get_nodes():

            if(theNode.get_label() == '&' and theNode.outdegree() != 1):
                return False
            elif(theNode.get_label() == '|' and theNode.outdegree() != 1):
                return False
            elif(theNode.get_label() == '^' and theNode.outdegree() != 1):
                return False
            elif(theNode.get_label() == '~' and (theNode.indegree() != 1 or theNode.outdegree() != 1)):
                return False
            elif(theNode.get_label() == '' and theNode.indegree() != 1):
                return False

        return not self.is_cyclic()

    @classmethod
    def synteseDes1(cls, strB: String):
        k = 0
        nbEntrees = int(log2(len(strB)))
        res = open_digraph.empty()
        listOfGraph = []
        for i in range(0, len(strB)):
            if strB[i] == '1':
                b = open_digraph([], [], [])
                b.add_node('&') #noeud d'id 1
                x = [-1]*nbEntrees
                for j in range(nbEntrees):
                    bol = int(int(i)/2**(nbEntrees - int(j) - 1)) % 2 == 1
                    if bol:
                        b.add_node('', {}, {1:1})
                        b.add_input_node(f"x{j}", b.lastNewId)
                    else:
                        b.add_node('~', {}, {1:1})
                        b.add_node('', {}, {b.lastNewId:1})
                        b.add_input_node(f"x{j}", b.lastNewId)
                    
                listOfGraph.append(b)
        res.iparallel(listOfGraph)
        entree_unique = False
        while not entree_unique:
            entree_unique = True
            for i1 in range(len(res.get_input_ids())):
                for i2 in range(i1+1, len(res.get_input_ids())):
                    id1 = res.get_input_ids()[i1]
                    id2 = res.get_input_ids()[i2]
                    if res.get_node_by_id(id1).get_label() == res.get_node_by_id(id2).get_label():
                        a = res.get_node_by_id(id1).get_children_ids()[0]
                        b = res.get_node_by_id(id2).get_children_ids()[0]
                        res.fusion_deux_noeud(a, b)
                        res.remove_node_by_id(id2)
                        entree_unique = False
                        break
        nodeIdRes = res.get_node_ids()
        tab = [nodeIdRes[i] for i in range(len(nodeIdRes)) if res.get_node_by_id(nodeIdRes[i]).get_label() == '&']
        res.add_node('|', {ind:1 for ind in tab}, None)
        return bool_circ(res)
                
                


def parse_parentheses(*strings : str) -> bool_circ:

    def sub_parse_parentheses(s : str) -> bool_circ:
        g = bool_circ(open_digraph([], [], []))
        g.add_node()
        g.add_output_nodes('', 1)
        current_node = 1
        s2 = ''
        labelList = {} # {label : id list}
        for char in s:    
            if char == '(':
                g.nodes[current_node].label += s2
                g.add_node(children={current_node:1})
                if not s2 in ['', '&', '|', '^', '~']:
                    if s2 in labelList:
                        labelList[s2] += current_node
                    else:
                        labelList.update({s2:[current_node]})
                current_node = g.lastNewId
                s2 = ''
            elif char == ')':
                g.nodes[current_node].label += s2
                if not s2 in ['', '&', '|', '^', '~']:
                    if s2 in labelList:
                        labelList[s2] += [current_node]
                    else:
                        labelList.update({s2:[current_node]})
                current_node = g.get_node_by_id(current_node).get_children_ids()[0]
                s2 = ''
            else:
                s2 += char
        for lab in labelList:
            l = labelList[lab]
            while len(l) != 1:
                g.fusion_deux_noeud(l[0], l[1], label=lab)
                l.remove(l[1])
            g.add_input_node(lab, l[0])
            g.get_node_by_id(l[0]).set_label('')
        return g

    g = bool_circ(open_digraph([], [], []))
    g.iparallel([sub_parse_parentheses(s) for s in strings])
    entree_unique = False
    while entree_unique == False:
        entree_unique = True
        for i1 in range(len(g.get_input_ids())):
            for i2 in range(i1+1, len(g.get_input_ids())):
                id1 = g.get_input_ids()[i1]
                id2 = g.get_input_ids()[i2]
                if g.get_node_by_id(id1).get_label() == g.get_node_by_id(id2).get_label():
                    g.fusion_deux_noeud(g.get_node_by_id(id1).get_children_ids()[0], g.get_node_by_id(id2).get_children_ids()[0])
                    g.remove_node_by_id(id2)
                    entree_unique = False
                    break
    return g

def code_de_grey(n):
    if n == 1:
        return ["0","1"]
    
    l = code_de_grey(n-1)
    newl = []

    lm = len(l)
    for k in range(lm):
        newl.append("0"+l[k])
    for k in range(lm):
        newl.append("1"+l[lm-1-k])

    return newl


def K_map(s):
    n = int(math.log(len(s), 2))
    l1 = code_de_grey(int(n/2))
    l2 = code_de_grey(n - int(n/2))

    l = []

    for x in range(len(l1)):
        l.append([int(s[int(l1[x] + l2[y], 2)]) for y in range(len(l2))])

    return l
    
"""def K_to_f_propositionel(K):
    Xl = len(K)
    o = int(math.log(Xl, 2))
    Yl = len(K[0])
    p = int(math.log(Xl, 2))

    def sub_total(i1, i2,j1,j2):
        tot = 0
        tot2 = 0
        for i in range(i1,i2+1):
            for j in range(j1,j2+1):
                if K[i%Xl][j%Yl] == 1:
                    tot += 1
                if K[i%Xl][j%Yl]:
                    tot2 += 1
                
        return tot, tot2

    n = 0
    for x in range(Xl):
        for y in range(Yl):
            n += K[x][y]

    l = []

    while n > 0:
        max = 0
        s_l = [0,0,0,0]

        for i in range(1,o+1):
            for j in range(1,p+1):
                for x in range(Xl):
                    for y in range(Yl):
                        s1,s2 = sub_total(x,x+2**i-1, y, y+2**j-1)
                        if s1 > max and s2 == 2**(i+j):
                            s_l = [x,(x+2**i-1)%Xl, y, (y+2**j-1)%Yl]
                            max = s1
        
        l.append(s_l.copy())
        for i in range(s_l[0],s_l[1]+1):
            for j in range(s_l[2],s_l[3]+1):
                K[i%Xl][j%Yl] = -1
        n += -max
        print(n)

    return l"""
