class open_digraph_composition_mx:
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
        def incrDictKey(dic, n):
            '''add n to every khey in the dic'''
            return {i + n: dic[i] for i in dic}
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
            self.lastNewId = b.lastNewId
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
        if len(self.get_input_ids()) != len(g.get_output_ids()):
            raise Exception("f n as pas autant de sortie que g a d entrée")
        b = g.copy()
        self.shift_indices(g.max_id() + 1)
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