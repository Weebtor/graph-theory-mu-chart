# from data_manager import DataManager
# import graph_theory as gt
# import matplotlib.pyplot as plt
# import networkx as nx
import sys
import numpy as np

import graph_algorithms as ga

import csv_handler
# import GLR 
import time
import tree_search


def print_msg_box(msg, indent=1, width=None, title=None):
    # Funcion para imprimir los resultados de forma amigable
    lines = msg.split('\n')
    space = " " * indent
    if not width:
        width = max(map(len, lines))
    box = f'╔{"═" * (width + indent * 2)}╗\n'  # upper_border
    if title:
        box += f'║{space}{title:<{width}}{space}║\n'  # title
        box += f'║{space}{"-" * len(title):<{width}}{space}║\n'  # underscore
    box += ''.join([f'║{space}{line:<{width}}{space}║\n' for line in lines])
    box += f'╚{"═" * (width + indent * 2)}╝'  # lower_border
    print(box)

if __name__ == "__main__":
    mode=sys.argv[1]#-Fb,-Ts, -A
    file_path = sys.argv[2]
    # Python obtiene el primer argumento como la ruta del archivo csv
    adjacency_matrix,char_names= csv_handler.csv_to_numpy_matrix_list(file_path)
    if mode =='-Fb' or mode =='-A':
        
        
        # print(adjacency_matrix,char_names)
        # csv_handler.csv_to_name(file_path)
        # print(names)
        print("\n\n Fuerza Bruta \n")
        tic = time.time()
        best_set, value = ga.min_dom_set_bruteforce(adjacency_matrix)
        toc = time.time()
        print("Tiempo fuerza bruta:", toc-tic)
        # print("no GLR")
        # tic = time.time()
        # mds = ga.min_dom_set(adjacency_matrix)
        # toc = time.time()
        # print("time:", toc-tic)
        msg=' Los personajes son: ' 
        for i in best_set:
            if i != best_set[-1]:
                msg += '['+ str(i)+']'+char_names[i-1]+ ', '
            else:
                msg += '['+ str(i)+']'+ char_names[i-1]+'.'
        print_msg_box(msg,indent=3,title='Minimo set dominante Fuerza Bruta')

    if mode == '-Ts' or mode == '-A':
        print('\n\n Tree Search')
        dom_set = tree_search.run(adjacency_matrix)
        best_set,value, set_domination = ga.best_option_from_dom_set(np.array(adjacency_matrix, dtype=np.float32), np.array(dom_set, dtype = np.uint32))
        # print(best_set,value,dom_set)
    
        msg=' Los personajes son: ' 
        for i in best_set:
            if i != best_set[-1]:
                msg += '['+ str(i)+']'+ char_names[i-1]+ ', '
            else:
                msg += '['+ str(i)+']'+ char_names[i-1]+'.'
        print_msg_box(msg,indent=3,title='Minimo set dominante Tree Search')

    
        

    #######################

    ######################

    # adjacency_matrix = GLR.encontrar_mds(np.array(adjacency_matrix, dtype=np.float32))

    # ##########################
    # G1 = nx.DiGraph(np.matrix(adjacency_matrix))
    # print(nx.find_cycle(G1, orientation="original"))
    # nx.draw_kamada_kawai(G1,  with_labels = True)
    # plt.savefig("filename.png")
    # #######################
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