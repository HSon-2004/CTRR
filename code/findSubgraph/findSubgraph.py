import networkx as nx
import matplotlib.pyplot as plt

def read_graph_from_tsv(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                u, v = map(int, parts[:2])  # Giữ lại chỉ số đỉnh
                weight = float(parts[-1].split(':')[-1].strip('}'))  # Chuyển đổi trọng số từ chuỗi thành số
                G.add_edge(u, v, weight=weight)
    return G


file_path1 = 'Graph.edgelist'
file_path2 = 'subGraph.edgelist'
# Read graph from TSV file
my_graph = read_graph_from_tsv(file_path1)

# Define a small pattern graph for subgraph isomorphism
pattern_graph = read_graph_from_tsv(file_path2)

# Find subgraph isomorphism using NetworkX
subgraph_isomorphisms = list(nx.algorithms.isomorphism.GraphMatcher(my_graph, pattern_graph).subgraph_isomorphisms_iter())

# Print the subgraph isomorphisms
# print("Subgraph Isomorphisms:")
# for subgraph in subgraph_isomorphisms:
#     print(subgraph)

# Visualize the main graph and the matched subgraphs
pos = nx.spring_layout(my_graph, k=0.15, iterations=100) 

nx.draw(my_graph, pos, node_size=20,  
        with_labels=False,
        font_size=5, 
        node_color='skyblue',
        alpha = 0.7, 
        font_weight='regular',
        linewidths=0.2, 
        edge_color='0.3')

nx.draw(pattern_graph, pos,  
        node_size=100,
        font_size=5,
        node_color='red',
        font_weight='regular',
        edge_color='red', 
        linewidths=1)

plt.axis("off")
plt.savefig("output1.png",dpi=3000)

