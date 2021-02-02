# -*- coding: utf-8 -*-


import undirected as un
import directed as di
import osmnx as ox
ox.config(use_cache=True, log_console=True)
ox.__version__

###############################################################
#                    GLOBAL VARIABLES TEST                    #
###############################################################

list_1 = [(0,1,1), (1,2,3), (2,0,5)]
list_2 = [(0,1,1),(0,6,1), (1,2,1), (2,0,1), (2,3,1), (3,4,1), (4,2,1), (4,5,1), (5,0,1), (6,4,1)]
list_3 = [(0,1,1), (1,2,1), (1,3,1),(3,2,1),(3,4,1)]
###############################################################
#                            SUPPORT                          #
###############################################################

def get_node_list(edge_list):
    list_node = []
    visited = []
    for i in range(len(edge_list)):
        if edge_list[i][0] not in visited:
            list_node.append(edge_list[i][0])
        if edge_list[i][1] not in visited:
            list_node.append(edge_list[i][1])
    return list(set(list_node))

###############################################################
#                            TESTS                            #
###############################################################
list_1_node = get_node_list(list_1)
list_2_node = get_node_list(list_2)
list_3_node = get_node_list(list_3)

def test_get_weigth():
    
    print("Le poids attendu entre", list_1_node[0], "et", list_1_node[1],": 1")
    if un.get_weight(list_1_node[0], list_1_node[1], list_1) == 1:
        print("TRUE")
    else:
        print("FALSE")
    print("Le poids attendu entre", list_1_node[1], "et", list_1_node[2],": 3")
    if un.get_weight(list_1_node[1], list_1_node[2], list_1) == 3:
        print("TRUE")
    else:
        print("FALSE")
    print("Le poids attendu entre", list_1_node[1], "et", list_1_node[2],": 5")
    if un.get_weight(list_1_node[2], list_1_node[0], list_1) == 5:
        print("TRUE")
    else:
        print("FALSE")
        
def test_get_neighbours():
    print("Le/Les voisin(s) attendu(s) de", list_1_node[0], "sont: 1-2")
    if un.get_neighbours(list_1, list_1_node[0]) == [1,2]:
        print("TRUE")
    else:
        print("FALSE")
    print("Le/Les voisin(s) attendu(s) de", list_1_node[1], "sont: 0-2")
    if un.get_neighbours(list_1, list_1_node[1]) == [0,2]:
        print("TRUE")
    else:
        print("FALSE")
    print("Le/Les voisin(s) attendu(s) de", list_1_node[2], "sont: 0-1")
    if un.get_neighbours(list_1, list_1_node[2]) == [0,1]:
        print("TRUE")
    else:
        print("FALSE")
        
def test_get_neighbours_oriented():
    print("Le/Les voisin(s) attendu(s) de", list_1_node[0], "sont: 1")
    if di.get_neighbours_oriented(list_1, list_1_node[0]) == [1]:
        print("TRUE")
    else:
        print("FALSE")
    print("Le/Les voisin(s) attendu(s) de", list_1_node[1], "sont: 2")
    if di.get_neighbours_oriented(list_1, list_1_node[1]) == [2]:
        print("TRUE")
    else:
        print("FALSE")
    print("Le/Les voisin(s) attendu(s) de", list_1_node[2], "sont: 0")
    if di.get_neighbours_oriented(list_1, list_1_node[2]) == [0]:
        print("TRUE")
    else:
        print("FALSE")
        
def test_is_eulerian():
    print("Le graph est:", list_1, "et le resultat attendu est: True")
    if un.is_eulerian(len(list_1_node), list_1) == True:
        print("Le graph est Eulerien:", un.is_eulerian(len(list_1_node), list_1))
    else:
        print("Le graph est Eulerien:", un.is_eulerian(len(list_1_node), list_1))
    print()
    print("Le graph est:", list_2, "et le resultat attendu est: True")
    if un.is_eulerian(len(list_2_node), list_2) == True:
        print("Le graph est Eulerien:", un.is_eulerian(len(list_2_node), list_2))
    else:
        print("Le graph est Eulerien:", un.is_eulerian(len(list_2_node), list_2))
    print()
    print("Le graph est:", list_3, "et le resultat attendu est: False")
    if un.is_eulerian(len(list_3_node), list_3) == True:
        print("Le graph est Eulerien:", un.is_eulerian(len(list_3_node), list_3))
    else:
        print("Le graph est Eulerien:", un.is_eulerian(len(list_3_node), list_3))

###############################################################
#                             MAIN                            #
###############################################################

def final_test():
    print()
    print("###############################################################")
    print("#                            TESTS                            #")
    print("###############################################################")
    print()
    print("List en question:\n", list_1)
    print("Verification du poids:\n")
    test_get_weigth()
    print()
    print()
    print("Verification des voisins (non-oriente):\n")
    test_get_neighbours()
    print()
    print("Verification des voisins (oriente):\n")
    test_get_neighbours_oriented()
    print()
    print("Verification si le graph est Eulerien:\n")
    test_is_eulerian()

