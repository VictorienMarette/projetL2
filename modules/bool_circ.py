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

    """
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
"""