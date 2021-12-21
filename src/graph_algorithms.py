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
@jit(["uint32(float32[:,:], uint32, uint32[:], uint32[:],uint32, uint32[:])"], nopython = True)
def not_generalized_leaf_removal(adjacency_matrix, vertex_index, dominated_set, set_route, max_depth, useless_set):

    current_depth = set_route.shape[0]

    if current_depth > max_depth:
        return np.uint32(max_depth)
    copy_dominated_set = np.copy(dominated_set) # Realiza una copia de los vertices dominados


    copy_dominated_set[vertex_index] = 2                        # Se marca asi mismo com dominado
    for j, val in enumerate(adjacency_matrix[vertex_index]):    # Itera sobre sobre la fila I de la matriz de adjacencia
        if val > 0:                                             # Evalua si existe una arista de I->J
            copy_dominated_set[j] = 1

    is_this_dom_set = np.bool_(True)

    for i, vertex in enumerate(copy_dominated_set):
        if vertex == 0:
            is_this_dom_set = np.bool_(False)
            max_depth = not_generalized_leaf_removal(adjacency_matrix, np.uint32(i),copy_dominated_set, np.append(set_route,i),max_depth, np.append(useless_set,i))
        # elif vertex == 1: # Verifica si estos vertices son un aporte
        #     evaluacion_copy = np.copy(dominated_set)
        #     for j, val in enumerate(adjacency_matrix[i]):
        #         if val > 0:
        #             evaluacion_copy[j] = 1
        #     # print("ev:",evaluacion_copy)
        #     # print("og:",copy_dominated_set)
        #     resp = np.array_equal(evaluacion_copy,copy_dominated_set )
        #     # print("equal:",resp)
        #     if resp == False and i not in useless_set:
        #         max_depth = not_generalized_leaf_removal(adjacency_matrix, np.uint32(i),copy_dominated_set, np.append(set_route,i),max_depth, np.append(useless_set,i))
        #     elif resp == True:
        #         useless_set = np.append(useless_set,np.uint32(i))


            # print(i, vertex)
            # print(adjacency_matrix)
            # print(copy)
    if is_this_dom_set:
        # print("max_depth:",max_depth)
        with objmode():  # annotate return type
            # print("set_dominante encontrado:",set_route)
            if dom_set["tamaño_actual"] > set_route.size:
                dom_set["sets"] = []
            dom_set["sets"].append(set_route)
        return np.uint32(current_depth)
    return np.uint32(max_depth)



def GLR(adjacency_matrix, max_depth):
    
    # Reglas de GLR:
    # 1- Si un vertice i no tiene a nadie que lo domine en el grafo actual, este vertice se considera como candidato a vertice dominante
    # 2- Si un vertice j tiene un unico vertice que lo puede dominar (vertice k) y j no tiene a quien dominar, k es candidato set dominante
    # 3- Si un vertice l  puede dominar a solo un vertice (vertice m) 

    pass
@jit(["Tuple((float32, uint32[:]))(float32[:,:],uint32[:])"], nopython = True)
def get_mds_value(adjacency_matrix, dominating_set):
    # print(dominating_set)
    dominated_vertex = np.zeros((adjacency_matrix.shape[0]),dtype=np.uint32)
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
    # print(adjacency_matrix)
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
    # print("mds:",mds)
    # for i in dom_set:
    #     if i.size == max_depth:
    #         mds = np.append(mds, i)
    best_set,value, set_domination = best_option_from_dom_set(numpy_matrix, np.array(mds, dtype = np.uint32))
    print(best_set,value, set_domination)
        
def min_dom_set_bruteforce(adjacency_matrix):
    dominating_sets = []
    # print(dominating_sets)
    vertex_index = np.arange(0,len(adjacency_matrix[0]),1)
    vertex_len = len(vertex_index)
    tic = time.time()
    for n in range(1,vertex_len+1):
        if len(dominating_sets) > 0:
            # print(dominating_sets)
            print("Total elementos:", len(dominating_sets))
            break
        print("Revisando para n=",n)
        for comb in itertools.combinations(vertex_index,n):
            # Check if dom set
            if check_dom_set(
                np.array(adjacency_matrix, dtype=np.float32), 
                np.array(list(comb),dtype=np.uint32), 
                np.uint32(vertex_len)
                ) == True:
                
                print("Se encontro el set: ", comb)
                dominating_sets.append(comb)
            # print(comb)
            pass
    toc = time.time()
    print("time:", toc-tic)
    best_set,value, set_domination = best_option_from_dom_set(np.array(adjacency_matrix, dtype=np.float32), np.array(dominating_sets, dtype = np.uint32))
    
    # print(best_set,value, set_domination)
    return best_set,value
    