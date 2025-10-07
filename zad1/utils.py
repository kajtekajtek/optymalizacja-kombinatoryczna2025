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
from Graph import Graph

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