
import numpy as np
from numba import jit,objmode



@jit(["boolean(float32[:])"], nopython = True)
def verificar_regla_1(arr):
    for i in arr:
        if i != np.float32(0):
            print(i)
            return np.bool_(False)

    return np.bool_(True)

# k: cardinalidad
# S_k: Set de nodos evaluados (posible dominantes)
# C_k = V - S_k
# C_k se dividie en C_k- (revisados) C_k+(No revisados) 
# F_k: Set de nodos no dominados


    

# @jit(["uint32[:](float32[:], float32[:])"], nopython = True)
# def verificar_regla_2(arr_domina_a, arr_dominado_por):
    
#     candidatos_regla_2 = np.empty(0, dtype=np.uint32)

#     # Verifica que j no tiene domina a nadie
#     for i in arr_domina_a:
#         if i != np.float32(0):
#             return candidatos_regla_2
#     # Verifica que vertice k no tiene domina a nadie
#     for i, val in enumerate(arr_dominado_por):
#         if val > 0:
#             candidatos_regla_2 = np.append(candidatos_regla_2, i)



#     return candidatos_regla_2


@jit(["uint32[:](float32[:,:],uint32[:],uint32[:],uint32[:])"], nopython = True)
def analizar_estado(numpy_matrix, set_vacio, set_ocupado, set_observado ):
    # candidatos_regla_1 = np.empty(0, dtype=np.uint32)
    # candidatos_regla_2 = np.empty(0, dtype=np.uint32)
    # edge_regla_3 = np.empty(0, dtype=np.uint32)
    candidatos = np.empty(0, dtype=np.uint32)

    # 1- Si un vertice i no tiene a nadie que lo domine en el grafo actual, este vertice se considera como candidato a vertice dominante
    for vertex in set_vacio:
        lo_dominan = numpy_matrix[:,vertex]
        if verificar_regla_1(lo_dominan):
            candidatos = np.append(candidatos, vertex)

    if candidatos.size > 0:
        return candidatos
    # 2- Si un vertice j tiene un unico vertice que lo puede dominar (vertice k) y j no tiene a quien dominar, k es candidato set dominante
    # for vertex in set_vacio:
    #     domina_a = numpy_matrix[vertex]
    #     dominado_por = numpy_matrix[:,vertex]
    #     candidatos_regla_2 = np.unique( np.append(candidatos_regla_2, verificar_regla_2(domina_a,)))

        



    # 3- Si un vertice l  puede dominar a solo un vertice (vertice m)
    return candidatos

@jit(["Tuple((float32[:,:],uint32[:]))(float32[:,:],uint32)"], nopython = True)
def eliminar_hoja(numpy_matrix, indice_vertice):
    set_observado = np.empty(0, dtype=np.uint32)
    for j, val in enumerate(numpy_matrix[indice_vertice]):
        if val >0:
            set_observado = np.append(set_observado, np.uint32(j))

        numpy_matrix[indice_vertice][j] = np.float32(0) #los que domina
        numpy_matrix[j][indice_vertice] = np.float32(0)

    return numpy_matrix, set_observado
    



@jit(["boolean(float32[:,:])"], nopython = True)
def encontrar_mds(numpy_matrix):
    set_vacio = np.arange(0,len(numpy_matrix[0]),1, dtype=np.uint32)
    set_ocupado = np.empty(0, dtype=np.uint32)
    set_observado = np.empty(0, dtype=np.uint32) # dominante
    print("Inicial")
    print(numpy_matrix)
    lista_candidatos = analizar_estado(numpy_matrix,  set_vacio, set_ocupado, set_observado)
    for vertice_indice in lista_candidatos:
        # instancia unica
        set_ocupado = np.unique(np.append(set_ocupado, vertice_indice))
        numpy_matrix, observado = eliminar_hoja(numpy_matrix, vertice_indice)
        set_observado = np.unique(np.append(set_observado, observado))
        set_vacio = np.setdiff1d(set_vacio, observado)
        print("Reduccion", vertice_indice)
        print(numpy_matrix)
        print(set_ocupado)
        print(set_observado)
        print(set_vacio)
    
    return np.bool_(False)


