from sympy import true
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
                ch = my_childrens[0]
                self.add_node(str((int(my_parent.get_label()) + 1)%2), {},{ch:1})
                self.remove_node_by_id(idNon)

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

    def regle_associativite_XOR(self, id_father, id_child):
        node_father = self.get_node_by_id(id_father)
        node_child = self.get_node_by_id(id_child)
        if(not node_father.isDirectParent(id_child) or not node_child.isDirectChild(id_father)):
            raise ValueError("Pas parents directs")
        for pr in node_father.get_parent_ids():
            self.add_edge(pr, id_child)
        self.remove_node_by_id(id_father)

    def regle_associativite_copie(self, id_father, id_child):
        node_father = self.get_node_by_id(id_father)
        node_child = self.get_node_by_id(id_child)
        if(not node_father.isDirectParent(id_child) or not node_child.isDirectChild(id_father)):
            raise ValueError("Pas parents directs")
        for ch in node_child.get_children_ids():
            self.add_edge(id_father, ch)
        self.remove_node_by_id(id_child)

    def regle_involution_XOR(self, id_father, id_child):
        node_father = self.get_node_by_id(id_father)
        node_child = self.get_node_by_id(id_child)
        if(not node_father.isDirectParent(id_child) or not node_child.isDirectChild(id_father)):
            raise ValueError("Pas parents directs")
        while(node_father.isDirectParent(id_child) and node_father.children[id_child] >= 2):
            self.remove_edge(id_father, id_child)
            self.remove_edge(id_father, id_child)

    def regle_effacement(self, id_father, id_child):
        node_father = self.get_node_by_id(id_father)
        node_child = self.get_node_by_id(id_child)
        if(not node_father.isDirectParent(id_child) or not node_child.isDirectChild(id_father)):
            raise ValueError("Pas parents directs")
        for pr in node_father.get_parent_ids():
            self.add_node("", {pr:1}, {})
        self.remove_node_by_id(id_child)
        self.remove_node_by_id(id_father)

    def regle_non_a_travers_XOR(self, id_father, id_child):
        node_father = self.get_node_by_id(id_father)
        node_child = self.get_node_by_id(id_child)
        if(not node_father.isDirectParent(id_child) or not node_child.isDirectChild(id_father)):
            raise ValueError("Pas parents directs")
        pr = node_father.get_parent_ids()[0]
        self.add_edge(pr, id_child)
        self.remove_node_by_id(id_father)
        ch = node_child.get_children_ids()[0]
        self.add_node("~", {id_child:1}, {ch:1})
        self.remove_edge(id_child, ch)

    def regle_non_a_travers_copie(self, id_father, id_child):
        node_father = self.get_node_by_id(id_father)
        node_child = self.get_node_by_id(id_child)
        if(not node_father.isDirectParent(id_child) or not node_child.isDirectChild(id_father)):
            raise ValueError("Pas parents directs")
        for ch in node_child.get_children_ids():
            self.add_node("~", {id_child:1}, {ch:1})
        pr = node_father.get_parent_ids()[0]
        self.add_edge(pr, id_child)
        self.remove_node_by_id(id_father)
        self.remove_edge(id_child, ch)
        print(self.idAffichage)

    def regle_involution_du_non(self, id_father, id_child):
        node_father = self.get_node_by_id(id_father)
        node_child = self.get_node_by_id(id_child)
        if(not node_father.isDirectParent(id_child) or not node_child.isDirectChild(id_father)):
            raise ValueError("Pas parents directs")
        pr = node_father.get_parent_ids()[0]
        ch = node_child.get_children_ids()[0]
        self.add_edge(pr, ch)
        self.remove_node_by_id(id_father)
        self.remove_node_by_id(id_child)

   #co feuille = noeud qui a des enfants mais pas de parents
    def evaluate(self, display = False, verbose = False):
        flag = True
        while flag:
            flagDisplay = False
            flag = False
            for id in self.get_node_ids():
                if(id in self.get_node_ids()):
                    # au cas ou le noeud n'a pas ete suppr de la liste mais suppr du graph
                    myNode = self.get_node_by_id(id)
                    if myNode.get_parent_ids() == []:
                        # le noeud n'a pas de parent
                        if myNode.get_children_ids() == []:
                            self.remove_node_by_id(id)
                            if(display):
                                self.display(verbose=verbose)
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
                                if(display):
                                    self.display(verbose=verbose)
                            elif(str_op == "&"):
                                self.regle_porte_et(id_op, idEntre)
                                flag = True
                                if(display):
                                    self.display(verbose=verbose)
                            elif(str_op == "|"):
                                self.regle_porte_ou(id_op, idEntre)
                                flag = True
                                if(display):
                                    self.display(verbose=verbose)
                            elif(str_op == "^"):
                                self.regle_porte_ou_exclusif(id_op, idEntre)
                                flag = True
                                if(display):
                                    self.display(verbose=verbose)
                            elif(str_op == "~"):
                                self.regle_porte_non(id_op, idEntre)
                                flag = True
                                if(display):
                                    self.display(verbose=verbose)
                    else:
                        
                        # le noeud a forcement des parents
                        if myNode.get_children_ids() != []:
                            str_father = myNode.get_label()
                            if(str_father == "^"):
                                ch = myNode.get_children_ids()[0]
                                myChild = self.get_node_by_id(ch)
                                if(myChild.get_label() == "^"):
                                    self.regle_associativite_XOR(id, ch)
                                    flag = True
                                    if(display):
                                        self.display(verbose=verbose)
                            # bug
                            if(str_father == ""):
                                for idn in myNode.get_children_ids():
                                    if idn in self.get_node_ids():
                                        n = self.get_node_by_id(idn)
                                        if n.get_label() == "":
                                            self.regle_associativite_copie(id, idn)
                                            flag = True
                                            if(display):
                                                self.display(verbose=verbose)
                                        if(n.get_label() == "^" and idn in myNode.children and myNode.children[idn] >= 2):
                                            self.regle_involution_XOR(id, n.get_id())
                                            flag = True
                                            if(display):
                                                self.display(verbose=verbose)
                            # endbug
                            if(str_father == "~"):
                                ch = myNode.get_children_ids()[0]
                                myChild = self.get_node_by_id(ch)
                                str_child = myChild.get_label()
                                if(str_child == "^"):
                                    self.regle_non_a_travers_XOR(id, ch)
                                    flag = True
                                    if(display):
                                        self.display(verbose=verbose)
                                elif(str_child == ""):
                                    self.regle_non_a_travers_copie(id, ch)
                                    flag = True
                                    if(display):
                                        self.display(verbose=verbose)
                                elif(str_child == "~"):
                                    self.regle_involution_du_non(id, ch)
                                    flag = True
                                    if(display):
                                        self.display(verbose=verbose)
                        elif myNode.get_label() == "":
                            print(myNode.get_id())
                            self.regle_effacement(myNode.get_parent_ids()[0], id)
                            flag = True
                            if(display):
                                self.display(verbose=verbose)