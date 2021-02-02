# -*- coding: utf-8 -*-

import osmnx as ox
ox.config(use_cache=True, log_console=True)
ox.__version__

###############################################################
#                       GLOBAL VARIABLE                       #
###############################################################

pair_return = []

###############################################################
#                       SUPPORT FUNCTIONS                     #
###############################################################


def odd_vertices(n, edge_list):
    '''
    renvoie une liste des noeuds qui sont de degrees impairs

    Parametres
    ----------
    n :
        nombre de sommet
    edge_list :
        liste des relations entre les noeuds du graphe

    Returns
    -------
    list_odd_nodesx :
        retourne la liste des des noeuds impaira
    count :
        retourne le nombre de noeuds impairs present dans la liste ci-desdus

    '''
    
    count = 0
    res = []
    res2 = []
    somme = 0
    somme2 = 0
    visited = []
    visited2 = []
    '''regarde pour le premier element du couple'''
    for i in range(0, len(edge_list)):
        somme = 0
        if edge_list[i][0] not in visited:
            for j in range(len(edge_list)):
                if edge_list[i][0] == edge_list[j][0] or edge_list[i][0] == edge_list[j][1]:
                    somme += 1
            visited.append(edge_list[i][0])
            if somme % 2 != 0:
                res.append(edge_list[i][0])
                count += 1
    '''regarde pour le deuxieme element du couple'''
    for i in range(0, len(edge_list)):
        somme2 = 0
        if edge_list[i][1] not in visited2:
            for j in range(len(edge_list)):
                if edge_list[i][1] == edge_list[j][0] or edge_list[i][1] == edge_list[j][1]:
                    somme2 += 1
            visited2.append(edge_list[i][1])
            if somme2 % 2 != 0:
                res2.append(edge_list[i][1])
                count += 1
    list_odd_nodes = res + res2
    list_odd_nodesx = list(set(list_odd_nodes))
    return list_odd_nodesx, count


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
   
   
def get_neighbours(edge_list, u):
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
        if u == edge_list[i][1]:
            list_neighbours.append(edge_list[i][0])
    return list(set(list_neighbours))

def is_eulerian(num_vertices, edge_list):
    '''
    regarde si le graphe est eulerien

    Parameters
    ----------
    num_vertices :
        nombre de sommets dans le graphe
    edge_list :
        liste des relations entre les noeuds du graphe

    Returns
    -------
    retourne True si le graphe est eulerien sinon False

    '''
    list_odd, count = odd_vertices(num_vertices, edge_list)
    
    if len(list_odd) == 2 or len(list_odd) == 0:
        return True
    return False


def dfs(vertice, visited, list_node, edge_list):
    '''
    fonction qui fait un parcours en profondeur
    
    Parameters
    ----------
    vertice :
        un sommet du graphe
    visited :
        liste remplit de False et qui change au fur et a mesure
    list_node :
        liste des noeuds du graphe
    edge_list :
        liste des relations entre les noeuds du graphe
    Returns
    -------
    retourne la liste visited pour savoir si tout les sommets ont ete visite

    '''
    visited[list_node.index(vertice)] = True
    
    neighbours = get_neighbours(edge_list, vertice)
    
    for i in neighbours:
        if visited[list_node.index(i)] == False:
            dfs(i, visited, list_node, edge_list)
    return visited


def dfs_count(vertice, visited, list_node, edge_list):
    '''
   dfs qui compte le nombre de sommet accessible à partir d'un autre sommet

    Parameters
    ----------
    vvertice :
        un sommet du graphe
    visited :
        liste remplit de False et qui change au fur et a mesure
    list_node :
        liste des noeuds du graphe
    edge_list :
        liste des relations entre les noeuds du graphe

    Returns
    -------
    retourne le nombre de sommet accessible depuis un sommet donnee

    '''
    visited[list_node.index(vertice)] = True
    count = 1
    neighbours = get_neighbours(edge_list, vertice)
    
    for i in neighbours:
        if visited[list_node.index(i)] == False:
            count = count + dfs_count(i, visited, list_node, edge_list)
    return count
    

def reverse_edge(edge_list):
    '''
    transforme une arrete: (i,j) -> (j,i)

    Parameters
    ----------
    edge_list :
        liste des relations entre les noeuds du graphe.

    Returns
    -------
    reverse_edge_list :
        retourne l'inverse de la edge_liste 
    '''
    reverse_edge_list = []
    for edge in edge_list:
        reverse_edge_list.append((edge[1],edge[0],edge[2]))
    return reverse_edge_list


def remove_edge(a, b, weigth, edge_list):
    '''
    supprime une arrete de la edge_list

    Parameters
    ----------
    a :
        un sommet du graphe
    b :
        un sommet du graphe
    weigth :
        le poids entre a et b
    edge_list :
        liste des relations entre les noeuds du graphe.

    Returns
    -------
    edge_list :
        retourne edge_list mais avec le triplet (a, b, weight) en moins

    '''
    for edge in edge_list:
        if edge[0] == a and edge[1] == b and edge[2] == weigth:
            edge_list.remove(edge)
        if edge[1] == a and edge[0] == b and edge[2] == weigth:
            edge_list.remove(edge)
    return edge_list


def twice_add(edge_list, a, b):
    '''
    ajoute (i,j) et (j,i) à  la edge list

    Parameters
    ----------
    edge_list :
        liste des relations entre les noeuds du graphe.
    a :
        un sommet du graphe
    b :
        un sommet du graphe

    Returns
    -------
    retourne la edge_list avec les nouvelles arretes ajoutes
    '''
    edge_list.append((a,b, get_weight(a, b, edge_list)))
    edge_list.append((b,a, get_weight(a, b, edge_list)))
    return edge_list

###############################################################
#                            DIJKSTRA                         #
###############################################################

def dijkstra(src, list_node, edge_list):
    '''
    foncion qui calcul le plus court chemin

    Parameters
    ----------
    src :
        un sommet du graphe
    list_node :
        liste des sommets du graphes
    edge_list :
        liste des relations dans le graphes

    Returns
    -------
    dist :
        retourne un dictionnaire qui donne la distance entre un sommet de depart et les autres sommets du graphes
    previous :
        retorune une dictionnaire qui stock le chemin
    '''
    
    dist = dict()
    previous = dict()
    
    for vertex in list_node:
        dist[vertex] = float("inf")
        previous[vertex] = None
    dist[src] = 0
    
    Q = set(list_node)
    
    while len(Q) > 0:
        u = min(Q, key=lambda vertex: dist[vertex])
        Q.discard(u)
        
        if dist[u] == float('inf'):
            break
        neighbours = get_neighbours(edge_list, u)
        
        for node in neighbours:
            weigth = get_weight(u,node,edge_list)
            alt = float(dist[u]) + weigth
            if alt < dist[node]:
                dist[node] = alt
                previous[node] = u
    return dist, previous

def dijkstra_path(src, target, list_node, edge_list):
    '''
    fonction qui donne le plus court chemin entre src et target

    Parameters
    ----------
    src :
        un sommet de depart du graphe
    target :
        un sommet d'arrive du graphe
    list_node :
        liste des sommetes du graphe
    edge_list :
        liste des relation du graphe

    Returns
    -------
    retourne le plus court chemin entre src et target

    '''
    
    _, prev = dijkstra(src, list_node, edge_list)
    path = []
    
    debut = target
    while debut != src:
        path.append(debut)
        debut = prev[debut]
    path.append(src)
    pathx = path.copy()
    pathx.reverse()
    return pathx

###############################################################
#                         GENERATE PAIR                       #
###############################################################

def generate_pair_possible(list_odd_nodes):
    '''
    genere toute les paires possibles entre les sommets de degres impair

    Parameters
    ----------
    list_odd_nodes :
        liste des sommets de degres impair du graphe

    Returns
    -------
    list_pair_edge :
        retourne une liste de toute les paires possible entre les sommets de la list_odd_nodes

    '''
    
    list_pair_edge = []
    for i in range(len(list_odd_nodes)):
        for j in range(i,len(list_odd_nodes)):
            if i != j or j != i:
                if (list_odd_nodes[i],list_odd_nodes[j]) not in list_pair_edge or (list_odd_nodes[j],list_odd_nodes[i]) not in list_pair_edge:
                    list_pair_edge.append((list_odd_nodes[i],list_odd_nodes[j]))
    return list_pair_edge

def remove_pair_in_list(list_pair_edge,a,b):
    '''
    fonction qui supprime les paires deja obtenu

    Parameters
    ----------
    list_pair_edge :
        liste des paires entre les sommets
    a :
        un sommet du graphe
    b :
        un sommet du graphe

    '''
    
    tmp = list_pair_edge.copy()
    n = len(tmp)
    for i in range(n):
        if list_pair_edge[i][0] == a or list_pair_edge[i][1] == a or list_pair_edge[i][0] == b or list_pair_edge[i][1] == b:
            list_pair_edge.remove(list_pair_edge[i])
            return remove_pair_in_list(list_pair_edge,a,b)
    
def choice_best_new_pair(list_pair_edge,list_odd_nodes,node,edge_list):
    '''
    choisit la meilleur paire possible parmis toute les paires existantes

    Parameters
    ----------
    list_pair_edge :
        liste des paires du graphe
    list_odd_nodes :
        liste des sommets de degres impair
    node :
        liste des sommets du graphe
    edge_list :
        liste des relations entre les sommets du graphe

    Returns
    -------
    retorune une liste des nouvelles paires

    '''
    
    min = dijkstra_path(list_odd_nodes[0],list_odd_nodes[1],node,edge_list)
    
    for i in range(len(list_pair_edge)):
        if dijkstra_path(list_pair_edge[i][0],list_pair_edge[i][1], node, edge_list) <= min:
            min = dijkstra_path(list_pair_edge[i][0],list_pair_edge[i][1], node, edge_list)
    pair_return.append((min[0],min[-1],min))
    list_odd_nodes.remove(min[0])
    list_odd_nodes.remove(min[-1])
    if len(list_odd_nodes) != 0:
        remove_pair_in_list(list_pair_edge,min[0],min[-1])
        return choice_best_new_pair(list_pair_edge,list_odd_nodes, node, edge_list)
    return pair_return


def set_up_dist(best_pair_list, edge_list):
    '''
    met en place le nouveau poids de chaque nouvelle paire

    Parameters
    ----------
    best_pair_list :
        liste des meilleures paires
    edge_list :
        liste des relations entre les sommets du graphe

    Returns
    -------
    list_weight_new_pair :
        retourne une liste avec les nouvelles paires + leurs poids associé

    '''
    
    list_weight_new_pair = []
    tmp = []
    somme = 0.0
    for pair in best_pair_list:
        somme = 0.0
        tmp = []
        for j in range(len(pair[2]) - 1):
            info = get_weight(pair[2][j],pair[2][j + 1], edge_list)
            tmp.append(info)
        for i in range(len(tmp)):
            somme += tmp[i]
        pairx = list(pair)
        pairx.pop(-1)
        pairx.append(somme)
        pair = tuple(pairx)
        list_weight_new_pair.append(pair)
    return list_weight_new_pair

def create_new_edge_list(list_odd_nodes, node, tmp):
    possible_pair = generate_pair_possible(list_odd_nodes)
    best_pair = choice_best_new_pair(possible_pair, list_odd_nodes, node, tmp)
    new_pair_with_theirs_dist = set_up_dist(best_pair, tmp)
    new_edge_list = tmp + new_pair_with_theirs_dist
    return new_edge_list, best_pair



###############################################################
#                           FLEURY                            #
###############################################################

def check_next_node(src, dest, edge_list, list_node):
    '''
    fonction qui regarde si le sommet voisin est accessible et si l'arrete
    entre src et dest n'est pas un pont

    Parameters
    ----------
    src :
        un sommet de depart
    dest :
        un sommet de destination
    edge_list :
        liste des relations entre les sommets du graphe
    list_node :
        liste des sommets du graphe

    Returns
    -------
    retourne True si le noeuds est accessible sinon False

    '''
    
    cpy_edge_list = edge_list.copy()
    neighbours = get_neighbours(cpy_edge_list, src)
    
    if neighbours == []:
        return
    
    if len(neighbours) == 1:
        return True
    else:
        visited = [False] * len(list_node)
        count1 = dfs_count(src, visited, list_node, cpy_edge_list)
        remove_edge(src, dest, get_weight(src, dest, cpy_edge_list),cpy_edge_list)
        remove_edge(dest, src, get_weight(src, dest, cpy_edge_list), cpy_edge_list)
        visited = [False] * len(list_node)
        count2 = dfs_count(src, visited, list_node, cpy_edge_list)
        twice_add(cpy_edge_list,src, dest)
        
        if count1 > count2:
            return False
        return True

def Fleury_non_eulerien(src, edge_list, list_node, best_pair):
    '''
    algorithme de Fleury qui permet de trouver et d'afficher le chemin eulerien

    Parameters
    ----------
    src :
        un sommet de depart
    edge_list :
        liste des realtions entre les sommets du graphe
    list_node :
        liste des sommets du graphe
    best_pair:
        liste des meilleures paires possible

    Returns
    -------
    affiche le chemin eulerien

    '''
    
    neighbours = get_neighbours(edge_list, src)
    for node in neighbours:
        if check_next_node(src, node, edge_list, list_node) == True:
            print("%d-%d " %(src, node))
            for elt in best_pair:
                if (elt[0] == src and elt[1] == node):
                    for i in range(len(elt[2]) - 1):
                        print("  (%d-%d) " %(elt[2][i], elt[2][i + 1]))
                if (elt[1] == src and elt[0] == node):
                    for i in range(len(elt[2]) - 1, 0,-1):
                        print("  (%d-%d) " %(elt[2][i], elt[2][i - 1]))
            remove_edge(src, node, get_weight(src, node, edge_list), edge_list)
            remove_edge(node, src, get_weight(src, node, edge_list), edge_list)
            Fleury_non_eulerien(node, edge_list, list_node, best_pair)
            
def Fleury_eulerien(src, edge_list, list_node):
    '''
    algorithme de Fleury qui permet de trouver et d'afficher le chemin eulerien

    Parameters
    ----------
    src :
        un sommet de depart
    edge_list :
        liste des realtions entre les sommets du graphe
    list_node :
        liste des sommets du graphe
    best_pair:
        liste des meilleures paires possible

    Returns
    -------
    affiche le chemin eulerien

    '''
    
    neighbours = get_neighbours(edge_list, src)
    for node in neighbours:
        if check_next_node(src, node, edge_list, list_node) == True:
            print("%d-%d " %(src, node))
            remove_edge(src, node, get_weight(src, node, edge_list), edge_list)
            remove_edge(node, src, get_weight(src, node, edge_list), edge_list)
            Fleury_eulerien(node, edge_list, list_node)

###############################################################
#                             MAIN                            #
###############################################################

def solve_undirected(num_vertices, edge_list):
    list_odd_nodes, _ = odd_vertices(num_vertices,edge_list)
    node = get_node_list(edge_list)
    odd_copy = list_odd_nodes.copy()
    
    if is_eulerian(num_vertices, edge_list) == False:
        tmp = reverse_edge(edge_list)
        new_edge_list, best_pair = create_new_edge_list(list_odd_nodes, node, tmp)
        fleury_edge_list = tmp + new_edge_list
        print("Une arrete ecrite sous la forme A-B et suivie d'arretes sous la forme (C-D)")
        print("signifie que l'arrete A-B est parcourue par le chemin decrit par les arretes entre ( )")
        Fleury_non_eulerien(odd_copy[0], fleury_edge_list, node, best_pair)
        
    else:
        tmp = reverse_edge(edge_list)
        fleury_edge_list = edge_list + tmp
        Fleury_eulerien(node[0], fleury_edge_list, node)
