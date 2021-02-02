# -*- coding: utf-8 -*-

import osmnx as ox
ox.config(use_cache=True, log_console=True)
ox.__version__

###############################################################
#                       GLOBAL VARIABLE                       #
###############################################################

balanced_node = []
dist_list = []

###############################################################
#                       SUPPORT FUNCTIONS                     #
###############################################################


def get_node_list(edge_list):
    '''
    recupere tous les noeuds du graphe dans une liste

    Parameters
    ----------
    edge_list :
        liste des relations entre les noeuds du graphe

    Returns
    -------
    retourne la liste des noeuds que contient le graphe

    '''
    
    list_node = []
    visited = []
    for i in range(len(edge_list)):
        if edge_list[i][0] not in visited:
            list_node.append(edge_list[i][0])
        if edge_list[i][1] not in visited:
            list_node.append(edge_list[i][1])
    return list(set(list_node))

          
def get_weight(a,b,edge_list):
    '''
    recupere le poids d'une arrete 

    Parameters
    ----------
    a :
        un noeud du graphe
    b :
        un noeud du graphe
    edge_list :
        liste des relations entre les noeuds du graphe

    Returns
    -------
    retorune le poids de l'arrete

    '''
    
    for edge in edge_list:
        if edge[0] == a and edge[1] == b:
            return edge[2]
        if edge[1] == a and edge[0] == b:
            return edge[2]
    return 0


def get_neighbours_oriented(edge_list, u):
    '''
    focntion qui recupere les voisins du sommet u

    Parameters
    ----------
    edge_list :
        liste des relations entre les noeuds du graphe
    u :
        un noeud du graphe

    Returns
    -------
    retourne les voisins de u

    '''
    list_neighbours = []
    for i in range(len(edge_list)):
        if u == edge_list[i][0]:
            list_neighbours.append(edge_list[i][1])
    return list(set(list_neighbours))


def get_adj_list(edge_list, list_node):
    '''
    recupere la liste d'adjacence du graphe
    
     Parameters
    ----------
    edge_list :
        liste des relations entre les noeuds du graphe
    list_node :
        liste des noeuds dans le graphe
    next_node:
        compteur qui permet de passer au noeud suivant lors de la recursivite
    
    Returns
    -------
    retourne la list d adjacence
    
    '''
    adj_list = []
    
    for node in list_node:
        neighbours = get_neighbours_oriented(edge_list, node)
        adj_list.append(neighbours)
    return adj_list


def check_node_balanced(edge_list, list_node, next_node):
    '''
    regarde les arcs sortants et entrants de chaque noeuds
    
    Parameters
    ----------
    edge_list :
        liste des relations entre les noeuds du graphe
    list_node :
        liste des noeuds dans le graphe
    next_node:
        compteur qui permet de passer au noeud suivant lors de la recursivite
    
    Returns
    -------
    retourne une list de triplet de la forme suivante: (id du noeud, nombre arc sortant, nombre arc enrant )
        
    '''
    
    
    count_entrant = 0
    count_sortant = 0

    for edge in edge_list:
        if edge[0] == list_node[next_node]:
            count_entrant += 1
        if edge[1] == list_node[next_node]:
            count_sortant += 1
            
    balanced_node.append([list_node[next_node], count_entrant, count_sortant])
        
    if next_node == len(list_node) - 1:
        return balanced_node
    return check_node_balanced(edge_list, list_node, next_node + 1)


def is_eulerian_oriented(balanced_node):
    '''
    determine si le graph est eulerien ou non
    
    Parameters
    ----------
    balanced_node :
        liste de triplet de la forme suivante : (id du noeud, nombre arc sortant, nombre arc enrant)

    Returns
    -------
    retourne True si le graphe ests eulerien sinon False

    '''
    for i in range(len(balanced_node)):
        if balanced_node[i][1] != balanced_node[i][2]:
            return False
    return True
    

###############################################################
#                          HIERHOLZER                         #
###############################################################

def Hierholzer_algo(adj, edge_list, list_node):
    '''
    fonction qui calcul le chemin eulerien dans un graph        
    
    Parametres
    ----------
    adj :
        liste d adjacence du graph
    edge_list :
        liste des relations entre les noeuds du graphe
    list_node :
        liste des noeuds dans le graphe

    Returns
    -------
    retourne le chemin eulerien

    '''
    
    start = list_node[0]
    current_path = [start]
    circuit = []
    
    while current_path:
        current_v = current_path[-1]
        if adj[list_node.index(current_v)]:
            next_v = adj[list_node.index(current_v)].pop()
            current_path.append(next_v)
        else:
            circuit.append(current_path.pop())
    circuitx = circuit.copy()
    circuitx.reverse()
    for i in range(len(circuitx) - 1):
        print("%d-%d " %(circuitx[i], circuitx[i + 1]))
            
def Hierholzer(edge_list, list_node):
    adj = get_adj_list(edge_list, list_node)
    return Hierholzer_algo(adj, edge_list, list_node)

###############################################################
#                             MAIN                            #
###############################################################

def solve_directed(num_vertices, edge_list):
    '''    
    seul le cas du graphe eulerien est pris en compte
    '''
    node = get_node_list(edge_list)
    balanced_node = check_node_balanced(edge_list, node, 0)
    if is_eulerian_oriented(balanced_node) == True:
        node = get_node_list(edge_list)
        Hierholzer(edge_list, node)
        
        
