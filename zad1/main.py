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

def main():
    graph = load_graph_from_file('directed_graph.txt')
    print(graph.get_sorted_degrees())
    for row in graph.matrix: print(row)

def load_graph_from_file(file_path: str) -> Graph:
    with open(file_path, 'r') as f:
        lines = f.readlines()
        directed = lines[0].strip() == 'directed'
        lines = lines[1:]
        n = max(max(map(int, line.split())) for line in lines) + 1

        graph = Graph(n, directed)
        for line in lines:
            u, v = map(int, line.split())
            graph.add_edge(u, v)

        return graph

if __name__ == "__main__":
    main()