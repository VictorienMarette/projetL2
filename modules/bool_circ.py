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
    for char in s:    
        if char == '(':
            g.nodes[current_node].label += s2
            g.add_node(children={current_node:1})
            current_node = g.lastNewId
            s2 = ''
        elif char == ')':
            g.nodes[current_node].label += s2
            current_node = g.get_node_by_id(current_node).get_children_ids()[0]
            s2 = ''
        else:
            s2 += char
    return g