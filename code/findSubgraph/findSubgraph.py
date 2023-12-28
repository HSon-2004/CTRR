import networkx as nx
import math
from networkx.algorithms import isomorphism
from pyvis.network import Network
from IPython.display import display, HTML



#==========================[READ FILE FUNCTION]============================#
def read_graph_from_tsv(file_path):
    G = nx.Graph()
    with open(file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split()
            if len(parts) >= 2:
                # load source vertix, destination vertix, and weight
                u, v, weight = map(int, parts[:3])  
                G.add_node(u)
                G.add_node(v)
                G.add_edge(u, v, weight=weight)
    return G
#==========================================================================#

file_path1 = 'testcase_1_G.edgelist' # File graph G
file_path2 = 'testcase_1_H.edgelist' # File graph H

# Read graph from file
my_graph = read_graph_from_tsv(file_path1)

# Define a small pattern graph for subgraph isomorphism
pattern_graph = read_graph_from_tsv(file_path2)

# Find subgraph isomorphism using NetworkX
subgraph_isomorphisms = list(nx.algorithms.isomorphism.GraphMatcher(my_graph, pattern_graph).subgraph_isomorphisms_iter())
if (subgraph_isomorphisms):
    print("There are subgraph isomorphism")
else:
    print("There are not subgraph isomorphism")
    exit()
# Load the number nodes of pattern_graph 
num_nodes =pattern_graph.number_of_nodes()

# Count the number of subgraphs
count = 0
for subgraph in subgraph_isomorphisms:
    count += 1
# Because the order of the nodes does not matter
count=count/math.factorial(num_nodes) 
# Print the number of subgraphs
print("Number of subgraph isomorphisms:", count)

# Identify nodes in a found subgraph
pos=0
list_nodes=[]
subgraph=str(subgraph_isomorphisms[0])
for i in range(num_nodes):
    if(pos==0): 
        pos=subgraph.find(':')
    else:
        pos = subgraph.find(':', pos + 1)
    if(pos!=-1):
        list_nodes.append(int(subgraph[pos-1]))

# Set color the main graph the matched subgraphs 
for i in my_graph.nodes:
    my_graph.nodes[i]['color']='#00BFFF'
for i in list_nodes:
    my_graph.nodes[i]['color']='red'
for edge in my_graph.edges:
    my_graph.edges[edge]['color'] = '#00BFFF'
for i in list_nodes:
    for j in list_nodes:
        if my_graph.has_edge(i, j):
            my_graph.edges[(i, j)]['color'] = 'red'

# Visualize the main graph and the matched subgraphs
net = Network(
    notebook=True,
    cdn_resources="remote",
    bgcolor="white",
    font_color="750px",
    height="750px",
    width="100%",
    select_menu=True,
    filter_menu=True,
)

net.from_nx(my_graph)
net.toggle_physics(False)
display(HTML(net.generate_html()))
# Save the html file of the graph by the name "networkx_pyvis.html"
net.save_graph("networkx_pyvis.html")
HTML(filename="networkx_pyvis.html")