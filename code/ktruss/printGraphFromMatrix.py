import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import zipfile
import io

def read_edge_matrix_from_file(file_path, encoding='utf-8'):
    try:
        with open(file_path, 'r', encoding=encoding, errors='replace') as file:
            edge_matrix = [list(map(int, line.strip().split())) for line in file]
    except UnicodeDecodeError:
        # If decoding as text fails, try treating it as a ZIP archive
        with zipfile.ZipFile(file_path, 'r') as zip_file:
            # Assuming the ZIP archive contains a single text file
            first_file = zip_file.namelist()[0]
            with zip_file.open(first_file) as text_file:
                content = io.TextIOWrapper(text_file, encoding=encoding, errors='replace')
                edge_matrix = [list(map(int, line.strip().split())) for line in content]

    return np.array(edge_matrix)

def draw_graph_from_edge_matrix(edge_matrix, output_file=None):
    G = nx.DiGraph()
    num_edges, num_vertices = edge_matrix.shape
    
    for edge in range(num_edges):
        for vertex in range(num_vertices):
            if edge_matrix[edge][vertex] == 1:
                G.add_edge(edge, vertex)

    pos = nx.spring_layout(G)
    nx.draw(G, pos, with_labels=True, arrows=True, connectionstyle="arc3,rad=0.1")
    
    if output_file:
        plt.savefig(output_file)
    else:
        plt.show()

# Usage
file_path = "ktruss_matrix.txt"
output_image_file = "graph_image.png"
edge_matrix = read_edge_matrix_from_file(file_path)
draw_graph_from_edge_matrix(edge_matrix, output_file=output_image_file)

