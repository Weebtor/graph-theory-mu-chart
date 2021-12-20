import re
from numba.core.types.misc import Object
import numpy as np
from numba import jit,objmode
from numpy.lib import copy
import time

from graph_algorithms import check_dom_set


GO_TO_STEP_2 = np.uint32(2)
GO_TO_STEP_5 = np.uint32(5)
GO_TO_STEP_6 = np.uint32(6)



@jit(["uint32[:](float32[:,:], uint32[:])"], nopython = True)
def neighbor_of_set(numpy_matrix, vertex_set):
    not_neighbor = np.arange(0,len(numpy_matrix[0]),1, dtype=np.uint32)
    domination_set = np.empty(0, dtype=np.uint32)
    for i in vertex_set:
        index_to_delete = np.empty(0, dtype=np.uint32)
        for vertex_j_index, j  in enumerate(not_neighbor):
            if i != j and numpy_matrix[i][j]:
                domination_set = np.append(domination_set, np.uint32(j))
                index_to_delete = np.append(index_to_delete, np.uint32(vertex_j_index))
        not_neighbor = np.delete(not_neighbor, index_to_delete)

    return domination_set


@jit(["boolean(float32[:,:], uint32[:], uint32[:])"], nopython = True)
def feasibility_test(numpy_matrix, F_k, C_k_plus):
    # Paso 2: Prueba de factibilidad
    for i in C_k_plus: # revisa el item
        for j in F_k:
            if i != j and numpy_matrix[i][j] >= np.float32(5):
                return np.bool_(True)  
    return np.bool_(False)

@jit(["boolean(float32[:,:], uint32[:], uint32)"], nopython = True)
def is_dominated(numpy_matrix, Set_k, vertex):
    for i in Set_k:
        if numpy_matrix[i][vertex] >= 5:
            return np.bool_(True)
    return np.bool_(False)

@jit(["Tuple((uint32,uint32))(float32[:,:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def select_max_brach(numpy_matrix, F_k, C_k_plus, Set_k):
    best_option = np.uint32(C_k_plus[0])
    best_index = np.uint32(0)
    best_val = np.uint32(0)
    for index, i in enumerate(C_k_plus):
        counter = np.uint32(0)
        for j in F_k:
            if i != j and numpy_matrix[i][j] >= 5:
                counter += 1
            
        counter = counter + (1 - is_dominated(numpy_matrix, Set_k, i)) 
        if counter > best_val:
            best_option = np.uint32(i)
            best_val = np.uint32(counter)
            best_index = np.uint32(index)

    
    return best_option, best_index

@jit(["uint32[:](float32[:,:], uint32, uint32[:])"], nopython = True)
def reduce_by_union_domination(numpy_matrix, vertex_i, F_k):
    operation_F_k = np.copy(F_k)
    to_del = np.empty(0, dtype=np.uint32) # set dominado

    for j_index, vertex_j in enumerate(F_k):
        if vertex_j == vertex_i or numpy_matrix[vertex_i][vertex_j] >= 5:
            to_del = np.append(to_del, np.uint32(j_index))

    operation_F_k = np.delete(operation_F_k, to_del)
    return operation_F_k


@jit(["boolean(float32[:,:], uint32[:], uint32)"], nopython = True)
def check_if_is_dominated_by_set(numpy_matrix, Set_k, q ):
    # Set_k domina -> q
    for dom_vertex in Set_k: # se revisa por cada vertice si lo domina
        if dom_vertex != q and numpy_matrix[dom_vertex][q] >= 5:
            return np.bool_(True)
    return np.bool_(False)


dom_set = []
profundidad = [100000]
@jit(["uint32(float32[:,:], uint32[:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def action_step_5(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k):
    
    if F_k.size == 0:
        print("-> Agregado", Set_k)
        with objmode():
            
            if profundidad[0] > Set_k.size:
                profundidad[0] = Set_k.size
                dom_set.clear()
            dom_set.append(Set_k)
        return GO_TO_STEP_6
    else:
        
        return GO_TO_STEP_2
    


@jit(["uint32(float32[:,:], uint32[:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def minimality_test(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k): # es minimal
    Set_k_prev = np.copy(Set_k[:-1]) # S_{k-1}
    if F_k.size == 0:
        return action_step_5(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k)
        # print("Is dom set", Set_k)
    # is not minimal if q in Sk -> q in N(Sk) and 
    for q_index, q in enumerate(Set_k_prev):
        if q in neighbor_of_set(numpy_matrix, Set_k):
            for j in neighbor_of_set(numpy_matrix, np.array([q], dtype=np.uint32)):
                dom_set_no_q = np.delete(np.copy(Set_k), q_index)
                if j in Set_k or is_dominated(numpy_matrix, dom_set_no_q, j):
                    # print("then set", Set_k, "is not minimal", q,"->",j)
                    return GO_TO_STEP_2
    
    return action_step_5(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k)

    

    # # evaluation = GO_TO_STEP_5
    # for q_index, q in enumerate(Set_k_prev): # q in S k-1
    #     # printt("check if", q, "dom by", Set_k)
    #     if check_if_is_dominated_by_set(numpy_matrix, Set_k, q ) == True: # verifica si es minimo
    #         # si existe un q en N(s_k) hay que hacer verificar la siguiente seccion y hacer backtracking
    #         # evaluation = np.uint32(6)
            
    #         break

    #     return GO_TO_STEP_5
    # # if evaluation == 6:
    # #     for q_index, q in enumerate(Set_k_prev): # antes de ir al paso 6 verfica que cumpla la condicion
    # #         dom_set_no_q = np.delete(np.copy(Set_k), q_index) # Set k sin q
    # #         for j in Gamma_function_vertex(numpy_matrix, np.uint32(q)): # por cada j en L(q)
    # #             if not (j in Set_k or is_dominated(numpy_matrix, dom_set_no_q, j) == False):
    # #                 break
            

    # #     return GO_TO_STEP_6

    # return action_step_5(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k)


@jit(["Tuple((uint32[:], uint32[:], uint32[:], uint32[:]))(float32[:,:], uint32[:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def action_step_3(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k):
    # copias en caso de que los punteros jodan
    Set_k_copy = np.copy(Set_k)
    C_k_plus_copy = np.copy(C_k_plus)       # C_{k+1}+ <- C_{k+1}+ - r_{k}
    C_k_minus_copy = np.copy(C_k_minus)
    F_k_copy = np.copy(F_k)
    r_k_vertex, r_k_index = select_max_brach(numpy_matrix, F_k, C_k_plus, Set_k)

    # Reduccion
    Set_k_copy = np.append(Set_k_copy, r_k_vertex)
    C_k_plus_copy = np.delete(C_k_plus_copy, r_k_index)
    C_k_minus_copy = np.append(C_k_minus_copy, r_k_vertex)
    F_k_copy = reduce_by_union_domination(numpy_matrix, r_k_vertex, F_k_copy)
    return Set_k_copy, C_k_plus_copy,C_k_minus_copy, F_k_copy





@jit(["void(float32[:,:], uint32[:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def action_step_2(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k):
    max_depth = np.uint32(0)
    with objmode(max_depth="uint32"):
        max_depth = profundidad[0]
    
    # print(max_depth)
    if max_depth > Set_k.size:


        while feasibility_test(numpy_matrix, F_k, C_k_plus):
            

            next_Set_k, C_k_plus,C_k_minus, next_F_k = action_step_3(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k) # reduccion para el el siguiente estado

            # if next_Set_k[0] == 131 and (next_Set_k[1] == 120 and next_Set_k[2] == 97 ):
            #     print("Set S", Set_k,"->", next_Set_k, next_F_k)
            # if next_F_k.size == 0:
            #     with objmode():
            #         dom_set.append(next_Set_k)
            

            go_to = minimality_test(numpy_matrix, next_Set_k, C_k_plus,C_k_minus, next_F_k) # evaluacion de si el posible set va al paso 2 o 6

            if go_to == GO_TO_STEP_2:
                action_step_2(numpy_matrix, next_Set_k, C_k_plus,C_k_minus, next_F_k)
            
        else:
            return

    else:
        return
    



@jit(["void(float32[:,:])"], nopython = True)
def initialisation(numpy_matrix):
    # Paso 1: iniciar
    Set_k = np.empty(0, dtype=np.uint32)
    C_k_minus = np.empty(0, dtype=np.uint32)
    C_k_plus = np.arange(0,len(numpy_matrix[0]),1, dtype=np.uint32)
    F_k = np.arange(0,len(numpy_matrix[0]),1, dtype=np.uint32)
    # k = Set_k.size
    action_step_2(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k)

    # Step 2: Ver si es factible
    # if feasibility_test(numpy_matrix, F_k, C_k_plus):
    #     # printt("es factible")
    #     Set_k, C_k_plus,C_k_minus, F_k = action_step_3(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k) # it 1
    #     # printt(Set_k)
    #     # printt(C_k_plus)
    #     # printt(C_k_minus)
    #     # printt("Non dominated:",F_k)
        

    


        

    

def run(matrix):
    # print(matrix[7][12])
    # print(matrix[3][12])
    matrix = np.array(matrix, dtype=np.float32)
    print(matrix)
    tic = time.time()
    initialisation(matrix)
    toc = time.time()
    print("Dom set Tree Search")
    print("time:", toc-tic)
    print("Total elementos:", len(dom_set))
    for i in dom_set:
        print(i)