from tkinter.filedialog import Open
from modules.matrice import *
from modules.open_digraph_composition_mx import *
from modules.open_digraph_path_mx import *
from modules.open_digraph_predicate_mx import *
import random
import os

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

    def indegree(self):
        '''return the input degree of the node'''
        res = 0
        for nod in self.parents:
            res += self.parents[nod]
        return res

    def outdegree(self):
        '''return the output degree of the node'''
        res = 0
        for nod in self.children:
            res += self.children[nod]
        return res

    def degree(self):
        '''return the degree of the node'''
        return self.indegree() + self.outdegree()

class open_digraph(open_digraph_composition_mx, open_digraph_path_mx, open_digraph_predicate_mx): # for open directed graph
    def __init__(self, inputs, outputs, nodes):
        '''
        inputs: int list; the ids of the input nodes
        outputs: int list; the ids of the output nodes
        nodes: node iter;
        '''
        self.inputs = inputs
        self.outputs = outputs
        self.nodes = {node.id:node for node in nodes} # self.nodes: <int,node> dict
        self.idAffichage = 0 # pour gerer l affichage
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
    def empty(cls):
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
        self.nodes.pop(id)

    def remove_nodes_by_id(self, listOfId):
        '''
        apply remove_node_by_id for all the id in listOfId
        listOfId : list of int (the ids)
        '''
        for id in listOfId:
            self.remove_node_by_id(id)

    def add_node(self, label='', parents=None, children=None):
        '''
        Add a new node to the graph
        label : label for the new node
        parents : int->int dict; map the new node's parents id to their multiplicity
        childrens : int->int dict; map the new node's children id to their multiplicity
        '''
        if parents == None:
            parents =  {}
        if children == None:
            children = {}
        newId = self.new_id() # On choisit un nouvel id
        self.lastNewId = newId # On actualise le dernier id attribue
        newNode = node(newId, label, parents, children)
        self.nodes.update({newId:newNode}) # On ajoute le nouveau noeud au graph

        # Mise a jour des autres noeuds

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
    def random(cls, n, bound, inputs=0, outputs=0, form="free"):
        '''
        return a new random graph
        form =
            free : graph libre
            DAG : graph dirige acyclique
            oriented : graph oriente
            loop-free : pas de regle sur les loops
            undirected : graph non dirige
            loop-free undirected : non dirige sans regle sur les loops
        '''
        g = open_digraph([], [], [])
        if form=="free":
            g = graph_from_adjacency_matrix(random_int_matrix(n, bound, null_diag=True))
        elif form=="DAG":
            g = graph_from_adjacency_matrix(random_triangular_int_matrix(n, bound, null_diag=True))
        elif form=="oriented":
            g = graph_from_adjacency_matrix(random_oriented_int_matrix(n, bound, null_diag=True))
        elif form=="loop-free": # ne serait ce pas plutot loop free oriented ?
            g = graph_from_adjacency_matrix(random_int_matrix(n, bound, null_diag=False))
        elif form=="undirected":
            g = graph_from_adjacency_matrix(random_symetric_int_matrix(n, bound, null_diag=True))
        elif form=="loop-free undirected":
            g = graph_from_adjacency_matrix(random_symetric_int_matrix(n, bound, null_diag=False))

        for i in range(inputs):
            id = random.randint(0, n-1)
            g.add_input_node("i" + str(i), id)
        for j in range(outputs):
            id = random.randint(0, n-1)
            g.add_output_nodes("o" + str(j), id)
        return g
            

    def random_unique_index(self):
        '''
        renvoie un dictionnaire, associant a chaque id de noeud un unique entier 0 =< i < n
        '''
        l = [i for i in range(len(self.get_node_ids()))]
        m = self.get_node_ids()
        d = {}
        while len(l) > 0:
            i = int(random.random()*len(l))
            d[m.pop()] = l.pop(i)
        return d

    def adjacency_matrix(self):
        '''renvoie une matrice d adjacence du graphe'''
        l = []
        d = self.random_unique_index()
        for i in range(len(self.get_node_ids())):
            l.append([])
            n = self.get_node_by_id(d[i])
            for j in range(len(self.get_node_ids())):
                if d[j] in n.get_children_ids():
                    l[i].append(n.children[d[j]])
                else:
                    l[i].append(0)
        return l

    def save_as_dot_file(self, path, verbose=False):
        """
        save the current graph to a dot file
        path: place the save the .dot
        verbose: true if the id must appear in the graph
        """
        f = open(path, "w")
        f.write("digraph G {\n")
        for Node in self.nodes:
            n = self.get_node_by_id(Node)
            if(verbose):
                f.write(f'    v{n.get_id()} [label="{n.get_label()}, id {Node}"]\n')
            else:
                f.write(f'    v{n.get_id()} [label="{n.get_label()}"]\n')
        for Node in list(self.get_nodes()):
            for c in Node.children:
                for i in range(Node.children[c]):
                    f.write(f'    v{Node.get_id()} -> v{c} \n')
        f.write("}")
        f.close()

    def display(self, verbose=False, name="tmp"):
        """
        save the current graph and display it
        """
        if name == "tmp":
            name = name + str(self.idAffichage)
            self.idAffichage += 1
        self.save_as_dot_file(f"tmp_files/{name}.dot", verbose)
        if os.name == 'nt':
            os.system(f"dot -Tpdf tmp_files/{name}.dot -o tmp_files/{name}.pdf")
            os.system(f"START tmp_files/{name}.pdf") # fonctionne pour le cmd prompt de windows
        else:
            os.system(f"dot -Tpdf tmp_files/{name}.dot -o tmp_files/{name}.pdf")
            os.system(f"firefox tmp_files/{name}.pdf")

    def copy(self):
        '''return a copy of the graph'''
        return open_digraph(self.inputs.copy(), self.outputs.copy(), [n.copy() for n in self.nodes.values()])

    def connected_components(self):
        '''
        envoie le nombre de composantes connexes, et un dictionnaire
        qui associe `a chaque id de noeuds du graphe un int qui correspond `a une
        composante connexe
        '''
        dic = {}

        def parcours(noeud, i):
            if noeud.get_id() in dic:
                if dic[noeud.get_id()] != i:
                    j = dic[noeud.get_id()]
                    for id in dic:
                        if dic[id] == i:
                            dic[id] = j
                    i = j
            else:
                dic[noeud.get_id()] = i
            for id in noeud.get_children_ids():
                parcours(self.get_node_by_id(id), i)

        for i in range(len(self.get_input_ids())):
            #permet d avoir le plus petit indice possible
            index_sub_graph = 0
            for j in range(i):
                if dic[self.get_input_ids()[j]] >= index_sub_graph:
                    index_sub_graph = dic[self.get_input_ids()[j]] +1
            parcours(self.get_node_by_id(self.get_input_ids()[i]), index_sub_graph)

        if dic == {}:
            return 0, {}
        #max([dic[id] for id in self.get_input_ids()]) + 1  est le nombre de sous graphs
        return max([dic[id] for id in self.get_input_ids()]) + 1 , dic

    def get_connected_components(self):
        '''
        qui renvoie une
        liste d open_digraphs, chacun correspondant `a une composante connexe du
        graphe de depart
        '''
        n, dic = self.connected_components()
        l = [open_digraph([],[],[]) for i in range(n)]
        for id in dic:
            l[dic[id]].nodes.update({id:self.get_node_by_id(id)})
            if id in self.get_output_ids():
                l[dic[id]].get_output_ids().append(id)
            if id in self.get_input_ids():
                l[dic[id]].get_input_ids().append(id)
        return l 

    def fusion_deux_noeud(self, id1, id2, label = None):
        '''
        fusionne deux noeuds dont les id
        id1 , id2: ids des noeuds
        label parametre optionnel permet de definir le label de la fusion
        (le noeud fusione a l id du premier noeud)
        '''
        parents1 = self.get_node_by_id(id1).parents
        children1 = self.get_node_by_id(id1).children
        parents2 = self.get_node_by_id(id2).parents
        children2 = self.get_node_by_id(id2).children
        for id in parents2:
            if id in parents1:
                n = max(parents1[id], parents2[id])
            else:
                n = parents2[id]
            for i in range(n):
                self.add_edge(id, id1)
        
        for id in children2:
            if id in children1:
                n = max(children1[id], children2[id])
            else:
                n = children2[id]
            for i in range(n):
                self.add_edge(id1, id)
        
        if label != None:
            self.get_node_by_id(id1).label = label
        self.remove_node_by_id(id2)


    
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
        d.lastNewId = n-1
    return d

def from_dot_file(path, nombre_espace_tab=4):
    nodes = {}
    f = open(path, "r")
    lines = f.readlines()[1:][:-1]
    for l in lines:
        nl = l[(nombre_espace_tab+1):][:-2]  
        try:
            i = int(nl[0])
        except:
            print("pas un int")
        if not i in nodes.keys():
            nodes[i] = node(i, '', {}, {})

        if nl[2] == "[":
            nodes[i].set_label(nl[10:][:-1])

        elif nl[2] == "-":
            nl = nl[1:]
            while nl != "":
                nl = nl[5:]
                try:
                    j = int(nl[0])
                except:
                    print("pas un int")
                if not j in nodes.keys():
                    nodes[j] = node(j, '', {}, {})
                if nodes[i].isDirectParent(j):
                    nodes[i].children[j] += 1
                    nodes[j].parents[i] += 1
                else:
                    nodes[i].add_child_id(j)
                    nodes[j].add_parent_id(i)
                
                i = j
                nl = nl[1:]
            
    return open_digraph([],[],nodes.values())