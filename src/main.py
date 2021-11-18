from data_manager import DataManager
import graph_functions as gf
import networkx as nx



if __name__ == "__main__":
    dm = DataManager(r"E:\Users\Victor\Documents\GitHub\graph-theory-mu-chart\datasets\84-char-smash.csv")
    mu_graph = nx.DiGraph()    

    vertex_list = dm.get_vertex_list() 
    
    gf.add_vertex_list(mu_graph, vertex_list)
    

    # armar grafo completo
    for i,character in enumerate(vertex_list):
        winning_mu = dm.get_character_winning_mu(vertex_list[i]) # obtiene los MU ganadores
        gf.add_edge_list(mu_graph, vertex_list[i], winning_mu)
        print(i, character)

    # dominating_sets = gf.get_all_dominating_sets_brute_force(mu_graph)
    # print(f"Dominating sets: {dominating_sets}")
    min_dominating_sets = gf.get_min_dominating_sets_brute_force(mu_graph)
    print(f"Min dominating sets: {min_dominating_sets}")

    gf.draw_graph(mu_graph)
    # print(answer)
    # print(gm.get_dominant_set_default())
    # gm.draw_graph()
    # print(vertex_list)
    # dm.get_char_mu(vertex_list[1])