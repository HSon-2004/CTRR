import networkx as nx

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

# Đường dẫn đến file TSV cục bộ
file_path1 = 'test_2.edgelist'
file_path2 = 'test_1.edgelist'

# Đọc đồ thị từ file TSV
my_graph = read_graph_from_tsv(file_path1)
pattern_graph = read_graph_from_tsv(file_path2)

# Tiếp tục xử lý subgraph isomorphism như trong mã gốc của bạn
subgraph_isomorphisms = list(nx.algorithms.isomorphism.GraphMatcher(my_graph, pattern_graph).subgraph_isomorphisms_iter())

formatted_subgraphs = []
for subgraph in subgraph_isomorphisms:
    formatted_subgraph_str = ', '.join(f'{pattern_node} {my_graph_node}' for pattern_node, my_graph_node in subgraph.items())
    formatted_subgraphs.append(formatted_subgraph_str)

formatted_subgraphs_str = '\n'.join(formatted_subgraphs)

# Write formatted subgraph isomorphisms to a text file
with open('formatted_subgraphs.txt', 'w') as f:
    f.write(formatted_subgraphs_str)

# Check if there are any subgraph isomorphisms
if subgraph_isomorphisms:
    print("Có một đồ thị con đồng đẳng.")
else:
    print("Không tìm thấy đồ thị con đồng đẳng.")
