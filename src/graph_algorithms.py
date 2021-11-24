import itertools
import numpy as np
from numba import jit,objmode
from numpy.core.records import array







@jit(["uint8(uint8)"],nopython=True)
def max_dom_set_items(number_of_vertex):
    log2n = np.log2(number_of_vertex)
    return int(log2n) + int(log2n % 1 > 0)


@jit(["boolean(float32[:,:],uint8[:],uint8)"], nopython=True)
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

@jit(["uint8[:,:](float32[:,:],uint8)"], nopython = True)
def get_order(adjacency_matrix, total_items):
    # Función para determinar el orden a evaluar de los vertices
    order_list = np.zeros((total_items,2),dtype=np.uint8)
    for i in range(0, total_items):
        order_list[i][0] = i
        order_list[i][1] = np.sum(adjacency_matrix[i]) 

    return order_list[np.argsort(order_list[:, 1])]



dom_set = []
@jit(["uint8(float32[:,:], uint8, uint8[:], uint8[:],uint8)"], nopython = True)
def generalized_leaf_removal(adjacency_matrix, vertex_index, dominated_set, set_route, max_depth):
    current_depth = set_route.shape[0]

    if current_depth > max_depth:
        return np.uint8(max_depth)
    copy_dominated_set = np.copy(dominated_set) # Realiza una copia de los vertices dominados
    copy_dominated_set[vertex_index] = 1        # Se marca asi mismo com dominado
    
    


    for j, val in enumerate(adjacency_matrix[vertex_index]):   # Itera sobre sobre la fila I de la matriz de adjacencia
        if val > 0:                                 # Evalua si existe una arista de I->J
            copy_dominated_set[j] = 1

    
    is_this_dom_set = np.bool_(True)
    for i, vertex in enumerate(copy_dominated_set):
        if vertex == 0:
            is_this_dom_set = np.bool_(False)
            max_depth = generalized_leaf_removal(
                adjacency_matrix, 
                np.uint8(i),
                copy_dominated_set, 
                np.append(set_route,i),
                max_depth
            )

    if is_this_dom_set:
        # print("max_depth:",max_depth)
        with objmode():  # annotate return type
            dom_set.append(set_route)
        return np.uint8(current_depth)
    return np.uint8(max_depth)

@jit(["Tuple((float32, uint8[:]))(float32[:,:],uint8[:])"], nopython = True)
def get_mds_value(adjacency_matrix, dominating_set):
    # print(dominating_set)
    dominated_vertex = np.zeros((adjacency_matrix.shape[0]),dtype=np.uint8)
    # print(dominated_vertex)

    acumulated_value = np.float32(0)
    for j, val in enumerate(dominated_vertex):
        
        edge_value = np.float32(0)
        for i in dominating_set:
            if adjacency_matrix[i][j] > edge_value:
                edge_value = adjacency_matrix[i][j]
                dominated_vertex[j] = i
        acumulated_value = acumulated_value + edge_value
    
    return acumulated_value, dominated_vertex


@jit(["Tuple((uint8[:], float32, uint8[:]))(float32[:,:],uint8[:,:])"], nopython = True)
def best_option_from_dom_set(adjacency_matrix, mds_sets):
    best_set_index = np.uint8(0)
    best_set_value = np.float32(0)
    set_domination = np.array([0],dtype=np.uint8)
    for i, val in enumerate(mds_sets):
        value,domination = get_mds_value(adjacency_matrix,mds_sets[i])
        if value > best_set_value:
            best_set_value = value
            best_set_index = i
            set_domination = domination
    return mds_sets[best_set_index],best_set_value, set_domination

def min_dom_set(adjacency_matrix):
    # print(adjacency_matrix)
    number_of_vertex = np.uint8(len(adjacency_matrix[0]))
    numpy_matrix = np.array(adjacency_matrix, dtype=np.float32)
    max_depth = np.uint8(max_dom_set_items(number_of_vertex))
    # vertex_priority = get_order(numpy_matrix,number_of_vertex)
    intial_dominated_set = np.zeros(number_of_vertex, dtype=np.uint8)
    # dom_set_list = np.array([])
    for i in range(0, number_of_vertex):
        max_depth = generalized_leaf_removal(
            numpy_matrix,
            np.uint8(i),
            intial_dominated_set,
            np.array([i], dtype = np.uint8),
            max_depth

        )
    mds = np.array([])
#   >>> ys = np.array([])
#   >>> ys = np.vstack([ys, xs]) if ys.size else xs
    for i in dom_set:
        if i.shape[0] == max_depth:
            mds = np.vstack((mds,i)) if mds.size else i
            # mds = np.vstack((mds,i))
    for i in mds:
        print(i)
    
    best_set,value, set_domination = best_option_from_dom_set(numpy_matrix, np.array(mds, dtype = np.uint8))
    print(best_set,value, set_domination)
        


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
                np.array(list(comb),dtype=np.uint8), 
                np.uint8(vertex_len)
                ) == True:
                dominating_sets.append(comb)
            # print(comb)
            pass
    best_set,value, set_domination = best_option_from_dom_set(np.array(adjacency_matrix, dtype=np.float32), np.array(dominating_sets, dtype = np.uint8))
    print(best_set,value, set_domination)
    return dominating_sets
    