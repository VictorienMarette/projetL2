from tkinter.filedialog import Open
from modules.matrice import *
from modules.open_digraph import *
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

def parse_parentheses(s : str) -> bool_circ:
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