class Graph:
    def __init__(self, n: int, directed: bool = False):
        self.n = n
        self.matrix = [[0] * n for _ in range(n)]
        self.directed = directed

    def add_edge(self, u: int, v: int):
        self.matrix[u][v] = 1
        if not self.directed:
            self.matrix[v][u] = 1

    def remove_edge(self, u: int, v: int):
        self.matrix[u][v] = 0
        if not self.directed:
            self.matrix[v][u] = 0

    def get_degree(self, u: int) -> int:
        if self.directed:
            return self.get_out_degree(u) + self.get_in_degree(u)
        else:
            return sum(self.matrix[u])

    def get_in_degree(self, u: int) -> int:
        return sum(self.matrix[i][u] for i in range(self.n))

    def get_out_degree(self, u: int) -> int:
        return sum(self.matrix[u][i] for i in range(self.n))

    def get_min_degree(self) -> int:
        return min(sum(row) for row in self.matrix)

    def get_max_degree(self) -> int:
        return max(sum(row) for row in self.matrix)

    def get_even_degree_count(self) -> int:
        return sum(1 for i in range(self.n) if self.get_degree(i) % 2 == 0)

    def get_odd_degree_count(self) -> int:
        return sum(1 for i in range(self.n) if self.get_degree(i) % 2 == 1)

    def get_sorted_degrees(self) -> list[int]:
        return sorted((self.get_degree(i) for i in range(self.n)), reverse=True)