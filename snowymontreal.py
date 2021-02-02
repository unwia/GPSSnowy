# -*- coding: utf-8 -*-

import osmnx as ox
ox.config(use_cache=True, log_console=True)
ox.__version__

import undirected as un
import directed as di
import test1



def solve(is_oriented, num_vertices, edge_list):
    if is_oriented == False:
        un.solve_undirected(num_vertices, edge_list)
    else:
        di.solve_directed(num_vertices, edge_list)
        
def test():
    test1.final_test()
        
