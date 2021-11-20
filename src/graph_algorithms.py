import itertools
import numpy as np
from numba import jit

@jit(nopython=True)
def max_dom_set_items(list_size):
    log2n = np.log2(list_size)
    return int(log2n) + int(log2n % 1 > 0)


@jit(["boolean(float32[:,:],uint32[:],uint32)"], nopython=True)
def check_dom_set(adjacency_matrix, set, vertex_len):
    # Función que evalua si un set es dominante
    # a partir de su matriz de adjacencia, el set
    # y la cantidad de vertices
    
    checked_vertex = np.zeros(vertex_len, dtype=np.uint8)   # Arreglo de 0 para determinar los vertices dominados
    
    for i in set:                                       # Intera sobre el set a evaluar
        checked_vertex[i] = 1                           # Marca su propio vertice como dominado

        for j, val in enumerate(adjacency_matrix[i]):   # Itera sobre sobre la fila I de la matriz de adjacencia
            if val > 0:                                 # Evalua si existe una arista de I->J
                checked_vertex[j] = 1                   # Marca el vertice J como dominado
            
    for item in checked_vertex:                         # Itera sobre el arreglo de vertices dominados
        if item == 0:                                   # Si un vertice no esta marcado como dominado
            return False                                # Retorna un False
    
    return True                                         # Si estan todos los vertices dominados retorna un True


    

def min_dom_set_bruteforce(adjacency_matrix):
    dominating_sets = []
    # print(dominating_sets)
    vertex_index = np.arange(0,len(adjacency_matrix[0]),1)
    vertex_len = len(vertex_index)
    for n in range(1,vertex_len+1):
        if len(dominating_sets) > 0:
            print(dominating_sets)

            break
        print("Revisando para n=",n)
        for comb in itertools.combinations(vertex_index,n):
            # Check if dom set
            if check_dom_set(
                np.array(adjacency_matrix, dtype=np.float32), 
                np.array(list(comb),dtype=np.uint32), 
                np.uint32(vertex_len)
                ) == True:
                dominating_sets.append(comb)
            # print(comb)
            pass

    return dominating_sets
    