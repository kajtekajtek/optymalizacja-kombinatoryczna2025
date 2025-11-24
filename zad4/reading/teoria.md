# Wyszukiwanie cyklu $C_3$ w grafie prostym

W teorii grafów **problem ten sprowadza się do znalezienia w grafie trzech wierzchołków, które są połączone każdy z każdym**. W dostarczonym kodzie zaimplementowano dwa główne podejścia do rozwiązania tego problemu: 
- metodę "naiwną" (brute-force) 
- oraz metodę algebraiczną wykorzystującą potęgowanie macierzy sąsiedztwa.

## 1. Podgraf izomorficzny i Cykl $C_3$

**Cykl $C_3$** to cykl o długości 3, potocznie nazywany **trójkątem**. Składa się on z trzech wierzchołków połączonych trzema krawędziami (np. $u-v$, $v-w$, $w-u$).

**Podgraf izomorficzny do $C_3$**: Mówimy, że graf $G$ zawiera podgraf izomorficzny do $C_3$, jeśli wewnątrz $G$ istnieje taki zestaw trzech wierzchołków, które zachowują strukturę trójkąta.
- W grafie nieskierowanym oznacza to istnienie krawędzi między każdą parą z trójki wierzchołków.
- W grafie skierowanym (zależnie od definicji, ale w tym kodzie) szukamy cyklu skierowanego $i \to j \to k \to i$.

W pliku `Graph.py` sprawdzenie to realizuje metoda pomocnicza `_is_triangle`, która weryfikuje istnienie odpowiednich krawędzi w zależności od typu grafu (skierowany/nieskierowany):

```python
# Z pliku Graph.py
def _is_triangle(self, i: int, j: int, k: int) -> bool:
    """
    Check if three vertices form a triangle.
    For undirected graphs: all three edges must exist
    For directed graphs: check for a cycle i->j->k->i
    """
    if not self.directed:
        # Dla nieskierowanych: muszą istnieć wszystkie 3 krawędzie
        return (self.has_edge(i, j) and 
                self.has_edge(j, k) and 
                self.has_edge(k, i))
    else:
        # Dla skierowanych: szukamy cyklu zamkniętego
        return ((self.has_edge(i, j) and self.has_edge(j, k) and self.has_edge(k, i)) or
                (self.has_edge(i, k) and self.has_edge(k, j) and self.has_edge(j, i)))
```

## 2\. Wersja Naiwna (Brute-force)

Metoda naiwna polega na sprawdzeniu wszystkich możliwych trójek wierzchołków w grafie. Jeśli graf ma $n$ wierzchołków, algorytm iteruje przez unikalne kombinacje $(i, j, k)$.

  * **Złożoność obliczeniowa:** $O(n^3)$ – ze względu na trzy zagnieżdżone pętle.
  * **Zasada działania:** Dla każdej trójki sprawdzamy funkcją `_is_triangle`, czy krawędzie istnieją.

Implementacja w `Graph.py`:

```python
# Z pliku Graph.py
def has_c3_naive(self) -> bool:
    """
    Naive approach to check if graph contains a C_3 cycle (triangle).
    Complexity: O(n^3) where n is the number of vertices
    """
    n = self.num_vertices
    
    # Sprawdź wszystkie możliwe trójki wierzchołków
    for i in range(n):
        for j in range(i + 1, n):
            for k in range(j + 1, n):
                # Sprawdź czy wierzchołki i, j, k tworzą trójkąt
                if self._is_triangle(i, j, k):
                    return True
    
    return False
```

## 3\. Wersja w oparciu o mnożenie macierzy

To podejście opiera się na własnościach **macierzy sąsiedztwa** $A$.

  * Macierz $A$ zawiera informację o bezpośrednich połączeniach (ścieżki długości 1).
  * Macierz $A^2 = A \times A$ zawiera liczbę ścieżek o długości 2 między wierzchołkami.
  * Macierz $A^3 = A^2 \times A$ zawiera liczbę ścieżek o długości 3 między wierzchołkami.

Jeśli na przekątnej (diagonali) macierzy $A^3$ znajduje się wartość większa od 0 (np. $A^3[i][i] > 0$), oznacza to, że istnieje ścieżka o długości 3 wychodząca z wierzchołka $i$ i wracająca do niego. W grafie prostym bez pętli własnych taka ścieżka musi być trójkątem ($C_3$).

**Obliczanie liczby trójkątów:**
Ślad macierzy (suma elementów na przekątnej) $Trace(A^3)$ jest powiązany z liczbą trójkątów, ale występuje nadmiarowe zliczanie:

  * Dla grafów **nieskierowanych**: Każdy trójkąt jest liczony 6 razy (3 wierzchołki startowe $\times$ 2 kierunki obiegu). Wynik dzielimy przez 6.
  * Dla grafów **skierowanych**: Każdy cykl jest liczony 3 razy (3 wierzchołki startowe). Wynik dzielimy przez 3.

Implementacja w `Graph.py` (z ręcznym mnożeniem macierzy):

```python
# Z pliku Graph.py
def has_c3_matrix(self) -> bool:
    # Oblicz A^2
    A2 = self.multiply_matrices(self.adj_matrix, self.adj_matrix)
    
    # Oblicz A^3 = A^2 * A
    A3 = self.multiply_matrices(A2, self.adj_matrix)
    
    # Sprawdź elementy na przekątnej A^3
    for i in range(self.num_vertices):
        if A3[i][i] > 0:
            return True
    
    return False

def count_c3_matrix(self) -> int:
    # ... (obliczenie A3 jak wyżej) ...
    
    # Suma elementów na przekątnej (ślad macierzy)
    trace = sum(A3[i][i] for i in range(self.num_vertices))
    
    # Podziel przez 6 dla nieskierowanych, przez 3 dla skierowanych
    if not self.directed:
        return trace // 6
    else:
        return trace // 3
```

-----

## Działanie algorytmu w programie krok po kroku

Analizując plik `main.py`, działanie programu przebiega następująco:

1.  **Inicjalizacja i Argumenty**:
    Program uruchamiany jest z wiersza poleceń. `argparse` parsuje argumenty, takie jak ścieżka do pliku z grafem (`filename`), wybrana metoda (`--method naive/matrix/both`) czy flaga wizualizacji (`--demo`).

2.  **Wczytanie Grafu**:
    Wywoływana jest funkcja `load_graph_from_file` (z `utils.py`). Odczytuje ona liczbę wierzchołków, typ grafu (skierowany/nieskierowany) oraz listę krawędzi, tworząc i wypełniając obiekt klasy `Graph`.

3.  **Metoda 1: Podejście Naiwne** (jeśli wybrano):

      * Program wyświetla nagłówek "METHOD 1: NAIVE APPROACH".
      * Jeśli użyto flagi `--show-all`, uruchamia `graph.find_all_c3_naive()`, która zwraca listę wszystkich znalezionych trójek.
      * W przeciwnym razie uruchamia `graph.find_one_c3_naive()`, która przerywa działanie po znalezieniu pierwszego trójkąta (optymalizacja czasu).
      * Wynik (istnienie trójkąta oraz konkretne wierzchołki) jest wypisywany na ekran.

4.  **Metoda 2: Podejście Macierzowe** (jeśli wybrano):

      * Program wyświetla nagłówek "METHOD 2: MATRIX MULTIPLICATION APPROACH".
      * Algorytm mnoży macierz sąsiedztwa samą przez siebie, aby uzyskać $A^2$, a następnie $A^3$.
      * Sprawdza ślad macierzy $A^3$ (`graph.count_c3_matrix()`). Jeśli ślad \> 0, trójkąty istnieją.
      * Obliczana jest całkowita liczba trójkątów poprzez podzielenie śladu przez 6 (lub 3).
      * *Hybrydowe szukanie konkretnych cykli:* Ponieważ samo mnożenie macierzy mówi tylko "ile" jest trójkątów, a nie "gdzie", program używa metody `find_all_c3_matrix_assisted`. Wykorzystuje ona macierz $A^2$ do przyspieszenia wyszukiwania – sprawdza wspólnych sąsiadów tylko tam, gdzie mnożenie macierzy sugeruje istnienie ścieżek.

5.  **Demonstracja (opcjonalnie)**:
    Jeśli podano flagę `--demo`, funkcja `print_matrix_multiplication_demo` wypisuje na ekran całe macierze $A$, $A^2$ i $A^3$, pokazując użytkownikowi matematyczne podstawy algorytmu.

6.  **Zakończenie**:
    Program wyświetla podsumowanie czasu wykonania (jeśli wybrano `--benchmark`) i kończy pracę.