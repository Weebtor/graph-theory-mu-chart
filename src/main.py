from data_manager import DataManager
from graph_manager import GraphManager
import networkx as nx


if __name__ == "__main__":
    gm = GraphManager()
    dm = DataManager(r"E:\Users\Victor\Documents\GitHub\graph-theory-mu-chart\datasets\16-char-sf2.csv")    
    vertex_list = dm.get_vertex_list() 
    gm.generate_graph_vertex(vertex_list)
    

    # armar grafo completo
    for i,character in enumerate(vertex_list):
        winning_mu = dm.get_character_winning_mu(vertex_list[i]) # obtiene los MU ganadores
        gm.generate_graph_edges(vertex_list[i], winning_mu)
        print(i, character)

    # gm.print_graph()
    answer = gm.check_if_dominant_set(['Chun-Li', 'Dhalsim', 'Claw', 'Ryu'])
    print(answer)
    print(gm.get_dominant_set_default())
    gm.draw_graph()
    # print(vertex_list)
    # dm.get_char_mu(vertex_list[1])