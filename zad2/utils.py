from FlowNetwork import FlowNetwork
import networkx as nx
import matplotlib.pyplot as plt

def load_flow_network_from_file(file_path: str) -> FlowNetwork:
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    edges = []
    max_node = -1
    for line in lines:
        parts = line.split()
        if len(parts) != 3:
            raise ValueError(f'Invalid line format: "{line}". Expected: u v capacity')
        u, v, capacity = map(int, parts)
        edges.append((u, v, capacity))
        max_node = max(max_node, u, v)
    
    n = max_node + 1
    network = FlowNetwork(n)
    
    for u, v, capacity in edges:
        network.add_edge(u, v, capacity)
    
    return network

def print_network_info(network: FlowNetwork):
    print(f"Number of nodes: {network.get_number_of_nodes()}")
    
    edge_count = sum(1 for i in range(network.n) for j in range(network.n) if network.capacity[i][j] > 0)
    print(f"Number of edges: {edge_count}")
    print()

def print_capacity_matrix(network: FlowNetwork):
    print("Capacity matrix:")
    for row in network.capacity:
        print(row)

def print_flow_results(network: FlowNetwork, max_flow: int, augmenting_paths: list, source: int, sink: int):
    print(f"\n{'='*60}")
    print(f"MAXIMUM FLOW RESULTS")
    print(f"{'='*60}")
    print(f"Source: {source}")
    print(f"Sink: {sink}")
    print(f"Maximum flow value: {max_flow}")
    print(f"Number of augmenting paths found: {len(augmenting_paths)}")
    
    print(f"\n{'='*60}")
    print("AUGMENTING PATHS:")
    print(f"{'='*60}")
    for i, (path, bottleneck) in enumerate(augmenting_paths, 1):
        path_str = ' -> '.join(str(u) for u, _ in reversed(path)) + f' -> {sink}'
        print(f"{i}. Path: {path_str}")
        print(f"   Flow added: {bottleneck}")
    
    print(f"\n{'='*60}")
    print("FINAL FLOW ON EDGES:")
    print(f"{'='*60}")
    for u in range(network.n):
        for v in range(network.n):
            if network.capacity[u][v] > 0:
                flow = network.flow[u][v]
                capacity = network.capacity[u][v]
                print(f"Edge ({u} -> {v}): {flow}/{capacity}")
    print(f"{'='*60}\n")

def save_flow_network_visualization(network: FlowNetwork, file_path: str, show_flow: bool = False):
    nx_graph = nx.DiGraph()
    
    for i in range(network.n):
        nx_graph.add_node(i)
    
    edge_labels = {}
    for u in range(network.n):
        for v in range(network.n):
            if network.capacity[u][v] > 0:
                nx_graph.add_edge(u, v)
                if show_flow:
                    edge_labels[(u, v)] = f"{network.flow[u][v]}/{network.capacity[u][v]}"
                else:
                    edge_labels[(u, v)] = str(network.capacity[u][v])
    
    pos = nx.spring_layout(nx_graph, k=2, iterations=50)
    
    plt.figure(figsize=(12, 8))
    nx.draw(nx_graph, pos, with_labels=True, node_color='lightblue', 
            edge_color='gray', node_size=700, font_size=12, 
            arrows=True, arrowsize=20, arrowstyle='->')
    
    nx.draw_networkx_edge_labels(nx_graph, pos, edge_labels, font_size=10)
    
    if show_flow:
        plt.title("Flow Network - Final Flow (flow/capacity)", fontsize=14)
    else:
        plt.title("Flow Network - Capacities", fontsize=14)
    
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to {file_path}")
    plt.close()
