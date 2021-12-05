from data_manager import DataManager
import graph_theory as gt
import matplotlib.pyplot as plt
import networkx as nx
import sys
import numpy as np

import graph_algorithms as ga

import csv_handler

import time

if __name__ == "__main__":
    file_path = sys.argv[1]

    # Python obtiene el primer argumento como la ruta del archivo csv
    adjacency_matrix= csv_handler.csv_to_numpy_matrix_list(file_path)
    # print(adjacency_matrix)
    print("brute force")
    tic = time.time()
    mds = ga.min_dom_set_bruteforce(adjacency_matrix)
    toc = time.time()
    print("time:", toc-tic)
    print("GLR")
    tic = time.time()
    mds = ga.min_dom_set(adjacency_matrix)
    toc = time.time()
    print("time:", toc-tic)

    # ##########################
    # G1 = nx.DiGraph(np.matrix(adjacency_matrix))
    # print(nx.find_cycle(G1, orientation="original"))
    # nx.draw_kamada_kawai(G1,  with_labels = True)
    # plt.savefig("filename.png")
    #######################
    # # for i, arg in enumerate(sys.argv):
    # #     print(f"Argument {i:>6}: {arg}")
    # dm = DataManager(file_path)
    # mu_graph = nx.DiGraph()    

    # vertex_list = dm.get_vertex_list() 
    
    # gt.add_vertex_list(mu_graph, vertex_list)
    

    # # armar grafo completo
    # for i,character in enumerate(vertex_list):
    #     winning_mu = dm.get_character_winning_mu(vertex_list[i]) # obtiene los MU ganadores
    #     gt.add_edge_list(mu_graph, vertex_list[i], winning_mu)
    #     print(i, character)

    # # dominating_sets = gt.get_all_dominating_sets_brute_force(mu_graph)
    # # print(f"Dominating sets: {dominating_sets}")
    # min_dominating_sets = gt.get_min_dominating_sets_brute_force(mu_graph)
    # print(f"Min dominating sets: {min_dominating_sets}")

    # gt.draw_graph(mu_graph)
    # print(answer)
    # print(gm.get_dominant_set_default())
    # gm.draw_graph()
    # print(vertex_list)
    # dm.get_char_mu(vertex_list[1])