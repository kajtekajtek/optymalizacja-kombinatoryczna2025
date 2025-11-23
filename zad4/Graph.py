from typing import List, Tuple, Optional
import copy

class Graph:
    """
    Simple graph representation using adjacency matrix.
    Supports both directed and undirected graphs.
    """
    
    def __init__(self, num_vertices: int, directed: bool = False):
        self.num_vertices  = num_vertices
        self.directed      = directed
        self.adj_matrix    = [[0 for _ in range(num_vertices)] for _ in range(num_vertices)]
        self.vertex_labels = [str(i) for i in range(num_vertices)]
    
    def set_vertex_labels(self, labels: List[str]):
        """Set custom labels for vertices."""
        if len(labels) != self.num_vertices:
            raise ValueError(f"Number of labels ({len(labels)}) must match number of vertices ({self.num_vertices})")
        self.vertex_labels = labels
    
    def add_edge(self, u: int, v: int):
        """
        Add an edge between vertices u and v.
        """
        if u < 0 or u >= self.num_vertices or v < 0 or v >= self.num_vertices:
            raise ValueError(f"Vertex indices must be in range [0, {self.num_vertices})")
        
        self.adj_matrix[u][v] = 1
        if not self.directed:
            self.adj_matrix[v][u] = 1
    
    def has_edge(self, u: int, v: int) -> bool:
        return self.adj_matrix[u][v] == 1
    
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
    
    def __str__(self) -> str:
        result = f"Graph ({'directed' if self.directed else 'undirected'}, {self.num_vertices} vertices)\n"
        result += "Adjacency Matrix:\n"
        
        # Header with vertex labels
        result += "    " + " ".join(f"{label:>3}" for label in self.vertex_labels) + "\n"
        
        for i, row in enumerate(self.adj_matrix):
            result += f"{self.vertex_labels[i]:>3} " + " ".join(f"{val:>3}" for val in row) + "\n"
        
        return result

