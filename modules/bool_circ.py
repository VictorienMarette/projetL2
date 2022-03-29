from sre_parse import Verbose
from tkinter.filedialog import Open
from tokenize import String
from modules.matrice import *
from modules.open_digraph import *
from math import log2
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
