from Graph import Graph
from typing import List, Tuple

def load_graph_from_file(file_path: str) -> Graph:
    """
    Load graph from file.
    
    Format:
        First line: <num_vertices> <directed|undirected>
        Second line (optional): vertex labels separated by spaces
        Subsequent lines: <vertex1> <vertex2> (one edge per line)
    
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
        # If the line doesn't contain exactly 2 integers, treat it as labels
        try:
            if len(parts) > 2:
                # Looks like labels
                graph.set_vertex_labels(parts)
                current_line += 1
        except:
            pass
    
    # Parse edges
    for line in lines[current_line:]:
        parts = line.split()
        if len(parts) < 2:
            continue
        
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
        
        graph.add_edge(u, v)
    
    return graph

def print_graph_info(graph: Graph):
    """Print basic information about the graph."""
    print(f"Graph type: {'Directed' if graph.directed else 'Undirected'}")
    print(f"Number of vertices: {graph.num_vertices}")
    
    # Count edges
    edge_count = 0
    for i in range(graph.num_vertices):
        for j in range(graph.num_vertices):
            if graph.has_edge(i, j):
                edge_count += 1
    
    if not graph.directed:
        edge_count //= 2  # Each undirected edge is counted twice
    
    print(f"Number of edges: {edge_count}")
    print()

def print_adjacency_matrix(graph: Graph):
    """Print the adjacency matrix of the graph."""
    print("Adjacency Matrix:")
    print("    " + " ".join(f"{label:>3}" for label in graph.vertex_labels))
    
    for i in range(graph.num_vertices):
        row_str = f"{graph.vertex_labels[i]:>3} "
        for j in range(graph.num_vertices):
            row_str += f"{graph.adj_matrix[i][j]:>3} "
        print(row_str)
    print()

def print_c3_result(graph: Graph, has_c3: bool, method: str):
    """Print the result of C_3 detection."""
    print(f"{'='*60}")
    print(f"C_3 Detection Result ({method})")
    print(f"{'='*60}")
    
    if has_c3:
        print("✓ Graph CONTAINS at least one C_3 cycle (triangle)")
    else:
        print("✗ Graph DOES NOT contain any C_3 cycle (triangle)")
    
    print(f"{'='*60}")
    print()

def print_c3_cycles(graph: Graph, cycles: List[Tuple[int, int, int]]):
    """Print all found C_3 cycles."""
    if not cycles:
        print("No C_3 cycles found.")
        return
    
    print(f"\nFound {len(cycles)} C_3 cycle(s):")
    print(f"{'='*60}")
    
    for i, (u, v, w) in enumerate(cycles, 1):
        label_u = graph.vertex_labels[u]
        label_v = graph.vertex_labels[v]
        label_w = graph.vertex_labels[w]
        print(f"{i}. Triangle: {label_u} - {label_v} - {label_w}")
        print(f"   Vertex indices: ({u}, {v}, {w})")
    
    print(f"{'='*60}")
    print()

def print_single_c3_cycle(graph: Graph, cycle: Tuple[int, int, int]):
    """Print a single C_3 cycle."""
    print(f"\nFound C_3 cycle:")
    print(f"{'='*60}")
    
    u, v, w = cycle
    label_u = graph.vertex_labels[u]
    label_v = graph.vertex_labels[v]
    label_w = graph.vertex_labels[w]
    
    print(f"Triangle: {label_u} - {label_v} - {label_w}")
    print(f"Vertex indices: ({u}, {v}, {w})")
    
    if graph.directed:
        print("\nEdges in the cycle:")
        if graph.has_edge(u, v) and graph.has_edge(v, w) and graph.has_edge(w, u):
            print(f"  {label_u} → {label_v}")
            print(f"  {label_v} → {label_w}")
            print(f"  {label_w} → {label_u}")
        else:
            print(f"  {label_u} → {label_w}")
            print(f"  {label_w} → {label_v}")
            print(f"  {label_v} → {label_u}")
    else:
        print("\nEdges in the triangle:")
        print(f"  {label_u} - {label_v}")
        print(f"  {label_v} - {label_w}")
        print(f"  {label_w} - {label_u}")
    
    print(f"{'='*60}")
    print()

def print_matrix_multiplication_demo(graph: Graph):
    """Demonstrate the matrix multiplication approach."""
    print(f"\n{'='*60}")
    print("Matrix Multiplication Approach Demonstration")
    print(f"{'='*60}")
    
    print("\nAdjacency Matrix A:")
    print_matrix(graph.adj_matrix, graph.vertex_labels)
    
    # Calculate A^2
    A2 = graph.multiply_matrices(graph.adj_matrix, graph.adj_matrix)
    print("\nA² (number of paths of length 2):")
    print_matrix(A2, graph.vertex_labels)
    
    # Calculate A^3
    A3 = graph.multiply_matrices(A2, graph.adj_matrix)
    print("\nA³ (number of paths of length 3):")
    print_matrix(A3, graph.vertex_labels)
    
    # Show trace
    trace = sum(A3[i][i] for i in range(graph.num_vertices))
    print(f"\nTrace of A³: {trace}")
    
    if not graph.directed:
        num_triangles = trace // 6
        print(f"Number of triangles: {trace} / 6 = {num_triangles}")
        print("(Each triangle is counted 6 times in undirected graphs)")
    else:
        num_cycles = trace // 3
        print(f"Number of C_3 cycles: {trace} / 3 = {num_cycles}")
        print("(Each cycle is counted 3 times in directed graphs)")
    
    print(f"{'='*60}")
    print()

def print_matrix(matrix: List[List[int]], labels: List[str]):
    """Print a matrix with labels."""
    n = len(matrix)
    
    # Determine column width based on maximum value
    max_val = max(max(row) for row in matrix)
    width = max(3, len(str(max_val)) + 1)
    
    # Header
    print("    " + " ".join(f"{label:>{width}}" for label in labels))
    
    # Rows
    for i in range(n):
        row_str = f"{labels[i]:>3} "
        for j in range(n):
            row_str += f"{matrix[i][j]:>{width}} "
        print(row_str)

def create_sample_graphs():
    """Create sample graph files for testing."""
    import os
    
    # Create graphs directory if it doesn't exist
    os.makedirs('graphs', exist_ok=True)
    
    # Sample 1: Simple triangle (undirected)
    with open('graphs/triangle.txt', 'w') as f:
        f.write("# Simple triangle graph\n")
        f.write("3 undirected\n")
        f.write("A B C\n")
        f.write("0 1\n")
        f.write("1 2\n")
        f.write("2 0\n")
    
    # Sample 2: Graph with multiple triangles (undirected)
    with open('graphs/multiple_triangles.txt', 'w') as f:
        f.write("# Graph with multiple triangles\n")
        f.write("5 undirected\n")
        f.write("A B C D E\n")
        f.write("0 1\n")
        f.write("1 2\n")
        f.write("2 0\n")
        f.write("2 3\n")
        f.write("3 4\n")
        f.write("4 2\n")
        f.write("0 3\n")
    
    # Sample 3: Graph without triangles (undirected)
    with open('graphs/no_triangles.txt', 'w') as f:
        f.write("# Graph without triangles (tree)\n")
        f.write("5 undirected\n")
        f.write("A B C D E\n")
        f.write("0 1\n")
        f.write("0 2\n")
        f.write("1 3\n")
        f.write("1 4\n")
    
    # Sample 4: Directed graph with cycle
    with open('graphs/directed_cycle.txt', 'w') as f:
        f.write("# Directed graph with C_3 cycle\n")
        f.write("4 directed\n")
        f.write("A B C D\n")
        f.write("0 1\n")
        f.write("1 2\n")
        f.write("2 0\n")
        f.write("1 3\n")
        f.write("3 2\n")
    
    # Sample 5: Complete graph K4
    with open('graphs/complete_k4.txt', 'w') as f:
        f.write("# Complete graph K4 (contains 4 triangles)\n")
        f.write("4 undirected\n")
        f.write("A B C D\n")
        f.write("0 1\n")
        f.write("0 2\n")
        f.write("0 3\n")
        f.write("1 2\n")
        f.write("1 3\n")
        f.write("2 3\n")
    
    print("Sample graph files created in 'graphs/' directory")
