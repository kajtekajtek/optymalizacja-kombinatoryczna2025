from Graph import Graph
import networkx as nx
import matplotlib.pyplot as plt

def load_graph_from_file(file_path: str) -> Graph:
    with open(file_path, 'r') as f:
        lines = f.readlines()

        print(lines[0].strip().lower())

        if lines[0].strip().lower() == 'd':
            directed = True
        elif lines[0].strip().lower() == 'u':
            directed = False
        else:
            raise ValueError('Error: first line must be "d" or "n"')

        lines = lines[1:]
        n = max(max(map(int, line.split())) for line in lines) + 1

        graph = Graph(n, directed)
        for line in lines:
            u, v = map(int, line.split())
            graph.add_edge(u, v)

        return graph

def print_statistics(graph: Graph):
    print(f"Number of nodes: {graph.get_number_of_nodes()}")
    print(f"Number of edges: {graph.get_number_of_edges()}")
    print(f"Number of even degree nodes: {graph.get_even_degree_count()}")
    print(f"Number of odd degree nodes: {graph.get_odd_degree_count()}")
    print(f"Minimum degree: {graph.get_min_degree()}")
    print(f"Maximum degree: {graph.get_max_degree()}")
    print(f"Sorted degrees: {graph.get_sorted_degrees()}")

def print_matrix(graph: Graph):
    for row in graph.matrix: print(row)

def save_graph_visualization_to_file(graph: Graph, file_path: str):
    if graph.directed:
        nx_graph = nx.DiGraph()
    else:
        nx_graph = nx.Graph()

    for i in range(graph.n):
        nx_graph.add_node(i)

    for u in range(graph.n):
        for v in range(graph.n):
            if graph.matrix[u][v]:
                if graph.directed:
                    nx_graph.add_edge(u, v)
                else:
                    if u <= v and graph.matrix[u][v]:
                        nx_graph.add_edge(u, v)

    pos = nx.spring_layout(nx_graph)
    nx.draw(nx_graph, pos, with_labels=True, node_color='lightblue', edge_color='gray', node_size=500, font_size=10, arrows=graph.directed)
    plt.title("Graph visualization")
    
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"Graph saved to {file_path}")
    plt.close()
