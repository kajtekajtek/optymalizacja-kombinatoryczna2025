from Graph import Graph
from typing import List, Tuple

def load_graph_from_file(file_path: str) -> Graph:
    """
    Load weighted graph from file.
    
    Format:
        First line: <num_vertices> <directed|undirected>
        Second line (optional): vertex labels separated by spaces
        Subsequent lines: <vertex1> <vertex2> <weight> (one edge per line)
    
    Args:
        file_path: Path to the graph file
        
    Returns:
        Graph object loaded from file
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip() and not line.strip().startswith('#')]
    
    if not lines:
        raise ValueError("File is empty")
    
    # First line: number of vertices and graph type
    first_line = lines[0].split()
    num_vertices = int(first_line[0])
    directed = first_line[1].lower() == 'directed' if len(first_line) > 1 else False
    
    graph = Graph(num_vertices, directed)
    
    current_line = 1
    
    # Check if second line contains vertex labels
    if current_line < len(lines):
        parts = lines[current_line].split()
        # If the line doesn't contain exactly 2-3 numbers, treat it as labels
        try:
            if len(parts) > 3:
                # Looks like labels
                graph.set_vertex_labels(parts)
                current_line += 1
            elif len(parts) == 3:
                # Could be edge or labels - try parsing as numbers
                float(parts[0])
                float(parts[1])
                float(parts[2])
                # It's an edge, not labels
            else:
                # Likely labels
                graph.set_vertex_labels(parts)
                current_line += 1
        except (ValueError, IndexError):
            # If parsing fails, assume it's labels
            if len(parts) > 2:
                graph.set_vertex_labels(parts)
                current_line += 1
    
    # Parse edges
    for line in lines[current_line:]:
        parts = line.split()
        if len(parts) < 2:
            continue
        
        # Parse weight (default to 1.0 if not provided)
        weight = 1.0
        if len(parts) >= 3:
            try:
                weight = float(parts[2])
            except ValueError:
                print(f"Warning: Invalid weight '{parts[2]}', using 1.0 for edge: {line}")
        
        # Try to parse as integers (indices) or as labels
        try:
            u = int(parts[0])
            v = int(parts[1])
        except ValueError:
            # Try to find labels
            try:
                u = graph.vertex_labels.index(parts[0])
                v = graph.vertex_labels.index(parts[1])
            except ValueError:
                print(f"Warning: Skipping invalid edge: {line}")
                continue
        
        graph.add_edge(u, v, weight)
    
    return graph

def print_graph_info(graph: Graph):
    """Print basic information about the graph."""
    print(f"Graph type: {'Directed' if graph.directed else 'Undirected'}")
    print(f"Number of vertices: {graph.num_vertices}")
    
    # Count edges and calculate total weight
    edge_count = 0
    total_weight = 0.0
    for i in range(graph.num_vertices):
        for j in range(graph.num_vertices):
            if graph.has_edge(i, j):
                edge_count += 1
                total_weight += graph.get_weight(i, j)
    
    if not graph.directed:
        edge_count //= 2  # Each undirected edge is counted twice
        total_weight /= 2  # Each undirected edge weight is counted twice
    
    print(f"Number of edges: {edge_count}")
    print(f"Total weight: {total_weight:.2f}")
    print()

def print_adjacency_matrix(graph: Graph):
    """Print the weighted adjacency matrix of the graph."""
    print("Weighted Adjacency Matrix:")
    print("    " + " ".join(f"{label:>8}" for label in graph.vertex_labels))
    
    for i in range(graph.num_vertices):
        row_str = f"{graph.vertex_labels[i]:>3} "
        for j in range(graph.num_vertices):
            weight = graph.get_weight(i, j)
            if weight == 0:
                row_str += f"{'0':>8} "
            else:
                row_str += f"{weight:>8.2f} "
        print(row_str)
    print()

def print_mst_result(graph: Graph, mst_edges: List[Tuple[int, int, float]], total_weight: float, algorithm: str):
    """Print the MST result."""
    print(f"{'='*80}")
    print(f"Minimum Spanning Tree ({algorithm})")
    print(f"{'='*80}")
    print()

    if not mst_edges:
        print("No MST found. Graph may be disconnected.")
        return
    
    print(f"Total weight: {total_weight:.2f}")
    print(f"Number of edges: {len(mst_edges)}")
    print()
    
    print("Edges in MST:")
    print(f"{'From':<10} {'To':<10} {'Weight':<10}")
    print("-" * 30)
    
    for u, v, weight in sorted(mst_edges):
        label_u = graph.vertex_labels[u]
        label_v = graph.vertex_labels[v]
        print(f"{label_u:<10} {label_v:<10} {weight:<10.2f}")
    
    print()
    print(f"{'='*80}")
    print()

def print_mst_adjacency_matrix(graph: Graph, mst_edges: List[Tuple[int, int, float]]):
    """Print the MST as an adjacency matrix."""
    print("MST Adjacency Matrix:")
    print("    " + " ".join(f"{label:>8}" for label in graph.vertex_labels))
    
    # Create MST adjacency matrix
    mst_matrix = [[0.0 for _ in range(graph.num_vertices)] for _ in range(graph.num_vertices)]
    for u, v, weight in mst_edges:
        mst_matrix[u][v] = weight
        mst_matrix[v][u] = weight
    
    for i in range(graph.num_vertices):
        row_str = f"{graph.vertex_labels[i]:>3} "
        for j in range(graph.num_vertices):
            weight = mst_matrix[i][j]
            if weight == 0:
                row_str += f"{'0':>8} "
            else:
                row_str += f"{weight:>8.2f} "
        print(row_str)
    print()

def save_mst_visualization(graph: Graph, mst_edges: List[Tuple[int, int, float]], filename: str = 'mst_visualization.png'):
    """Save a visualization of the MST using networkx and matplotlib."""
    try:
        import networkx as nx
        import matplotlib.pyplot as plt
        
        # Create graph
        G = nx.Graph()
        
        # Add all vertices
        for i in range(graph.num_vertices):
            G.add_node(i, label=graph.vertex_labels[i])
        
        # Add all edges from original graph (in light gray)
        for i in range(graph.num_vertices):
            for j in range(i + 1, graph.num_vertices):
                if graph.has_edge(i, j):
                    weight = graph.get_weight(i, j)
                    G.add_edge(i, j, weight=weight, color='lightgray', style='dashed')
        
        # Create MST set for quick lookup
        mst_set = set()
        for u, v, _ in mst_edges:
            mst_set.add((u, v))
            mst_set.add((v, u))
        
        # Highlight MST edges
        for u, v, weight in mst_edges:
            if G.has_edge(u, v):
                G[u][v]['color'] = 'red'
                G[u][v]['style'] = 'solid'
                G[u][v]['weight'] = weight
        
        # Create layout
        pos = nx.spring_layout(G, k=1, iterations=50)
        
        # Draw graph
        plt.figure(figsize=(12, 8))
        
        # Draw all edges
        edges = G.edges()
        colors = [G[u][v].get('color', 'black') for u, v in edges]
        styles = [G[u][v].get('style', 'solid') for u, v in edges]
        
        for (u, v), color, style in zip(edges, colors, styles):
            nx.draw_networkx_edges(G, pos, edgelist=[(u, v)], edge_color=color, 
                                  style=style, width=2, alpha=0.6)
        
        # Draw nodes
        nx.draw_networkx_nodes(G, pos, node_color='lightblue', 
                              node_size=1000, alpha=0.9)
        
        # Draw labels
        labels = {i: graph.vertex_labels[i] for i in range(graph.num_vertices)}
        nx.draw_networkx_labels(G, pos, labels, font_size=10, font_weight='bold')
        
        # Draw edge labels (weights)
        edge_labels = {}
        for u, v in G.edges():
            weight = G[u][v].get('weight', 1.0)
            edge_labels[(u, v)] = f'{weight:.1f}'
        nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
        
        plt.title("Minimum Spanning Tree\n(Red edges = MST, Gray edges = other edges)", 
                 fontsize=14, fontweight='bold')
        plt.axis('off')
        plt.tight_layout()
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"MST visualization saved to: {filename}")
        plt.close()
        
    except ImportError:
        print("Warning: networkx or matplotlib not available. Skipping visualization.")
    except Exception as e:
        print(f"Warning: Could not create visualization: {e}")
