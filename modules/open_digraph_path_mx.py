class open_digraph_path_mx:
    def chemin_plus_cours_ancetre_commun(self, id1, id2):
        """
        Trouve la plus petite longueur entre id1 et id2 et chaque
        ancetre commun a ces deux noeuds
        id1, id2 : int nodes id
        return : dict{ancetres: (longueur id1, longueur id2)}
        """
        a, aUseless = self.Dijkstra(id1, direction=-1)
        b, bUseless = self.Dijkstra(id2, direction=-1)
        dict = {}
        for id in self.get_node_ids():
            if id in a and id in b:
                dict[id] = (a[id], b[id])
        return dict

    def tri_topologique(self):
        """
        realise le tri topologique compresse vers le haut du graphe
        """
        def sub_tri_topologique(a, l):
            if a.get_node_ids() == []:
                return l
            l2 = []
            for id in a.get_node_ids():
                if a.get_node_by_id(id).get_parent_ids() == []:
                    l2.append(id)
            
            if l2 == []:
                raise Exception("self est cyclique")

            a.remove_nodes_by_id(l2)
            l.append(l2)
            return sub_tri_topologique(a, l)
        return sub_tri_topologique(self.copy(), [])

    def profondeur_noeud(self, id):
        """
        Donne la profondeur du noeud id en se servant du tri topologique
        """
        l = self.tri_topologique()
        for i in range(len(l)):
            if id in l[i]:
                return i

    def profondeur_graph(self):
        """
        Donne la profondeur du graphe en se servant du tri topologique
        """
        return len(self.tri_topologique()) - 1

    def distances_la_plus_longue(self, id1, id2):
        """
        Renvoi la plus grande distance et le plus long chemin entre les noeuds id1 et id2
        """
        l = self.tri_topologique()
        n = 0
        for i in range(len(l)):
            if id1 in l[i]:
                n = i
                break

        dis = {id1:0}
        prev = {}
        for i in range(n+1, len(l)):
            if id2 in l[i]:
                break
            for id in l[i]:
                max = -1
                idmax = -1
                for id_parent in self.get_node_by_id(id).get_parent_ids():
                    if id_parent in dis:
                        if dis[id_parent] > max:
                            max = dis[id_parent]
                            idmax = id_parent
                if max != -1:
                    dis[id] = max+1
                    prev[id] = idmax
        
        max = -1
        l = [id2]
        for id_parent in self.get_node_by_id(id2).get_parent_ids():
            if id_parent in dis:
                if dis[id_parent] > max:
                    max = dis[id_parent]
                    l = [id_parent]+l

        while (l[0] != id1):
            l = [prev[l[0]]] + l
        
        return max+1, prev

    def Dijkstra(self, src, direction=None, tgt=None):
        """
        Apply the Dijkstera algorithm to the node src
        src : node id (int)
        direction : None (child and parents) or -1 (only parents) or 1 (only children)
        tgt : utility parameter only used for shortest_path, do not use !
        """
        Q = [src]
        dist = {src:0}
        prev = {}
        while(Q != []):
            u = min(Q, key=lambda v:dist[v])
            Q.remove(u)
            if u == tgt:
                return dist, prev
            neighbours = []
            if direction == None or direction == -1: # on cherche dans les parents
                neighbours += self.get_node_by_id(u).get_parent_ids()
            if direction == None or direction == 1: # on cherche dans les enfants
                neighbours += self.get_node_by_id(u).get_children_ids()
            for v in neighbours:
                if not v in dist:
                    Q += [v]
                if not v in dist or dist[u] > dist[u] + 1:
                    dist.update({v:dist[u] + 1})
                    prev.update({v:u})
        if(direction != None):
            del dist[src]
        return dist, prev

    def shortest_path(self, src, tgt):
        """
        Find the shortest_path between src ang tgt
        src : id of the source node
        tgt : id of the target node
        return : list [src, x1, ..., xn, tgt]
        """
        d, p = self.Dijkstra(src, tgt=tgt)
        res = [tgt]
        i = tgt
        while(i != src):
            res = [p[i]] + res
            i = p[i]
        return res



