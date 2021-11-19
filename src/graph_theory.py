from itertools import combinations
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import itertools
from numba import jit


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
    log2n = np.log2(length)  # Maxiño atamaño del set dominate
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

@jit(nopython=True)
def max_dom_set_items(list_size):
    log2n = np.log2(list_size)
    return int(log2n) + int(log2n % 1 > 0)

@jit(nopython=True)
def get_min_dominating_sets_brute_force(digraph):
    dominating_sets = []

    vertex_list = digraph.nodes # Lista de vertices

    max_items = max_dom_set_items(len(vertex_list))
    # print("Total of characters:",length)
    print("Limite de cantidad de pj:", max_items)

    # print(max_dom_set_items)

    # counter = 0
    for n in range(1,max_items + 1):

        if len(dominating_sets) > 0:
            break

        print("Revisando para n=",n)
        for comb in itertools.combinations(vertex_list,n):
            if check_if_dominant_set(digraph, list(comb)):
                dominating_sets.append(comb)
                print(comb)

    return dominating_sets