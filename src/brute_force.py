import itertools
import numpy as np
from numba import jit,objmode
from numpy.core.records import array
import time

@jit(["uint32(uint32)"],nopython=True)
def max_dom_set_items(number_of_vertex):
    log2n = np.log2(number_of_vertex)
    return int(log2n) + int(log2n % 1 > 0)

@jit(["boolean(float32[:,:],uint32[:],uint32)"], nopython=True)
def check_dom_set(adjacency_matrix, set, vertex_len):
    # Función que evalua si un set es dominante
    # a partir de su matriz de adjacencia, el set
    # y la cantidad de vertices
    
    checked_vertex = np.zeros(vertex_len, dtype=np.uint32)   # Arreglo de 0 para determinar los vertices dominados
    
    for i in set:                                       # Intera sobre el set a evaluar
        checked_vertex[i] = 1                           # Marca su propio vertice como dominado
        for j, val in enumerate(adjacency_matrix[i]):   # Itera sobre sobre la fila I de la matriz de adjacencia
            if val > 0:                                 # Evalua si existe una arista de I->J
                checked_vertex[j] = 1                   # Marca el vertice J como dominado
            
    for item in checked_vertex:                         # Itera sobre el arreglo de vertices dominados
        if item == 0:                                   # Si un vertice no esta marcado como dominado
            return False                                # Retorna un False
    
    return True                                         # Si estan todos los vertices dominados retorna un True

@jit(["uint32[:,:](float32[:,:],uint32)"], nopython = True)
def get_order(adjacency_matrix, total_items):
    # Función para determinar el orden a evaluar de los vertices
    order_list = np.zeros((total_items,2),dtype=np.uint32)
    for i in range(0, total_items):
        order_list[i][0] = i
        order_list[i][1] = np.sum(adjacency_matrix[i]) 

    return order_list[np.argsort(order_list[:, 1])]

dom_set = {
    "sets":[],
    "tamaño_actual": 99999999999999999999
}

@jit(["Tuple((float32, uint32[:]))(float32[:,:],uint32[:])"], nopython = True)
def get_mds_value(adjacency_matrix, dominating_set):
    dominated_vertex = np.zeros((adjacency_matrix.shape[0]),dtype=np.uint32)
    acumulated_value = np.float32(0)
    for j, val in enumerate(dominated_vertex): 
        edge_value = np.float32(0)
        for i in dominating_set:
            if adjacency_matrix[i][j] > edge_value:
                edge_value = adjacency_matrix[i][j]
                dominated_vertex[j] = i
        acumulated_value = acumulated_value + edge_value
    
    return acumulated_value, dominated_vertex


@jit(["Tuple((uint32[:], float32, uint32[:]))(float32[:,:],uint32[:,:])"], nopython = True)
def best_option_from_dom_set(adjacency_matrix, mds_sets):
    best_set_index = np.uint32(0)
    best_set_value = np.float32(0)
    set_domination = np.array([0],dtype=np.uint32)
    print("Evaluando MDS")
    for i, val in enumerate(mds_sets):
        value,domination = get_mds_value(adjacency_matrix,mds_sets[i])
        if value > best_set_value:
            best_set_value = value
            best_set_index = i
            set_domination = domination
    print('El set elegido es: ', mds_sets[best_set_index], ' con una puntuacion de ', best_set_value)
    return mds_sets[best_set_index],best_set_value, set_domination

def min_dom_set(adjacency_matrix):
    number_of_vertex = np.uint32(len(adjacency_matrix[0]))
    numpy_matrix = np.array(adjacency_matrix, dtype=np.float32)
    max_depth = np.uint32(max_dom_set_items(number_of_vertex))
    # max_depth = np.uint32(3)
    # vertex_priority = get_order(numpy_matrix,number_of_vertex)
    intial_dominated_set = np.zeros(number_of_vertex, dtype=np.uint32)
    # dom_set_list = np.array([])
    for i in range(0, number_of_vertex):
        max_depth = not_generalized_leaf_removal(
            numpy_matrix,
            np.uint32(i),
            intial_dominated_set,
            np.array([i], dtype = np.uint32),
            max_depth,
            np.array([i], dtype = np.uint32)
        )
    mds = np.array(dom_set["sets"], dtype=np.uint32)
    best_set,value, set_domination = best_option_from_dom_set(numpy_matrix, np.array(mds, dtype = np.uint32))
    print(best_set,value, set_domination)
        
def min_dom_set_bruteforce(adjacency_matrix):
    dominating_sets = []
    vertex_index = np.arange(0,len(adjacency_matrix[0]),1)
    vertex_len = len(vertex_index)
    tic = time.time()
    for n in range(1,vertex_len+1):
        if len(dominating_sets) > 0:
            break
        for comb in itertools.combinations(vertex_index,n):
            # Check if dom set
            if check_dom_set(
                np.array(adjacency_matrix, dtype=np.float32), 
                np.array(list(comb),dtype=np.uint32), 
                np.uint32(vertex_len)
                ) == True:
                dominating_sets.append(comb)
            pass
    toc = time.time()
    print("Tiempo de busqueda set dominantes: ", toc-tic)
    best_set,value, set_domination = best_option_from_dom_set(np.array(adjacency_matrix, dtype=np.float32), np.array(dominating_sets, dtype = np.uint32))
    
    return best_set,value
    