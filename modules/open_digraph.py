from tkinter.filedialog import Open
from modules.matrice import *
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
        '''renvoie une matrice d’adjacence du graphe'''
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

    def display(self, verbose=False):
        """
        save the current graph and display it
        """
        self.save_as_dot_file("tmp_files/tmp.dot", verbose)
        if os.name == 'nt':
            os.system("dot -Tpdf tmp_files/tmp.dot -o tmp_files/tmp.pdf")
            os.system("START tmp_files/tmp.pdf") # fonctionne pour le cmd prompt de windows
        else:
            os.system("dot -Tpdf tmp_files/tmp.dot -o tmp_files/tmp.pdf")
            os.system("firefox tmp_files/tmp.pdf")

    def copy(self):
        '''return a copy of the graph'''
        return open_digraph(self.inputs.copy(), self.outputs.copy(), [n.copy() for n in self.nodes.values()])

    def is_cyclic(self):
        b = self.copy()
        b.outputs = []
        b.inputs = []
        if b.get_node_ids() == []:
            return False
        for node in b.get_nodes():
            if node.get_children_ids() == []: #and len(node.get_parent_ids()) > 0
                a = b.copy()
                a.remove_node_by_id(node.get_id())
                return a.is_cyclic()

        return True

    def max_id(self):
        """
        return minimal id from the graph
        """
        max = -1
        for i in self.get_node_ids():
            if i > max:
                max = i
        return max
        
    def min_id(self):
        """
        return maximal id from the graph
        """
        if self.get_node_ids() == []:
            return -1
        min = self.get_node_ids()[0]
        for i in self.get_node_ids():
            if i < min:
                min = i
        return min

    def shift_indices(self, n):
        """
        add n to every khey in the graph
        """
        for nod in self.get_nodes():
            nod.parents = incrDictKey(nod.parents, n)
            nod.children = incrDictKey(nod.children, n)
            nod.id += n
        self.nodes = incrDictKey(self.nodes, n)
        self.lastNewId += n
        self.inputs = list(map(lambda x: x + n, self.inputs))
        self.outputs = list(map(lambda x: x + n, self.outputs))

    def iparallel(self,l):
        """
        add g to self. self is modified, not g in l .
        l : list of open_digraph
        """
        def sub_iparallel(g):
            b = g.copy()
            b.shift_indices(self.max_id() + 1)
            self.outputs.extend(b.outputs)
            self.inputs.extend(b.inputs)
            self.nodes.update(b.nodes)
        for g in l:
            sub_iparallel(g)

            
    def parallel(self,l):
        """
        add parallel composition g to self. neither self and l are modified.
        """
        a = self.copy()
        a.iparallel(l)
        return a  

    def icompose(self, g):
        '''
        le transforme en la composee avec g
        fait f = gof
        les noeuds de sortie de f et ceux d entrer de g fusionne
        '''
        print(self.get_input_ids())
        print(g.get_output_ids())
        if len(self.get_output_ids()) != len(g.get_input_ids()):
            raise Exception("f n as pas autant de sortie que g a d entrée")
        b = g.copy()
        b.shift_indices(self.max_id() + 1)
        for i in range(len(self.get_input_ids())):
            print(b.get_output_ids()[i])
            self.get_node_by_id(self.get_input_ids()[i]).add_parent_id(b.get_output_ids()[i])
            b.get_node_by_id(b.get_output_ids()[i]).add_child_id(self.get_input_ids()[i])
        self.nodes.update(b.nodes)
        self.inputs = b.get_input_ids()


    def compose(self, g):
        b = self.copy()
        return b.icompose(g) 

    '''l idee c qu on parcours une fois le graph pr chaque input 
    on note chaque noeud avec la place du input dans la liste
    si un noeud a deja une valeur dans le dict on join les deux valeurs ensemble 
    avec la plus petite valeur
    '''
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
        graphe de d ́epart
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

def incrDictKey(dic, n):
    '''add n to every khey in the dic'''
    return {i + n: dic[i] for i in dic}