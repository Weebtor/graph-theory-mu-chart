import matplotlib.pyplot as plt
import networkx as nx
import sys
import numpy as np
import ntpath
import brute_force as bf
import csv_handler
import time
import tree_search


def print_msg_box(best_set,char_names,indent=1, width=None, title=None):

    msg=' Los personajes son: ' 
    for i in best_set:
        if i != best_set[-1]:
            msg += '['+ str(i)+']'+char_names[i]+ ', '
        else:
            msg += '['+ str(i)+']'+ char_names[i]+'.'

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

def path_leaf(path):
    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)

if __name__ == "__main__":
    mode=sys.argv[1]#-Fb,-Ts, -A
    file_path = sys.argv[2]
    # Python obtiene el primer argumento como la ruta del archivo csv
    print('Procesando dataset....')
    adjacency_matrix,char_names= csv_handler.csv_to_numpy_matrix_list(file_path)
    if mode =='-Fb' or mode =='-A':
        print("\n\n Fuerza Bruta \n")
        tic = time.time()
        best_set, value = bf.min_dom_set_bruteforce(adjacency_matrix)
        toc = time.time()
        print("Tiempo fuerza bruta:", toc-tic)
        print_msg_box(best_set,char_names,indent=3,title='Minimo set dominante Fuerza Bruta')

    if mode == '-Ts' or mode == '-A':
        print('\n\n Tree Search')
        dom_set = tree_search.run(adjacency_matrix)
        best_set,value, set_domination = bf.best_option_from_dom_set(np.array(adjacency_matrix, dtype=np.float32), np.array(dom_set, dtype = np.uint32))
        print_msg_box(best_set,char_names,indent=3,title='Minimo set dominante Tree Search')

    
    if mode == '-P':
        G1 = nx.DiGraph(np.matrix(adjacency_matrix))
        nx.draw_kamada_kawai(G1,  with_labels = True)
        name=path_leaf(file_path).split('.')[0]
        plt.savefig("img/"+name+".png")
    

    