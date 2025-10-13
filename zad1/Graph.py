# Zaimplementuj odpowiednie struktury danych i procedury pozwalające na 
# przechowywanie grafu (skierowanego (S) i nieskierowanego (N)) w postaci 
# macierzy sąsiedztwa oraz: 
# - dodanie/usunięcie krawędzi/wierzchołka (S/N)
# - wyznaczenie stopnia wierzchołka (w przypadku grafu skierowanego rozważyć 
#   stopnie wchodzące i wychodzące) (S/N) oraz minimalnego (N) i maksymalnego 
#   stopnia grafu (N)
# - wyznaczenie, ile jest wierzchołków stopnia parzystego i nieparzystego (N)
# - wypisanie (posortowanego nierosnąco) ciągu stopni wierzchołków w grafie (N)

# - przedstaw graficznie wprowadzony graf
# - Program powinien być odporny na błędy użytkownika.
# - graf może być przekazany przez użytkownika za pomocą pliku tekstowego
#   (np. lista krawędzi).
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

    def add_node(self):
        self.n += 1
        self.matrix.append([0] * self.n)
        for row in self.matrix:
            row.append(0)

    def remove_node(self, u: int):
        self.n -= 1
        self.matrix.pop(u)
        for row in self.matrix:
            row.pop(u)

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

    def get_number_of_edges(self) -> int:
        total = sum(sum(row) for row in self.matrix)
        if not self.directed:
            return total // 2
        else:
            return total
    
    def get_number_of_nodes(self) -> int:
        return self.n