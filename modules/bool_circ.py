from tkinter.filedialog import Open
from modules.matrice import *
from open_digraph import *
import random
import os

class bool_circ(open_digraph): # a subclass of open_digraph

    def __init__(self, g):
        """
        g : open_digraph
        """
        return g