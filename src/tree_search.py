from numba.core.types.misc import Object
import numpy as np
from numba import jit,objmode
from numpy.lib import copy
import time

from graph_algorithms import check_dom_set


GO_TO_STEP_2 = np.uint32(0)
GO_TO_STEP_6 = np.uint32(1)

@jit(["uint32[:](float32[:,:], uint32)"], nopython = True)
def Gamma_function_vertex(numpy_matrix, vertex_i):
    domination_set = np.empty(0, dtype=np.uint32)
    for j, val in enumerate(numpy_matrix[vertex_i]):
        if vertex_i != j and  numpy_matrix[vertex_i][j] >= np.float32(5):
            domination_set = np.append(domination_set, np.uint32(j))
    return domination_set


@jit(["boolean(float32[:,:], uint32[:], uint32[:])"], nopython = True)
def feasibility_test(numpy_matrix, F_k, C_k_plus):

    for i in C_k_plus: # revisa el item
        # print(i)
        for j in F_k:
            if i != j and numpy_matrix[i][j] >= np.float32(5):
                # print("[",i,"]", "[",j,"]:", numpy_matrix[i][j])
                return np.bool_(True)  
    return np.bool_(False)

@jit(["uint32(float32[:,:], uint32[:], uint32)"], nopython = True)
def is_dominated(numpy_matrix, Set_k, vertex):
    for i in Set_k:
        if numpy_matrix[i][vertex] >= 5:
            return np.uint32(1) 
    return np.uint32(0)

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


@jit(["boolean(float32[:,:], uint32, uint32[:])"], nopython = True)
def check_if_is_dominated_by_set(numpy_matrix, q, dom_set ):
    is_dominated = np.bool_(False)
    for i in dom_set:
        if i != q and numpy_matrix[i][q] >= 5:
            return np.bool_(True)
    return is_dominated


dom_set = []
@jit(["uint32(float32[:,:], uint32[:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def action_step_5(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k):
    if F_k.size == 0:
        # printt("Es dominante", Set_k)
        # printt("Con F_k:", F_k)
        with objmode():
            dom_set.append(Set_k)
        return GO_TO_STEP_6
    else:
        
        return GO_TO_STEP_2
    


@jit(["uint32(float32[:,:], uint32[:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def action_step_4(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k): # es minimal
    Set_k_prev = np.copy(Set_k[:-1]) # S_{k-1}

    go_tp_step = np.uint32(5)
    for q in Set_k_prev:
        # printt("check if", q, "dom by", Set_k)
        if check_if_is_dominated_by_set(numpy_matrix, q, Set_k_prev) == True: # verifica si es minimo
            # # printt(Set_k, "paso 6", F_k)
            go_tp_step = np.uint32(6)
            break
    if go_tp_step == 5:
        # # printt("Fk",F_k)
        return action_step_5(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k)

    elif go_tp_step == 6: 
        for q_index, q in enumerate(Set_k_prev): # antes de ir al paso 6 verfica que cumpla la condicion
            dom_set_no_q = np.delete(np.copy(Set_k), q_index)
            for j in Gamma_function_vertex(numpy_matrix, np.uint32(q)):
                if j in Set_k or is_dominated(numpy_matrix, dom_set_no_q, j):
                    return GO_TO_STEP_6
    return action_step_5(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k)


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


    while feasibility_test(numpy_matrix, F_k, C_k_plus):

        next_Set_k, C_k_plus,C_k_minus, next_F_k = action_step_3(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k) # reduccion para el el siguiente estado

        if next_Set_k[0] == 131 and (next_Set_k[1] == 120 and next_Set_k[2] == 97 ):
            print("Set S", Set_k,"->", next_Set_k, next_F_k)
        if next_F_k.size == 0:
            with objmode():
                dom_set.append(next_Set_k)
        

        go_to = action_step_4(numpy_matrix, next_Set_k, C_k_plus,C_k_minus, next_F_k) # evaluacion de si el posible set va al paso 2 o 6

        if go_to == GO_TO_STEP_2:
            action_step_2(numpy_matrix, next_Set_k, C_k_plus,C_k_minus, next_F_k)


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
    tic = time.time()
    initialisation(np.array(matrix, dtype=np.float32))
    toc = time.time()
    print("time:", toc-tic)
    print("Dom set")
    for i in dom_set:
        print(i)