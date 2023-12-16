import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt

def draw_graph_from_file(file_path):
    try:
        # Đọc dữ liệu từ file TSV với delimiter là tab và không có header
        df = pd.read_csv(file_path, delimiter='\t', header=None, names=['edge', 'vertice', 'weight'])

        # Tạo đồ thị
        G = nx.Graph()

        # Thêm cạnh vào đồ thị
        for edge_name in df['edge']:
            nodes = edge_name.split('-')  # Assuming the edge name is in the format "A-B"
            G.add_edge(*nodes)

        # Vẽ đồ thị
        pos = nx.spring_layout(G)
        nx.draw_networkx_nodes(G, pos)
        nx.draw_networkx_labels(G, pos)
        nx.draw_networkx_edges(G, pos)

        plt.show()

    except Exception as e:
        print(f"An error occurred: {e}")

# Sử dụng ví dụ
file_path = 'ktruss_example.tsv'  # Thay thế bằng đường dẫn đến file của bạn
draw_graph_from_file(file_path)
