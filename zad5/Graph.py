from typing import List, Tuple, Optional
import copy
import sys

class Graph:
    """
    Weighted graph representation using adjacency matrix.
    Supports both directed and undirected graphs with edge weights.
    """
    
    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices  = num_vertices
        self.directed      = directed
        # Store weights (0 means no edge, non-zero means edge with that weight)
        self.adj_matrix    = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
        self.vertex_labels = [str(i) for i in range(num_vertices)]
    
    def set_vertex_labels(self, labels: List[str]):
        """Set custom labels for vertices."""
        if len(labels) != self.num_vertices:
            raise ValueError(f"Number of labels ({len(labels)}) must match number of vertices ({self.num_vertices})")
        self.vertex_labels = labels
    
    def add_edge(self, u: int, v: int, weight: float = 1.0):
        """
        Add an edge between vertices u and v with optional weight.
        For unweighted graphs, weight defaults to 1.0.
        """
        if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
            raise ValueError(f"Vertex indices must be in range [0, {self.num_vertices})")
        
        self.adj_matrix[u][v] = weight
        if not self.directed:
            self.adj_matrix[v][u] = weight
    
    def has_edge(self, u: int, v: int) -> bool:
        """Check if there is an edge between u and v."""
        return self.adj_matrix[u][v] != 0
    
    def get_weight(self, u: int, v: int) -> float:
        """Get the weight of edge (u, v). Returns 0 if no edge exists."""
        return self.adj_matrix[u][v]
    
    def get_adjacency_matrix(self) -> List[List[int]]:
        return copy.deepcopy(self.adj_matrix)
    
    # finding C_3 cycles using the naive approach
    
    def has_c3_naive(self) -> bool:
        """
        Naive approach to check if graph contains a C_3 cycle (triangle).
        Complexity: O(n^3) where n is the number of vertices
        Returns:
            True if graph contains at least one C_3 cycle, False otherwise
        """
        n = self.num_vertices
        
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if self._is_triangle(i, j, k):
                        return True
        
        return False
    
    def _is_triangle(self, i: int, j: int, k: int) -> bool:
        """
        Check if three vertices form a triangle.
        - For undirected graphs: all three edges must exist
        - For directed graphs: check for a cycle i->j->k->i
        """
        if not self.directed:
            return (self.has_edge(i, j) and 
                    self.has_edge(j, k) and 
                    self.has_edge(k, i))
        else:
            return ((self.has_edge(i, j) and self.has_edge(j, k) 
                    and self.has_edge(k, i)) or (self.has_edge(i, k) 
                    and self.has_edge(k, j) and self.has_edge(j, i)))
    
    def find_one_c3_naive(self) -> Optional[Tuple[int, int, int]]:
        """
        Find and return one C_3 cycle if it exists using naive approach.
        Returns:
            Tuple of three vertex indices forming a triangle, or None if no triangle exists
        """
        n = self.num_vertices
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if self._is_triangle(i, j, k):
                        return (i, j, k)
        
        return None
    
    def find_all_c3_naive(self) -> List[Tuple[int, int, int]]:
        """
        Find all C_3 cycles in the graph using naive approach.
        
        Returns:
            List of tuples, each containing three vertex indices forming a triangle
        """
        n = self.num_vertices
        triangles = []
        for i in range(n):
            for j in range(i + 1, n):
                for k in range(j + 1, n):
                    if self._is_triangle(i, j, k):
                        triangles.append((i, j, k))
        return triangles
    
    # finding C_3 cycles using the matrix multiplication approach

    def multiply_matrices(self, A: List[List[int]], B: List[List[int]]) -> List[List[int]]:
        """
        Custom implementation of matrix multiplication.
        Args:
            A: First matrix (n x m)
            B: Second matrix (m x p)
        Returns:
            Result matrix (n x p)
        """
        n = len(A)
        m = len(B)
        p = len(B[0]) if m > 0 else 0
        
        if not A or not B:
            raise ValueError("Matrices cannot be empty")
        
        if len(A[0]) != m:
            raise ValueError("Matrix dimensions don't match for multiplication")
        
        result = [[0 for _ in range(p)] for _ in range(n)]
        
        for i in range(n):
            for j in range(p):
                for k in range(m):
                    result[i][j] += A[i][k] * B[k][j]
        
        return result
    
    def has_c3_matrix(self) -> bool:
        """
        Check if graph contains a C_3 cycle using matrix multiplication.
        - Matrix A (adjacency matrix) represents the graph.
        - Matrix A^2 gives the number of walks of length 2.
        - Matrix A^3 gives the number of walks of length 3; 
          if the diagonal element A[i][i] is non-zero, there's a cycle 
          of length 3 starting and ending at the vertex i.
        Complexity: O(n^3) for matrix multiplication, but more efficient in practice
        Returns:
            True if graph contains at least one C_3 cycle, False otherwise
        """
        A2 = self.multiply_matrices(self.adj_matrix, self.adj_matrix)
        A3 = self.multiply_matrices(A2, self.adj_matrix)
        
        for i in range(self.num_vertices):
            if A3[i][i] > 0:
                return True
        
        return False
    
    def count_c3_matrix(self) -> int:
        """
        Count the number of C_3 cycles using matrix multiplication.
        For undirected graphs:
        - Each triangle is counted 6 times (2 directions x 3 starting vertices)
        For directed graphs:
        - Each cycle is counted 3 times (once for each starting vertex)
        Returns:
            Number of C_3 cycles in the graph
        """
        A2 = self.multiply_matrices(self.adj_matrix, self.adj_matrix)
        A3 = self.multiply_matrices(A2, self.adj_matrix)
        trace = sum(A3[i][i] for i in range(self.num_vertices))
        if not self.directed:
            return trace // 6
        else:
            return trace // 3
    
    def find_one_c3_matrix(self) -> Optional[Tuple[int, int, int]]:
        """
        Find one C_3 cycle using matrix multiplication approach.
        
        We use A^2 to help identify potential triangles efficiently.
        If A^2[i][j] > 0 and A[i][j] = 1, then there's a path of length 2 from i to j
        and a direct edge from i to j, which means there's a triangle.
        
        Returns:
            Tuple of three vertex indices forming a triangle, or None if no triangle exists
        """
        n = self.num_vertices
        
        if not self.directed:
            # For undirected: check if there's a common neighbor k for edge (i, j)
            for i in range(n):
                for j in range(i + 1, n):
                    if self.has_edge(i, j):
                        # Check if there's a vertex k connected to both i and j
                        for k in range(n):
                            if k != i and k != j:
                                if self.has_edge(i, k) and self.has_edge(j, k):
                                    return (i, j, k)
        else:
            # For directed: find a directed cycle i->j->k->i
            for i in range(n):
                for j in range(n):
                    if i != j and self.has_edge(i, j):
                        # Look for k such that j->k and k->i
                        for k in range(n):
                            if k != i and k != j:
                                if self.has_edge(j, k) and self.has_edge(k, i):
                                    return (i, j, k)
        
        return None
    
    def find_all_c3_matrix_assisted(self) -> List[Tuple[int, int, int]]:
        """
        Find all C_3 cycles using matrix multiplication to assist the search.
        
        This is a hybrid approach: use A^3 to know triangles exist,
        then find them efficiently using A^2.
        
        Returns:
            List of tuples, each containing three vertex indices forming a triangle
        """
        triangles = []
        n = self.num_vertices
        
        if not self.directed:
            # For undirected: check if there's a common neighbor k for edge (i, j)
            for i in range(n):
                for j in range(i + 1, n):
                    if self.has_edge(i, j):
                        # Check if there's a vertex k connected to both i and j
                        for k in range(j + 1, n):
                            if self.has_edge(i, k) and self.has_edge(j, k):
                                triangles.append((i, j, k))
        else:
            # For directed: find all directed cycles i->j->k->i
            seen = set()
            for i in range(n):
                for j in range(n):
                    if i != j and self.has_edge(i, j):
                        # Look for k such that j->k and k->i
                        for k in range(n):
                            if k != i and k != j:
                                if self.has_edge(j, k) and self.has_edge(k, i):
                                    # Normalize the cycle representation (smallest vertex first)
                                    cycle = tuple(sorted([i, j, k]))
                                    if cycle not in seen:
                                        seen.add(cycle)
                                        triangles.append((i, j, k))
        
        return triangles
    
    def prim_mst(self, start_vertex: int = 0) -> Tuple[List[Tuple[int, int, float]], float]:
        """
        Find Minimum Spanning Tree using Prim's algorithm.
        
        Args:
            start_vertex: Starting vertex for Prim's algorithm (default: 0)
            
        Returns:
            Tuple of (list of edges in MST as (u, v, weight), total weight)
            Edges are represented as (u, v, weight) where u < v for undirected graphs
        """
        if self.directed:
            raise ValueError("Prim's algorithm requires an undirected graph")
        
        n = self.num_vertices
        if n == 0:
            return [], 0.0
        
        # Track which vertices are in MST
        in_mst = [False] * n
        # Track minimum weight edge to connect vertex to MST
        min_weight = [sys.float_info.max] * n
        # Track parent vertex for each vertex in MST
        parent = [-1] * n
        
        # Start with the first vertex
        min_weight[start_vertex] = 0.0
        mst_edges = []
        total_weight = 0.0
        
        # Build MST
        for _ in range(n):
            # Find vertex with minimum weight not yet in MST
            u = -1
            min_val = sys.float_info.max
            for v in range(n):
                if not in_mst[v] and min_weight[v] < min_val:
                    min_val = min_weight[v]
                    u = v
            
            if u == -1:
                # Graph is not connected
                break
            
            # Add u to MST
            in_mst[u] = True
            total_weight += min_weight[u]
            
            # Add edge to MST (skip for first vertex)
            if parent[u] != -1:
                # Store edge with smaller index first
                edge = (min(parent[u], u), max(parent[u], u), min_weight[u])
                mst_edges.append(edge)
            
            # Update min_weight for vertices adjacent to u
            for v in range(n):
                if not in_mst[v] and self.adj_matrix[u][v] != 0:
                    weight = self.adj_matrix[u][v]
                    if weight < min_weight[v]:
                        min_weight[v] = weight
                        parent[v] = u
        
        return mst_edges, total_weight
    
    def kruskal_mst(self) -> Tuple[List[Tuple[int, int, float]], float]:
        """
        Find Minimum Spanning Tree using Kruskal's algorithm with Union-Find.
        
        Returns:
            Tuple of (list of edges in MST as (u, v, weight), total weight)
            Edges are represented as (u, v, weight) where u < v
        """
        if self.directed:
            raise ValueError("Kruskal's algorithm requires an undirected graph")
        
        n = self.num_vertices
        if n == 0:
            return [], 0.0
        
        # Collect all edges
        edges = []
        for u in range(n):
            for v in range(u + 1, n):  # Only upper triangle for undirected
                if self.adj_matrix[u][v] != 0:
                    edges.append((u, v, self.adj_matrix[u][v]))
        
        # Sort edges by weight
        edges.sort(key=lambda x: x[2])
        
        # Union-Find data structure
        parent = list(range(n))
        rank = [0] * n
        
        def find(x: int) -> int:
            """Find root of x with path compression."""
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        def union(x: int, y: int) -> bool:
            """Union sets containing x and y. Returns True if union was successful."""
            root_x = find(x)
            root_y = find(y)
            
            if root_x == root_y:
                return False  # Already in same set
            
            # Union by rank
            if rank[root_x] < rank[root_y]:
                parent[root_x] = root_y
            elif rank[root_x] > rank[root_y]:
                parent[root_y] = root_x
            else:
                parent[root_y] = root_x
                rank[root_x] += 1
            
            return True
        
        # Build MST
        mst_edges = []
        total_weight = 0.0
        
        for u, v, weight in edges:
            if union(u, v):
                mst_edges.append((u, v, weight))
                total_weight += weight
                if len(mst_edges) == n - 1:
                    break  # MST has n-1 edges
        
        return mst_edges, total_weight
    
    def __str__(self) -> str:
        result = f"Graph ({'directed' if self.directed else 'undirected'}, {self.num_vertices} vertices)\n"
        result += "Adjacency Matrix (weights):\n"
        
        # Header with vertex labels
        result += "    " + " ".join(f"{label:>6}" for label in self.vertex_labels) + "\n"
        
        for i, row in enumerate(self.adj_matrix):
            result += f"{self.vertex_labels[i]:>3} " + " ".join(f"{val:>6.1f}" if val != 0 else f"{'0':>6}" for val in row) + "\n"
        
        return result

