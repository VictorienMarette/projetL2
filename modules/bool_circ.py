from sre_parse import Verbose
from tkinter.filedialog import Open
from tokenize import String
from modules.bool_circ_regle_mx import bool_circ_regle_mx
from modules.matrice import *
from modules.open_digraph import *
import math

import math
from math import log2
import random
import os

class bool_circ(bool_circ_regle_mx): # a subclass of open_digraph

    def __init__(self, g):
        """
        g : open_digraph
        """
        super().__init__(g.inputs.copy(), g.outputs.copy(), g.nodes.values())

    def is_well_formed(self, printCondition = False):
        """
        verifie sur le graph est bien forme
        return : boolean
        """

        # Condition sur les degrees
        for theNode in self.get_nodes():

            if(theNode.get_label() == '&' and theNode.outdegree() != 1):
                if printCondition:
                    print("Condition 1")
                return False
            elif(theNode.get_label() == '|' and theNode.outdegree() != 1):
                if printCondition:
                    print("Condition 2")
                return False
            elif(theNode.get_label() == '^' and theNode.outdegree() != 1):
                if printCondition:
                    print("Condition 3")
                return False
            elif(theNode.get_label() == '~' and (theNode.indegree() != 1 or theNode.outdegree() != 1)):
                if printCondition:
                    print("Condition 4")
                return False
            elif(theNode.get_label() == '' and theNode.indegree() != 1):
                if printCondition:
                    print("Condition 5")
                return False
            elif((theNode.get_label() == '1' or theNode.get_label() == '0')  and (theNode.indegree() != 0 or theNode.outdegree() != 1)):
                return False

        return not self.is_cyclic()

    @classmethod
    def synteseDes1(cls, strB: String):
        k = 0
        nbEntrees = int(math.log2(len(strB)))
        res = open_digraph.empty()
        listOfGraph = []
        for i in range(0, len(strB)):
            if strB[i] == '1':
                b = open_digraph([], [], [])
                b.add_node('&') #noeud d'id 1
                x = [-1]*nbEntrees
                for j in range(nbEntrees):
                    bol = int(int(i)/2**(nbEntrees - int(j) - 1)) % 2 == 1
                    if bol:
                        b.add_node('', {}, {1:1})
                        b.add_input_node(f"x{j}", b.lastNewId)
                    else:
                        b.add_node('~', {}, {1:1})
                        b.add_node('', {}, {b.lastNewId:1})
                        b.add_input_node(f"x{j}", b.lastNewId)
                    
                listOfGraph.append(b)
        res.iparallel(listOfGraph)
        entree_unique = False
        while not entree_unique:
            entree_unique = True
            for i1 in range(len(res.get_input_ids())):
                for i2 in range(i1+1, len(res.get_input_ids())):
                    id1 = res.get_input_ids()[i1]
                    id2 = res.get_input_ids()[i2]
                    if res.get_node_by_id(id1).get_label() == res.get_node_by_id(id2).get_label():
                        a = res.get_node_by_id(id1).get_children_ids()[0]
                        b = res.get_node_by_id(id2).get_children_ids()[0]
                        res.fusion_deux_noeud(a, b)
                        res.remove_node_by_id(id2)
                        entree_unique = False
                        break
        nodeIdRes = res.get_node_ids()
        tab = [nodeIdRes[i] for i in range(len(nodeIdRes)) if res.get_node_by_id(nodeIdRes[i]).get_label() == '&']
        res.add_node('|', {ind:1 for ind in tab}, None)
        return bool_circ(res)

    @classmethod
    def int_to_bbc(cls, entier :int, taille_registre :int ):
        g = bool_circ.empty()
        l = []
        for i in range(taille_registre):
            j = entier%2
            l = [j]+l
            entier = (entier-j)/2
        for j in l:
            g.iparallel([bool_circ(open_digraph([], [1],[node(0,str(int(j)), {},{1:1}), node(1,"",{0:1},{})]))])
        return g                      

    @classmethod
    def random(cls, n,inp = 0, outp = 0):
        """
        renvoi un bool_circ aleatoire
        args : n -> 
        """
        operateurs_unitaires = ["~"]
        operateurs_binaires = ["&", "|"]
        
        g = open_digraph.random(n, 2,form="DAG")
        l = g.get_node_ids().copy()
        for id in l:
            nod = g.get_node_by_id(id)
            if len(nod.get_parent_ids()) == 0:
                g.add_node(nod.label, {}, {id:1})
                g.add_input_id(g.lastNewId)
                nod.label = ""
            if len(nod.get_children_ids()) == 0:
                g.add_node("", {id:1}, {})
                g.add_output_id(g.lastNewId)
                nod.label = ""
        

        if inp != 0:
            l1 = g.get_node_ids()
            l2 = g.get_input_ids()
            l3 = g.get_output_ids()
            l = [x for x in l1 if x not in l2 and x not in l3]
            while len(g.inputs) < inp:
                i = random.choice(l)
                g.add_input_node("x"+str(i), i)
                g.get_node_by_id(i).set_label("")
                l.remove(i)
            while len(g.inputs) > inp:
                l2 = g.get_input_ids()
                i1 = random.choice(l2)
                i2 = random.choice([x for x in l2 if x != i1])
                I1 = g.get_node_by_id(i1).get_children_ids()[0]
                I2 = g.get_node_by_id(i2).get_children_ids()[0]
                g.remove_nodes_by_id([i1,i2])
                g.add_node("",{},{I1:1,I2:1})
                g.add_input_node("x" +str(g.new_id()),g.lastNewId) 

        if outp != 0:
            l1 = g.get_node_ids()
            l2 = g.get_output_ids()
            l3 = g.get_input_ids()
            l = [x for x in l1 if x not in l2 and x not in l3]
            while len(g.outputs) < outp:
                i = random.choice(l)
                g.add_output_nodes("", i)
                l.remove(i)
            while len(g.outputs) > outp:
                l2 = g.get_output_ids()
                i1 = random.choice(l2)
                i2 = random.choice([x for x in l2 if x != i1])
                I1 = g.get_node_by_id(i1).get_parent_ids()[0]
                I2 = g.get_node_by_id(i2).get_parent_ids()[0]
                g.remove_nodes_by_id([i1,i2])
                g.add_node("",{I1:1,I2:1}, {})
                g.add_output_nodes("",g.lastNewId) 
            
        l = g.get_node_ids().copy()
        for id in l:
            nod = g.get_node_by_id(id)
            if len(nod.get_parent_ids()) == 1 and len(nod.get_children_ids()) == 1:
                nod.set_label(random.choice(operateurs_unitaires))
            if len(nod.get_parent_ids()) == 1 and len(nod.get_children_ids()) > 1:
                nod.set_label("")
            if len(nod.get_parent_ids()) > 1 and len(nod.get_children_ids()) == 1:
                nod.set_label(random.choice(operateurs_binaires))
            if len(nod.get_parent_ids()) > 1 and len(nod.get_children_ids()) > 1:
                p = nod.parents.copy()
                c = nod.children.copy()
                g.remove_node_by_id(nod.id)
                i1 = g.lastNewId
                i2 = i1 +1
                g.add_node(random.choice(operateurs_binaires), p,{})
                g.add_node("", {g.lastNewId:1},c)
                g.lastNewId += 2
        return bool_circ(g)                

    @classmethod
    def Adder(cls, n):
        if n == 0:
            g = open_digraph([], [], [])
            g.add_node("", {}, {})
            g.add_node("&", {1:1}, {})
            g.add_node("", {}, {2:1})
            g.add_node("^", {1:1, 3:1})
            g.add_node("", {4:1}, {})
            g.add_node("&", {5:1}, {})
            g.add_node("|", {2:1, 6:1}, {})
            g.add_node("", {}, {6:1})
            g.add_node("^", {8:1, 5:1}, {})
            g.add_input_node("x0", 1)
            g.add_input_node("x1", 3)
            g.add_input_node("xret", 8)
            g.add_output_nodes("oret", 7)
            g.add_output_nodes("o0", 9)
            return bool_circ(g)
        else:
            adder = bool_circ.Adder(n - 1)
            adderbis = adder.copy()
            adder.iparallel([adderbis])
            deuxPuiss = 2**n
            for i in range(0, deuxPuiss):
                bigId = max([id for id in adder.get_input_ids() if adder.get_node_by_id(id).get_label() == f"x{i}"])
                adder.get_node_by_id(bigId).set_label(f"x{i + deuxPuiss}")

            for i in range(int(deuxPuiss/2), deuxPuiss):
                smallId = [id for id in adder.get_input_ids() if adder.get_node_by_id(id).get_label() == f"x{i}"][0]
                bigId = [id for id in adder.get_input_ids() if adder.get_node_by_id(id).get_label() == f"x{2*deuxPuiss - i - 1}"][0]
                nS = adder.get_node_by_id(smallId)
                bS = adder.get_node_by_id(bigId)
                idFilsSmall = nS.get_children_ids()[0]
                idFilsBig = bS.get_children_ids()[0]
                adder.remove_edge(smallId, idFilsSmall)
                adder.remove_edge(bigId, idFilsBig)
                adder.add_edge(smallId, idFilsBig)
                adder.add_edge(bigId, idFilsSmall)

            for i in range(0, int(deuxPuiss/2)):
                bigId = max([id for id in adder.get_output_ids() if adder.get_node_by_id(id).get_label() == f"o{i}"])
                adder.get_node_by_id(bigId).set_label(f"o{i + int(deuxPuiss/2)}")

            # retenus
            retBanq = [id for id in adder.get_output_ids() if adder.get_node_by_id(id).get_label() == f"oret"]
            bigORet = max(retBanq)
            smallXRet = min([id for id in adder.get_input_ids() if adder.get_node_by_id(id).get_label() == f"xret"])
            src = adder.get_node_by_id(bigORet).get_parent_ids()[0]
            tgt = adder.get_node_by_id(smallXRet).get_children_ids()[0]
            adder.remove_node_by_id(bigORet)
            adder.remove_node_by_id(smallXRet)
            adder.add_edge(src, tgt)
            return adder

    @classmethod
    def half_Adder(cls, n):
        adder = bool_circ.Adder(n)
        xRetId = [id for id in adder.get_input_ids() if adder.get_node_by_id(id).get_label() == f"xret"][0]
        adder.get_node_by_id(xRetId).set_label("0")
        return adder

    @classmethod
    def encodeur(cls):
        a = parse_parentheses("(((x1)^(x2))^(x4))","(((x1)^(x3))^(x4))","(x1)","(((x2)^(x3))^(x4))","(x2)","(x3)","(x4)")
        a.evaluate()
        return a

    @classmethod
    def desencodeur(cls):
        a1 = parse_parentheses("((((x1)^(x3))^(x5))^(x7))", "((((x2)^(x3))^(x6))^(x7))", "x3", "((((x4)^(x5))^(x6))^(x7))", "(x5)", "x6", "(x7)")
        a2 = parse_parentheses("((((x1)&(x2))&(~(x4)))^(x3))", "((((x1)&(~(x2)))&(x4))^(x5))", "((((~(x1))&(x2))&(x4))^(x6))","((((x1)&(x2))&(x4))^(x7))")
        a2.icompose(a1)
        a2.evaluate()
        return a2


def parse_parentheses(*strings : str) -> bool_circ:
    """
    Creer un bool_circ a partir de l expression str
    Args : str : String
           return : le graph correspondant
    """

    def sub_parse_parentheses(s : str) -> bool_circ:
        g = bool_circ(open_digraph([], [], []))
        g.add_node()
        g.add_output_nodes(f'o', 1)
        current_node = 1
        s2 = ''
        labelList = {} # {label : id list}
        for char in s:    
            if char == '(':
                g.nodes[current_node].label += s2
                g.add_node(children={current_node:1})
                if not s2 in ['', '&', '|', '^', '~']:
                    if s2 in labelList:
                        labelList[s2] += current_node
                    else:
                        labelList.update({s2:[current_node]})
                current_node = g.lastNewId
                s2 = ''
            elif char == ')':
                g.nodes[current_node].label += s2
                if not s2 in ['', '&', '|', '^', '~']:
                    if s2 in labelList:
                        labelList[s2] += [current_node]
                    else:
                        labelList.update({s2:[current_node]})
                current_node = g.get_node_by_id(current_node).get_children_ids()[0]
                s2 = ''
            else:
                s2 += char
        for lab in labelList:
            l = labelList[lab]
            while len(l) != 1:
                g.fusion_deux_noeud(l[0], l[1], label=lab)
                l.remove(l[1])
            g.add_input_node(lab, l[0])
            g.get_node_by_id(l[0]).set_label('')
        return g

    g = bool_circ(open_digraph([], [], []))
    g.iparallel([sub_parse_parentheses(s) for s in strings])
    entree_unique = False
    while entree_unique == False:
        entree_unique = True
        for i1 in range(len(g.get_input_ids())):
            for i2 in range(i1+1, len(g.get_input_ids())):
                id1 = g.get_input_ids()[i1]
                id2 = g.get_input_ids()[i2]
                if g.get_node_by_id(id1).get_label() == g.get_node_by_id(id2).get_label():
                    g.fusion_deux_noeud(g.get_node_by_id(id1).get_children_ids()[0], g.get_node_by_id(id2).get_children_ids()[0])
                    g.remove_node_by_id(id2)
                    entree_unique = False
                    break
    return g

def code_de_grey(n):
    """
    args : n int
    """
    if n == 1:
        return ["0","1"]
    
    l = code_de_grey(n-1)
    newl = []

    lm = len(l)
    for k in range(lm):
        newl.append("0"+l[k])
    for k in range(lm):
        newl.append("1"+l[lm-1-k])

    return newl


def K_map(s):
    n = int(math.log(len(s), 2))
    l1 = code_de_grey(int(n/2))
    l2 = code_de_grey(n - int(n/2))

    l = []

    for x in range(len(l1)):
        l.append([int(s[int(l1[x] + l2[y], 2)]) for y in range(len(l2))])

    return l
    
"""def K_to_f_propositionel(K):
    Xl = len(K)
    o = int(math.log(Xl, 2))
    Yl = len(K[0])
    p = int(math.log(Xl, 2))

    def sub_total(i1, i2,j1,j2):
        tot = 0
        tot2 = 0
        for i in range(i1,i2+1):
            for j in range(j1,j2+1):
                if K[i%Xl][j%Yl] == 1:
                    tot += 1
                if K[i%Xl][j%Yl]:
                    tot2 += 1
                
        return tot, tot2

    n = 0
    for x in range(Xl):
        for y in range(Yl):
            n += K[x][y]

    l = []

    while n > 0:
        max = 0
        s_l = [0,0,0,0]

        for i in range(1,o+1):
            for j in range(1,p+1):
                for x in range(Xl):
                    for y in range(Yl):
                        s1,s2 = sub_total(x,x+2**i-1, y, y+2**j-1)
                        if s1 > max and s2 == 2**(i+j):
                            s_l = [x,(x+2**i-1)%Xl, y, (y+2**j-1)%Yl]
                            max = s1
        
        l.append(s_l.copy())
        for i in range(s_l[0],s_l[1]+1):
            for j in range(s_l[2],s_l[3]+1):
                K[i%Xl][j%Yl] = -1
        n += -max
        print(n)

    return l"""
