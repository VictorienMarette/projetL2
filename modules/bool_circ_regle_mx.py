from modules.open_digraph import open_digraph


class bool_circ_regle_mx(open_digraph):
    """
    methode des regles de simplification du TD11
    En general : id*typeDeNoeud* -> int node id
    idEntre -> int node id qui vaut 0 ou 1
    """
    def regle_copies(self, idCopie, idEntre):
        # idCopie pointe sur le noeud de copie
        # idEntre pointe sur le noeud d'entre (0 ou 1)
        my_node = self.get_node_by_id(idCopie)
        if my_node.get_label() == "":
            my_parent = self.get_node_by_id(idEntre)
            if my_parent.get_label() in ["0","1"]:
                my_childrens = my_node.get_children_ids()
                for ch in my_childrens:
                    self.add_node(my_parent.get_label(), {},{ch:1})
                self.remove_node_by_id(idEntre)
                self.remove_node_by_id(idCopie)

    def regle_porte_non(self, idNon, idEntre):
        # idNon pointe sur le noeud non
        my_node = self.get_node_by_id(idNon)
        if my_node.get_label() == "~":
            my_parent = self.get_node_by_id(idEntre)
            if my_parent.get_label() in ["0","1"]:
                my_childrens = my_node.get_children_ids()
                for ch in my_childrens:
                    self.add_node(str((int(my_parent.get_label()) + 1)%2), {},{ch:1})
                self.remove_node_by_id(id)

    def regle_porte_et(self, idEt, idEntre):
        # idEt pointe sur le noeud et
        my_node = self.get_node_by_id(idEt)
        if my_node.get_label() == "&":
            my_parent = self.get_node_by_id(idEntre)
            if my_parent.get_label() in ["0","1"]:
                my_childrens = my_node.get_children_ids()
                ch = my_childrens[0]
                if(my_parent.get_label() == "1"):
                    self.remove_node_by_id(my_parent.get_id())
                else:
                    self.add_node("0", {}, {ch:1})
                    self.remove_node_by_id(idEt)

    def regle_porte_ou(self, idOu, idEntre):
        # idEt pointe sur le noeud ou
        my_node = self.get_node_by_id(idOu)
        if my_node.get_label() == "|":
            my_parent = self.get_node_by_id(idEntre)
            if my_parent.get_label() in ["0","1"]:
                my_childrens = my_node.get_children_ids()
                ch = my_childrens[0]
                if(my_parent.get_label() == "0"):
                    self.remove_node_by_id(idEntre)
                else:
                    self.add_node("1", {}, {ch:1})
                    self.remove_node_by_id(idOu)

    def regle_porte_ou_exclusif(self, idOuExcl, idEntre):
        # idEt pointe sur le noeud ou exclusif
        my_node = self.get_node_by_id(idOuExcl)
        if my_node.get_label() == "^":
            my_parent = self.get_node_by_id(idEntre)
            if my_parent.get_label() in ["0","1"]:
                my_childrens = my_node.get_children_ids()
                ch = my_childrens[0]
                if(my_parent.get_label() == "0"):
                    self.remove_node_by_id(idEntre)
                else:
                    self.remove_node_by_id(idEntre)
                    self.remove_edge(idOuExcl, ch)
                    self.add_node("~", {idOuExcl:1}, {ch:1})

    def regle_element_neutre(self, idElem):
        # idElem est l'element neutre pointe
        my_node = self.get_node_by_id(idElem)
        if my_node.get_label() in ["|", "^"]:
            my_node.set_label("0")
        if my_node.get_label() == "&":
            my_node.set_label("1") 

   #co feuille = noeud qui a des enfants mais pas de parents
    def evaluate(self):
        flag = True
        while flag:
            flag = False
            for id in self.get_node_ids():
                if(id in self.get_node_ids()):
                    # le noeud n'a pas ete suppr
                    myNode = self.get_node_by_id(id)
                    if myNode.get_parent_ids() == []:
                        # le noeud n'a pas de parent et n'est pas un input
                        if myNode.get_children_ids() == []:
                            self.remove_node_by_id(id)
                            continue
                        if(myNode.get_label() not in ["0", "1"]):
                            self.regle_element_neutre(id)
                        elif not myNode.get_children_ids()[0] in self.get_output_ids():
                            if(len(myNode.get_children_ids()) > 1):
                                raise RuntimeError("Plus d'un enfant")
                            id_op = myNode.get_children_ids()[0]
                            idEntre = id
                            str_op = self.get_node_by_id(id_op).get_label()
                            if(str_op == ""):
                                self.regle_copies(id_op, idEntre)
                                flag = True
                            elif(str_op == "&"):
                                self.regle_porte_et(id_op, idEntre)
                                flag = True
                            elif(str_op == "|"):
                                self.regle_porte_ou(id_op, idEntre)
                                flag = True
                            elif(str_op == "^"):
                                self.regle_porte_ou_exclusif(id_op, idEntre)
                                flag = True
                            elif(str_op == "~"):
                                self.regle_porte_non(id_op, idEntre)
                                flag = True
                            # self.display()