class node:
    def __init__(self, identity, label, parents, children):
        '''
        identity: int; its unique id in the graph
        label: string;
        parents: int->int dict; maps a parent node's id to its multiplicity
        children: int->int dict; maps a child node's id to its multiplicity
        '''
        self.id = identity
        self.label = label
        self.parents = parents
        self.children = children
    
    def __eq__(self, p):
        '''surcharge de l'operateur d'egalite'''
        if self.id != p.id:
            return False
        if self.label != p.label:
            raise Exception("Les Noeuds sont egaux mais n'ont pas le meme Label")
        if self.parents != p.parents:
            raise Exception("Les Noeuds sont egaux mais n'ont pas le meme dict parents")
        if self.children != p.children:
            raise Exception("Les Noeuds sont egaux mais n'ont pas le meme dict enfants")
        return True

    def get_id(self):
        '''get the id of the node'''
        return self.id
    
    def get_label(self):
        '''get the label of the node'''
        return self.label
    
    def get_parent_ids(self):
        '''get the list of the parents id'''
        return self.parents.keys()

    def get_children_ids(self):
        '''get the list of the children id'''
        return self.children.khey()

    def set_id(self, i):
        '''set the id of the node'''
        self.id = i

    def set_label(self, label):
        '''set the label of the node'''
        self.label = label

    def set_parents_ids(self, parents):
        '''set the parents ids'''
        self.parents = parents

    def set_children_ids(self, children):
        '''set the children ids'''
        self.children = children

    def add_child_id(self, child):
        '''add/update a child id'''
        self.children.update({child.id:child})

    def add_parent_id(self, parent):
        '''add/update a parent id'''
        self.children.update({parent.id:parent})

    def __str__(self):
         return self.label + " " + str(self.id) + " " + str(self.children) + " " + str(self.parents)

    def __repr__(self):
        return str(self)

    def copy(self):
        '''return a copy of the node'''
        return node(self.id, self.label, self.parents.copy(), self.children.copy())


class open_digraph: # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict

    #Pour les getter on renvoi des copies et non les pointeurs
    def get_input_ids(self):
        """get the input ids"""
        return self.inputs.copy()
    
    def get_output_ids(self):
        """get the output ids"""
        return self.outputs.copy()

    def get_id_node_map(self):
        """get the id:node dic"""
        return self.node.copy()

    def get_nodes(self):
        """get the nodes list"""
        return self.nodes.values()  

    def get_node_ids(self):
        """get the nodes id list"""
        return self.nodes.keys()

    def get_node_by_id(self, id):
        """get the node with the ID id"""
        return self.nodes[id]

    def get_nodes_by_ids(self, idList):
        """"get the nodes list with ID in idList"""
        return [self.get_node_by_id(id) for id in idList]

    def set_input_ids(self, inputs):
        """set the inputs list"""
        self.inputs = inputs

    def add_input_id(self, id):
        """add an id to the input list"""
        self.inputs.append(id)

    def set_output_ids(self, outputs):
        """set the outputs list"""
        self.outputs = outputs

    def add_output_id(self, id):
        """add an id to the outputs list"""
        self.outputs.append(id)

    def __str__(self):
        res = ""
        for n in(self.nodes):
            res += self.nodes[n].label + " "
        return res
    
    def __repr__(self):
        return str(self)

    @classmethod
    def empty():
        """return an empty graph"""
        return open_digraph([], [], [])

    def copy(self):
        """return a copy of the graph"""
        return open_digraph(self.inputs.copy(), self.outputs.copy(), [n.copy() for n in self.nodes.values()])