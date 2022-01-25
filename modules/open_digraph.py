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
        return list(self.parents.keys())

    def get_children_ids(self):
        '''get the list of the children id'''
        return list(self.children.keys())

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

    def add_child_id(self, id):
        '''add/update a child id
        Node id has to be a new child for self'''
        self.children.update({id:1})

    def add_parent_id(self, id):
        '''add/update a parent id
        Node id has to be a new parent for self'''
        self.parents.update({id:1})
    
    def remove_parent_once(self, id):
        '''remove a link to the parent with id'''
        if self.isDirectChild(id):
            self.parents[id] = self.parents[id] - 1
            if  self.parents[id] <= 0:
                del self.parents[id]

    def remove_child_once(self, id):
        '''remove a link to the children with id'''
        if self.isDirectParent(id):
            self.children[id] = self.children[id] - 1
            if  self.children[id] <= 0:
                del self.children[id]

    def remove_parent_id (self, id):
        '''remove all link to the parent with id'''
        if self.isDirectChild(id):
            del self.parents[id]

    def remove_child_id (self, id):
        '''remove all link to the children with id'''
        if self.isDirectParent(id):
            del self.children[id]

    def isDirectParent(self, id):
        '''check if node id is a direct child from self'''
        return id in self.children

    def isDirectChild(self, id):
        '''check if node id is a direct parent from self'''
        return id in self.parents

    def __str__(self):
         return self.label + " " + str(self.id) + " " + str(self.parents) + " " + str(self.children)

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
        self.sortedListOfId = sorted(self.nodes.keys()) # on garde toujours une liste triee
                                                        # des ID pour ne pas avoir a la recalculer a chaque fois

    #Pour les getter on renvoi des copies et non les pointeurs
    def get_input_ids(self):
        '''get the input ids'''
        return self.inputs
    
    def get_output_ids(self):
        '''get the output ids'''
        return self.outputs

    def get_id_node_map(self):
        '''get the id:node dic'''
        return self.nodes

    def get_nodes(self):
        '''get the nodes list'''
        return self.nodes.values()  

    def get_node_ids(self):
        '''get the nodes id list'''
        return self.sortedListOfId

    def get_node_by_id(self, id):
        '''get the node with the ID id'''
        return self.nodes[id]

    def get_nodes_by_ids(self, idList):
        '''get the nodes list with ID in idList'''
        return [self.get_node_by_id(id) for id in idList]

    def set_input_ids(self, inputs):
        '''set the inputs list'''
        self.inputs = inputs

    def add_input_id(self, id):
        '''add an id to the input list'''
        self.inputs.append(id)

    def set_output_ids(self, outputs):
        '''set the outputs list'''
        self.outputs = outputs

    def add_output_id(self, id):
        '''add an id to the outputs list'''
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
        '''return an empty graph'''
        return open_digraph([], [], [])

    def new_id(self):
        '''return a new id for the graph'''
        return self.sortedListOfId[-1] + 1

    def add_edge(self, src, tgt):
        '''add a link from node with id src to node with id tgt'''
        if src not in self.sortedListOfId or tgt not in self.sortedListOfId:
            raise Exception("Les id passes en argument ne correspondent a aucun noeud")
        srcNode = self.get_node_by_id(src)
        tgtNode = self.get_node_by_id(tgt)
        if(srcNode.isDirectParent(tgt)): # Si un lien existe deja
            tgtNode.parents[src] += 1
            srcNode.children[tgt] += 1
        else: # Si le lien n'existe pas
            srcNode.add_child_id(tgt)
            tgtNode.add_parent_id(src)

    def add_node(self, parents, children, label=''): # Attention pas meme signature que dans le sujet (pb)
        newId = self.newId() # On choisit un nouvel id
        self.sortedListOfId.append(newId) # On ajoute le nouvel id a la banque d'id
        newNode = node(newId, label, parents, children)
        self.nodes.update({newId:newNode}) # On ajoute le nouveau noeud au graph

        # Mise a jour des autres noeuds, demander au prof

    def remove_edge(self, src, tgt):
        '''remove one edge from src to tgt'''
        self.get_node_by_id(src).remove_child_once(tgt)
        if self.get_node_by_id(src).get_children_ids() == [] and not src in self.get_output_ids():
            self.get_output_ids().append(src)
        self.get_node_by_id(tgt).remove_parent_once(src)
        if self.get_node_by_id(tgt).get_parent_ids() == [] and not tgt in self.get_input_ids():
            self.inputs.append(tgt)


    def copy(self):
        '''return a copy of the graph'''
        return open_digraph(self.inputs.copy(), self.outputs.copy(), [n.copy() for n in self.nodes.values()])