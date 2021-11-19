import itertools
import numpy as np
from numba import jit

@jit(nopython=True)
def max_dom_set_items(list_size):
    log2n = np.log2(list_size)
    return int(log2n) + int(log2n % 1 > 0)

# @jit(nopython=True)
def check_dom_set(adjacency_matrix, set, vertex_len):
    checked_vertex = np.zeros(vertex_len, dtype=int)
    print("for:", set)
    for i in set:
        checked_vertex[i] = 1

        for j, val in enumerate(adjacency_matrix[i]):
            if val > 0:
                checked_vertex[j] = 1
            
    print(checked_vertex)
    for item in checked_vertex:
        if item == 0:
            return False
    print(True)
    return True


    

def min_dom_set_bruteforce(adjacency_matrix):
    dominating_sets = []
    print(dominating_sets)
    vertex_index = np.arange(0,len(adjacency_matrix[0]),1)
    vertex_len = len(vertex_index)
    # max_items = max_dom_set_items(len(vertex_index))
    for n in range(1,vertex_len+1):
        if len(dominating_sets) > 1:
            print(dominating_sets)

            break
        print("Revisando para n=",n)
        for comb in itertools.combinations(vertex_index,n):
            # Check if dom set
            if check_dom_set(adjacency_matrix, 
                np.array(list(comb)),
                np.uint32(vertex_len)) == True:
                dominating_sets.append(comb)
            # print(comb)
            pass

    return dominating_sets
    