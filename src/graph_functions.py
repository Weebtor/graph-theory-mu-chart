from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import math
import itertools

from networkx.algorithms import dominating

# class GraphManager():
#     def __init__(self) -> None:
#         self.graph = nx.DiGraph()
    
#     def draw_graph(self):
#         nx.draw(self.graph)
#         plt.savefig("filename.png")
#         #   nx.draw(G, arrows=True, arrowsize=20, with_labels=True, node_color='#00b4d9', edge_color=('g', 'r', 'g', 'g', 'r', 'g', 'g', 'r'), node_size=2000)
#     def print_graph_info(self):
#         print("Info:",self.graph)
#         print("Nodes:",self.graph.nodes)
#         print("Edges:",self.graph.edges)

#     def check_if_dominant_set(self, char_list):
#         nbunch = self.graph.nbunch_iter(char_list)
#         return nx.is_dominating_set(self.graph,nbunch)




#     def generate_graph_vertex(self, character_list:list) -> None:
#         for character in character_list:
#             self.graph.add_node(character)

#     def generate_graph_edges(self, character: str, mu_dict: dict):
#         for vs_char, mu_result in mu_dict.items():
#             self.graph.add_edge(character, vs_char, weight=mu_result)
#             print(f"{character}-{mu_result}->{vs_char}")
#         # self.graph
    
#     def get_graph_vertex_list(self):

#         return self.graph.nodes


#     def get_all_dominating_sets_brute_force(self):

#         dominating_sets = []

#         vertex_list = self.get_graph_vertex_list() # Lista de vertices
#         length = len(vertex_list)  # Largo de la lista 
#         log2n = math.log2(length)  # Maxiño atamaño del set dominate
#         max_dom_set_items = int(log2n) + int(log2n % 1 > 0) # Se aproxima
#         print(vertex_list)
#         print(max_dom_set_items)

#         # counter = 0
#         for n in range(1,max_dom_set_items + 1):
#             print(n)
#             for comb in itertools.combinations(vertex_list,n):
#                 if self.check_if_dominant_set(list(comb)):
#                     dominating_sets.append(comb)
#                     print(comb)

#         return dominating_sets

#     def get_min_dominating_sets_brute_force(self):
#         dominating_sets = []

#         vertex_list = self.get_graph_vertex_list() # Lista de vertices
#         length = len(vertex_list)  # Largo de la lista 
#         log2n = math.log2(length)  # Maxiño atamaño del set dominate
#         max_dom_set_items = int(log2n) + int(log2n % 1 > 0) # Se aproxima
#         print(vertex_list)
#         print(max_dom_set_items)

#         # counter = 0
#         for n in range(1,max_dom_set_items + 1):
#             if len(dominating_sets) > 0:
#                 break 
#             print(n)
#             for comb in itertools.combinations(vertex_list,n):
#                 if self.check_if_dominant_set(list(comb)):
#                     dominating_sets.append(comb)
#                     print(comb)

#         return dominating_sets
                    

            

#         # for i in range(len(vertex_list) + 1):
#         #     combinations_object = itertools.combinations(vertex_list, i)
#         #     combinations_list = list(combinations_object)
            
#         #     if len(combinations_list) > max_dom_set_items:
#         #         for combination in combinations_list:
#         #             print(combination)
#         #         break 



def draw_graph(digraph) -> None:
    nx.draw(digraph)
    plt.savefig("filename.png")

def print_graph_info(digraph) -> None:
    print("Info:",digraph)
    print("Nodes:",digraph.nodes)
    print("Edges:",digraph.edges)

def check_if_dominant_set(digraph, char_list) -> None:
    nbunch = digraph.nbunch_iter(char_list)
    return nx.is_dominating_set(digraph,nbunch)

def add_vertex_list(digraph:nx.DiGraph,character_list:list) -> None:
    for character in character_list:
        digraph.add_node(character)

def add_edge_list(digraph:nx.DiGraph, character: str, mu_dict: dict):
    for vs_char, mu_result in mu_dict.items():
        digraph.add_edge(character, vs_char, weight=mu_result)
        # print(f"{character}-{mu_result}->{vs_char}")

def get_all_dominating_sets_brute_force(digraph):

    dominating_sets = []

    vertex_list = digraph.nodes # Lista de vertices
    length = len(vertex_list)  # Largo de la lista 
    log2n = math.log2(length)  # Maxiño atamaño del set dominate
    max_dom_set_items = int(log2n) + int(log2n % 1 > 0) # Se aproxima
    # print(vertex_list)
    # print(max_dom_set_items)

    # counter = 0
    for n in range(1,max_dom_set_items + 1):
        # print(n)
        for comb in itertools.combinations(vertex_list,n):
            if check_if_dominant_set(digraph,list(comb)):
                dominating_sets.append(comb)
                # print(comb)

    return dominating_sets


def get_min_dominating_sets_brute_force(digraph):
    dominating_sets = []

    vertex_list = digraph.nodes # Lista de vertices
    length = len(vertex_list)  # Largo de la lista 
    log2n = math.log2(length)  # Maxiño atamaño del set dominate
    max_dom_set_items = int(log2n) + int(log2n % 1 > 0) # Se aproxima
    print("Total of characters:",length)
    print("Limite de cantidad de pj:", max_dom_set_items)

    # print(max_dom_set_items)

    # counter = 0
    for n in range(1,max_dom_set_items + 1):

        if len(dominating_sets) > 0:
            break

        print("Revisando para n=",n)
        for comb in itertools.combinations(vertex_list,n):
            if check_if_dominant_set(digraph, list(comb)):
                dominating_sets.append(comb)
                print(comb)

    return dominating_sets