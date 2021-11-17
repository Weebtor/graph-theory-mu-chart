import networkx as nx
import matplotlib.pyplot as plt

class GraphManager():
    def __init__(self) -> None:
        self.graph = nx.DiGraph()
    
    def draw_graph(self):
        nx.draw(self.graph)
        plt.savefig("filename.png")
        #   nx.draw(G, arrows=True, arrowsize=20, with_labels=True, node_color='#00b4d9', edge_color=('g', 'r', 'g', 'g', 'r', 'g', 'g', 'r'), node_size=2000)
    def print_graph_info(self):
        print("Info:",self.graph)
        print("Nodes:",self.graph.nodes)
        print("Edges:",self.graph.edges)

    def check_if_dominant_set(self, char_list):
        nbunch = self.graph.nbunch_iter(char_list)
        return nx.is_dominating_set(self.graph,nbunch)

    def get_dominant_set_default(self):
        return nx.dominating_set(self.graph, 'Ryu')



    def generate_graph_vertex(self, character_list:list) -> None:
        for character in character_list:
            self.graph.add_node(character)

    def generate_graph_edges(self, character: str, mu_dict: dict):
        for vs_char, mu_result in mu_dict.items():
            self.graph.add_edge(character, vs_char, weight=mu_result)
            print(f"{character}-{mu_result}->{vs_char}")
        # self.graph
    