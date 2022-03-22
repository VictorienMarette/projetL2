class open_digraph_predicate_mx:
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