import numpy as np
from numba import jit,objmode

from graph_algorithms import check_dom_set


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
        #counter + 1 -
    
    return best_option, best_index

@jit(["uint32[:](float32[:,:], uint32, uint32[:])"], nopython = True)
def reduce_by_union_domination(numpy_matrix, vertex_index, F_k):
    # dominated = np.empty(0, dtype=np.uint32)
    # for j, val in enumerate(numpy_matrix[vertex_index]):
    #     if val >= 5:
    #         dominated = np.append(dominated, np.uint32(j))

    to_del = np.empty(0, dtype=np.uint32)
    for j, index in enumerate(F_k):
        # print(numpy_matrix[vertex_index][index])
        if numpy_matrix[vertex_index][index] >= 5:
            to_del = np.append(to_del, np.uint32(j))

    # print(to_del)
    return np.delete(F_k, to_del)

@jit(["Tuple((uint32[:], uint32[:], uint32[:], uint32[:]))(float32[:,:], uint32[:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def action_step_3(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k):
    r_k_vertex, r_k_index = select_max_brach(numpy_matrix, F_k, C_k_plus, Set_k)
    Set_k = np.append(Set_k, r_k_vertex)   # S_{k+1} <- S_{k} + r_{k} 
    C_k_plus = np.delete(C_k_plus, r_k_index)       # C_{k+1}+ <- C_{k+1}+ - r_{k}
    C_k_minus = np.append(C_k_minus, r_k_vertex)
    F_k = reduce_by_union_domination(numpy_matrix, r_k_index, F_k)
    # F_k = np.union1d(F_k, get_dominated_set(numpy_matrix, r_k_index))

    return Set_k, C_k_plus,C_k_minus, F_k

@jit(["boolean(float32[:,:], uint32, uint32[:])"], nopython = True)
def check_if_is_dominated_by_set(numpy_matrix, q, dom_set ):
    is_dominated = np.bool_(False)
    for i in dom_set:
        if i != q and numpy_matrix[i][q] >= 5:
            return np.bool_(True)
    return is_dominated
    

@jit(["void(float32[:,:], uint32[:], uint32[:], uint32[:], uint32[:])"], nopython = True)
def action_step_4(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k):
    Set_k_prev = np.copy(Set_k[:-1])
    print("Set_k", Set_k)
    print("Set_k_prev", Set_k_prev)

    for q_index, q in enumerate(Set_k_prev):
        if check_if_is_dominated_by_set(numpy_matrix, q, Set_k) == True:
            print(q, "cumple con ?")
            gamma_set = Gamma_function_vertex(numpy_matrix, np.uint32(q))
            print("q domina a", gamma_set)
            dom_set_no_q = np.delete(np.copy(Set_k), q_index)
            print("no q", dom_set_no_q)
            go_step_5 = np.bool_(True)
            for j in gamma_set:
                if j in Set_k or is_dominated(numpy_matrix, dom_set_no_q, j) == False:
                    print(j, "pertenece a", Set_k)
                    go_step_6 = np.bool_(False)
                    print("Go step 6")
                    # Go step 5
                    break
            if go_step_5:
                print("Go step 5")

            # Go step 5

        else:
            print(q, "no cumple con ?")
            # Go step 5
    
    # for i in Set_k:
    #     for q in Set_k_prev:
    #         ev_2 = np.bool_(False) 
    #         if i != q and numpy_matrix[i][q] >= np.float32(5):
    #             # Step 6?
    #             break
    pass

@jit(["void(float32[:,:])"], nopython = True)
def initialisation(numpy_matrix): # Step 1
    Set_k = np.empty(0, dtype=np.uint32)
    C_k_minus = np.empty(0, dtype=np.uint32)
    C_k_plus = np.arange(0,len(numpy_matrix[0]),1, dtype=np.uint32)
    F_k = np.arange(0,len(numpy_matrix[0]),1, dtype=np.uint32)
    # Step 2: Ver si es factible
    if feasibility_test(numpy_matrix, F_k, C_k_plus):
        print("es factible")
        Set_k, C_k_plus,C_k_minus, F_k = action_step_3(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k) # it 1
        print(Set_k)
        print(C_k_plus)
        print(C_k_minus)
        print("Non dominated:",F_k)
        Set_k, C_k_plus,C_k_minus, F_k = action_step_3(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k) # it 2
        print(Set_k)
        print(C_k_plus)
        print(C_k_minus)
        print("Non dominated:",F_k)
        action_step_4(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k)
        Set_k, C_k_plus,C_k_minus, F_k = action_step_3(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k) # it 3
        print(Set_k)
        print(C_k_plus)
        print(C_k_minus)
        print("Non dominated:",F_k)
        action_step_4(numpy_matrix, Set_k, C_k_plus,C_k_minus, F_k)
        

    # Step 3: Elegir vertice
    else:
        print("No es factible -> Step 6")
        

    

def run(matrix):
    initialisation(np.array(matrix, dtype=np.float32))