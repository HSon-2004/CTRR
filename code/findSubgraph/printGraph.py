import networkx as nx
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file
with open("Graph.edgelist", "r") as file:
    lines = file.readlines()

# Tạo đồ thị
G = nx.Graph()

# Thêm cạnh và trọng số từ dữ liệu
for line in lines:
    parts = line.strip().split()
    if len(parts) >= 2:
        u, v = map(int, parts[:2])  # Giữ lại chỉ số đỉnh
        weight = float(parts[-1].split(':')[-1].strip('}'))  # Chuyển đổi trọng số từ chuỗi thành số
        G.add_edge(u, v, weight=weight)

# Vẽ đồ thị
pos = nx.spring_layout(G)
nx.draw(G, pos, with_labels=False, font_size=8, font_color="black", node_size=20, node_color="skyblue", edge_color="gray", font_weight="bold", width=1, alpha=0.7)

#pos = nx.spring_layout(G)
#nx.draw(G, pos, with_labels=True, font_size=8, font_color="black", node_size=20, node_color="skyblue", edge_color="gray", font_weight="bold", width=2, alpha=0.7)



# Hiển thị đồ thị
plt.savefig("output.png",dpi=3000)
