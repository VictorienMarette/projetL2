from matrice import *

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
    
    # On ne renvoi pas d'exception dans les cas ou il n'y a pas de liaisons

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
        if self.nodes == {}:
            self.lastNewId = 0
        else:
            self.lastNewId = max(list(self.nodes.keys())) # on garde toujours un id superieur a tous les autres
                                                        # (pas forcemment le max)
    def get_input_ids(self):
        '''get the input ids'''
        return self.inputs
    
    def get_output_ids(self):
        '''get the output ids'''
        return self.outputs

    def get_id_node_map(self):
        '''get the id:node dict'''
        return self.nodes

    # fonction perso
    def get_nodes_dict(self):
        '''get the nodes dict'''
        return self.nodes

    def get_nodes(self):
        '''get the nodes list'''
        return self.nodes.values()  

    def get_node_ids(self):
        '''get the nodes id list'''
        return list(self.nodes.keys())

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
        for n in(self.nodes.values()):
            res += f"Node({str(n)})\n"
        return res
    
    def __repr__(self):
        return str(self)

    @classmethod
    def empty():
        '''return an empty graph'''
        return open_digraph([], [], [])

    def new_id(self):
        '''return a new id for the graph'''
        return self.lastNewId + 1

    def add_edge(self, src, tgt):
        '''add an edge from node with id src to node with id tgt'''
        listOfId = self.get_node_ids()
        if src not in listOfId or tgt not in listOfId:
            raise Exception("Les id passes en argument ne correspondent a aucun noeud")
        srcNode = self.get_node_by_id(src)
        tgtNode = self.get_node_by_id(tgt)
        if(srcNode.isDirectParent(tgt)): # Si un lien existe deja
            tgtNode.parents[src] += 1
            srcNode.children[tgt] += 1
        else: # Si le lien n'existe pas
            srcNode.add_child_id(tgt)
            tgtNode.add_parent_id(src)

    def remove_edge(self, src, tgt): # Question : Faut il retirer un noeud du graph s'il a 0 liaisons avec le reste ?
        '''remove one edge from node with id src to node with id tgt'''
        #l'edge est enlevé
        self.get_node_by_id(src).remove_child_once(tgt)
        self.get_node_by_id(tgt).remove_parent_once(src)
        #on regarde si l'edge existe encore
        if src in self.get_input_ids() and len(self.get_node_by_id(src).get_children_ids()) != 1:
            raise Exception("Le noeud " + str(src) + " est un inputs mais n'a pas un unique enfant")
        if tgt in self.get_output_ids() and len(self.get_node_by_id(tgt).get_parent_ids()) != 1:
            raise Exception("Le noeud " + str(src) + " est un output mais n'a pas un unique parent")

    def remove_edges(self, list):
        '''
        apply remove_edge to the argments list = [src, tgt]
        list : (int, int) pairs (src, tgt)
        '''
        for p in list:
            self.remove_edge(p[0], p[1])        

    def remove_parallel_edges(self, src, tgt): # Meme question
        '''remove all edge from node with id src to node with id tgt'''
        #les edges sont enlevé
        self.get_node_by_id(src).remove_child_id(tgt)
        self.get_node_by_id(tgt).remove_parent_id(src)
        #on regarde si l'edge existe encore
        if src in self.get_input_ids() and len(self.get_node_by_id(src).get_children_ids()) != 1:
            raise Exception("Le noeud " + str(src) + " est un inputs mais n'a pas un unique enfant")
        if tgt in self.get_output_ids() and len(self.get_node_by_id(tgt).get_parent_ids()) != 1:
            raise Exception("Le noeud " + str(src) + " est un output mais n'a pas un unique parent")

    def remove_parallel_edges_2(self, list):
        '''
        apply remove_parallel_edge to the argument list = [src, tgt]
        list : (int, int) pairs (src, tgt)
        '''
        for p in list:
            self.remove_parallel_edges(p[0], p[1])

    def remove_node_by_id(self, id):
        '''remove a node from the open_disgraphe'''
        parents = self.get_node_by_id(id).get_parent_ids()
        childrens = self.get_node_by_id(id).get_children_ids()
        #remove outputs inputs
        if id in self.outputs:
            self.outputs.remove(id)
        if id in self.inputs:
            self.inputs.remove(id)
        #remove edges
        for children in childrens:
            self.remove_parallel_edges(id, children)
        for parent in parents:
            self.remove_parallel_edges(parent, id)

    def remove_nodes_by_id(self, listOfId):
        '''
        apply remove_node_by_id for all the id in listOfId
        listOfId : list of int (the ids)
        '''
        for id in listOfId:
            self.remove_node_by_id(id)

    def add_node(self, label='', parents={}, children={}):
        '''
        Add a new node to the graph
        label : label for the new node
        parents : int->int dict; map the new node's parents id to their multiplicity
        childrens : int->int dict; map the new node's children id to their multiplicity
        '''
        newId = self.new_id() # On choisit un nouvel id
        self.lastNewId = newId # On actualise le dernier id attribue
        newNode = node(newId, label, parents, children)
        self.nodes.update({newId:newNode}) # On ajoute le nouveau noeud au graph

        # Mise a jour des autres noeuds

        # Si le noeud est entrant
        if parents == {}:
            self.inputs.append(newId)
            for idChildren in children:
                if idChildren in self.inputs:
                    self.inputs.remove(idChildren)
        # Si le noeud est sortant
        if children == {}:
            self.outputs.append(newId)
            for idParent in parents:
                if idParent in self.outputs:
                    self.outputs.remove(idParent)

        # Dans tous les cas
        for idParent in parents:
            # Ajout dans les parents
            parentNode = self.get_node_by_id(idParent)
            parentNode.add_child_id(newId)
            parentNode.children[newId] = parents[idParent]

        for idChildren in children:
            # Ajout dans les enfants
            childNode = self.get_node_by_id(idChildren)
            childNode.add_parent_id(newId)
            childNode.parents[newId] = children[idChildren]


    def is_well_formed(self):
        '''
        Check if the graph is well formed.
        Les conditions sur un graph pour etre correct sont decrites dans le sujet du TP2
        '''
        
        for idInNode in self.inputs:
            # Condition 1
            if not idInNode in self.nodes:
                return False
            # Condtion 2
            node = self.get_node_by_id(idInNode)
            if len(node.children) != 1 or node.parents != {} or list(node.children.values()) != [1]:
                return False
            
        for idOutNode in self.outputs:
            # Condition 1
            if not idOutNode in self.nodes:
                return False
            # Condition 3
            node = self.get_node_by_id(idOutNode)
            if len(node.parents) != 1 or node.children != {} or list(node.parents.values()) != [1]:
                return False
       
        # Condition 4
        for id in self.get_nodes_dict():
            if self.get_nodes_dict()[id].get_id() != id:
                return False

        
        # Condition 5
        for jid in self.get_nodes_dict(): # on regarde chaque noeud
            j = self.get_node_by_id(jid)

            # on regarde ses enfants
            for iid in j.children:
                i = self.get_node_by_id(iid)
                if not i.isDirectChild(jid) or i.parents[jid] != j.children[iid]:
                    return False

            # on regarde ses parents
            for iid in j.parents:
                i = self.get_node_by_id(iid)
                if not i.isDirectParent(jid) or i.children[jid] != j.parents[iid]:
                    return False

        # on a tout teste
        return True
            
    def add_input_node(self, label, id):
        '''
        Create a new input node
        Raise exception if the node id doesnt exists
        Raise exception if the node id is a graph entry
        '''
        if not id in self.get_node_ids():
            raise Exception("Le noeud id n'existe pas")
        if id in self.get_input_ids():
            raise Exception("Le noeud id est deja une entree du graph")
        newId = self.new_id()
        self.lastNewId = newId
        Node = node(newId, label, {}, {id:1})
        self.get_node_by_id(id).add_parent_id(newId)
        self.add_input_id(newId)
        self.nodes.update({newId: Node})

    def add_output_nodes(self, label, id):
        '''
        Create a new output node
        Raise exception if the node id doesnt exists
        Raise exception if the node id is a graph exit
        '''
        if not id in self.get_node_ids():
            raise Exception("Le noeud id n'existe pas")
        if id in self.get_output_ids():
            raise Exception("Le noeud id est deja une sortie du graph")
        newId = self.new_id()
        self.lastNewId = newId
        Node = node(newId, label, {id:1}, {})
        self.get_node_by_id(id).add_child_id(newId)
        self.add_output_id(newId)
        self.nodes.update({newId: Node})

    @classmethod
    def random(n, bound, inputs=0, outputs=0, form="free"):
        '''
        
        '''
        if form=="free":
            return graph_from_adjacency_matrix
        elif form=="DAG":
            ...
        elif form=="oriented":
            ...
        elif form=="loop-free":
            ...
        elif form=="undirected":
            ...
        elif form=="loop-free undirected":
            return False

    def copy(self):
        '''return a copy of the graph'''
        return open_digraph(self.inputs.copy(), self.outputs.copy(), [n.copy() for n in self.nodes.values()])






def graph_from_adjacency_matrix(mat):
    '''
    return the graph corresponding to the matrix mat
    '''
    n = len(mat)
    d = open_digraph([], [], [])
    for i in range(n):
        parents = {}
        children = {}
        for j in range(n):
            if mat[i][j] != 0:
                children.update({j:mat[i][j]})
            if mat[j][i] != 0:
                parents.update({j:mat[j][i]})
        nod = node(i, 'n' + str(i), parents, children)
        d.nodes.update({i:nod})
    return d