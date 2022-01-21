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
        return self.id
    
    def get_label(self):
        return self.label
    
    def get_parent_ids(self):
        return self.parents

    def get_children_ids(self):
        return self.children

    def set_id(self, i):
        self.id = i

    def set_label(self, label):
        self.label = label

    def set_parents_ids(self, parents):
        self.parents = parents

    def set_children_ids(self, children):
        self.children = children

    def add_child_id(self, child):
        self.children.update({child.id:child})

    def add_parent_id(self, parent):
        self.children.update({parent.id:parent})

    def __str__(self):
         return self.label + " " + str(self.id) + " " + str(self.children) + " " + str(self.parents)

    def __repr__(self):
        return str(self)

    def copy(self):
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

    def get_input_ids(self):
        return self.inputs
    
    def get_output_ids(self):
        return self.outputs

    def get_id_node_map(self):
        return self.node

    def get_nodes(self):
        return self.nodes.values()  

    def get_node_ids(self):
        return self.nodes.keys()

    def get_node_by_id(self, id):
        return self.nodes[id]

    def set_input_ids(self, inputs):
        self.inputs = inputs

    def add_input_id(self, input):
        self.inputs.append(input)

    def set_output_ids(self, outputs):
        self.outputs = outputs

    def add_output_id(self, output):
        self.outputs.append(output)

    def __str__(self):
        res = ""
        for n in(self.nodes):
            res += self.nodes[n].label + " "
        return res
    
    def __repr__(self):
        return str(self)

    @classmethod
    def empty():
        return open_digraph([], [], [])

    def copy(self):
        return open_digraph(self.inputs.copy(), self.outputs.copy(), [n.copy() for n in self.nodes.values()])