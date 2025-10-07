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
from utils import load_graph_from_file, print_statistics, print_matrix

def main():
    graph = load_graph_from_file('graphs/undirected_1.txt')
    print_statistics(graph)
    print_matrix(graph)

if __name__ == "__main__":
    main()