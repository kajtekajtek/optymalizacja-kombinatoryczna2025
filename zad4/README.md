# Zadanie 4 - Wyszukiwanie podgrafu C_3

Implementation of C_3 cycle (triangle) detection in graphs using adjacency matrix representation.

## Zadanie

W oparciu o reprezentację grafu prostego w postaci macierzy sąsiedztwa zaimplementować procedurę, która sprawdza, czy graf zawiera podgraf izomorficzny do cyklu C_3:
- Wersja naiwna - 1 punkt
- Wypisanie co najmniej jednego cyklu C3 o ile istnieje - 1 punkt
- Wersja w oparciu o mnożenie macierzy - 2 punkty

**Uwaga:** Mnożenie macierzy zaimplementowane samodzielnie (bez bibliotek numpy itp.).

## Opis rozwiązania

### C_3 Cycle (Triangle)
C_3 to cykl o 3 wierzchołkach, zwany również trójkątem. W grafie nieskierowanym to trzy wierzchołki połączone wzajemnie krawędziami. W grafie skierowanym to cykl kierowany przechodzący przez 3 wierzchołki.

### Zaimplementowane metody

#### 1. Metoda naiwna (`has_c3_naive()`)
**Złożoność:** O(n³)

Sprawdza wszystkie możliwe trójki wierzchołków (i, j, k) gdzie i < j < k i weryfikuje czy tworzą trójkąt.

Dla grafu nieskierowanego sprawdza istnienie krawędzi:
- (i, j)
- (j, k)
- (k, i)

#### 2. Znajdowanie cykli (`find_one_c3_naive()`, `find_all_c3_naive()`)
Dodatkowo do wykrywania istnienia, implementacja potrafi:
- Znaleźć jeden cykl C_3
- Znaleźć wszystkie cykle C_3 w grafie

#### 3. Metoda mnożenia macierzy (`has_c3_matrix()`)
**Złożoność:** O(n³)

Wykorzystuje matematyczną własność macierzy sąsiedztwa:
- A² zawiera liczbę ścieżek długości 2 między wierzchołkami
- A³ zawiera liczbę ścieżek długości 3 między wierzchołkami
- Elementy diagonalne A³ pokazują liczbę cykli długości 3 rozpoczynających się w danym wierzchołku

**Dla grafu nieskierowanego:**
- Każdy trójkąt jest liczony 6 razy (2 kierunki × 3 wierzchołki startowe)
- Liczba trójkątów = trace(A³) / 6

**Dla grafu skierowanego:**
- Każdy cykl jest liczony 3 razy (raz dla każdego wierzchołka startowego)
- Liczba cykli = trace(A³) / 3

**Implementacja własna mnożenia macierzy:**
```python
def multiply_matrices(A, B):
    n = len(A)
    m = len(B)
    p = len(B[0])
    result = [[0 for _ in range(p)] for _ in range(n)]
    
    for i in range(n):
        for j in range(p):
            for k in range(m):
                result[i][j] += A[i][k] * B[k][j]
    
    return result
```

## Format plików wejściowych

```
<liczba_wierzchołków> <directed|undirected>
[opcjonalnie: etykiety wierzchołków oddzielone spacjami]
<wierzchołek1> <wierzchołek2>
<wierzchołek1> <wierzchołek2>
...
```

### Przykład

```
3 undirected
A B C
0 1
1 2
2 0
```

Tworzy prosty trójkąt z trzech wierzchołków A, B, C.

## Użycie

### Podstawowe użycie

```bash
python main.py graphs/triangle.txt
```

### Tylko metoda naiwna

```bash
python main.py graphs/triangle.txt --method naive
```

### Tylko metoda mnożenia macierzy

```bash
python main.py graphs/triangle.txt --method matrix
```

### Pokaż wszystkie cykle C_3

```bash
python main.py graphs/multiple_triangles.txt --show-all
```

### Tryb szczegółowy (pokazuje macierz sąsiedztwa)

```bash
python main.py graphs/triangle.txt --verbose
```

### Demonstracja mnożenia macierzy

```bash
python main.py graphs/triangle.txt --demo
```

Pokazuje krok po kroku:
- Macierz A (macierz sąsiedztwa)
- Macierz A² (ścieżki długości 2)
- Macierz A³ (ścieżki długości 3)
- Obliczenie liczby trójkątów

### Benchmark

```bash
python main.py graphs/complete_k4.txt --benchmark
```

Porównuje wydajność obu metod.

### Tworzenie przykładowych plików

```bash
python main.py --create-samples
```

Tworzy katalog `graphs/` z przykładowymi grafami:
- `triangle.txt` - prosty trójkąt
- `multiple_triangles.txt` - graf z wieloma trójkątami
- `no_triangles.txt` - graf bez trójkątów (drzewo)
- `directed_cycle.txt` - graf skierowany z cyklem C_3
- `complete_k4.txt` - graf pełny K₄ (zawiera 4 trójkąty)

## Przykłady grafów

### 1. Prosty trójkąt (triangle.txt)

```
3 undirected
A B C
0 1
1 2
2 0
```

Graf:
```
  A --- B
   \   /
    \ /
     C
```

**Wynik:** 1 trójkąt: (A, B, C)

### 2. Graf z wieloma trójkątami (multiple_triangles.txt)

```
5 undirected
A B C D E
0 1
1 2
2 0
2 3
3 4
4 2
0 3
```

Graf:
```
  A --- B
  |\   /|
  | \ / |
  |  C  |
  | /|\ |
  |/ | \|
  D--+--E
```

**Wynik:** 3 trójkąty

### 3. Graf bez trójkątów (no_triangles.txt)

```
5 undirected
A B C D E
0 1
0 2
1 3
1 4
```

Graf (drzewo):
```
      A
     / \
    B   C
   / \
  D   E
```

**Wynik:** 0 trójkątów

### 4. Graf pełny K₄ (complete_k4.txt)

```
4 undirected
A B C D
0 1
0 2
0 3
1 2
1 3
2 3
```

Graf pełny K₄:
```
  A ---- B
  |\    /|
  | \  / |
  |  \/  |
  |  /\  |
  | /  \ |
  |/    \|
  D ---- C
```

**Wynik:** 4 trójkąty: (A,B,C), (A,B,D), (A,C,D), (B,C,D)

## Przykładowe wyjście

```
================================================================================
C_3 CYCLE (TRIANGLE) DETECTION IN GRAPHS
================================================================================

Loading graph from: graphs/complete_k4.txt
Graph loaded successfully.

Graph type: Undirected
Number of vertices: 4
Number of edges: 6

================================================================================
METHOD 1: NAIVE APPROACH
================================================================================
Checking all possible triples of vertices...

============================================================
C_3 Detection Result (Naive)
============================================================
✓ Graph CONTAINS at least one C_3 cycle (triangle)
============================================================

Found C_3 cycle:
============================================================
Triangle: A - B - C
Vertex indices: (0, 1, 2)

Edges in the triangle:
  A - B
  B - C
  C - A
============================================================

================================================================================
METHOD 2: MATRIX MULTIPLICATION APPROACH
================================================================================
Using A³ to detect cycles...

============================================================
C_3 Detection Result (Matrix Multiplication)
============================================================
✓ Graph CONTAINS at least one C_3 cycle (triangle)
============================================================

Number of C_3 cycles: 4

Found C_3 cycle:
============================================================
Triangle: A - B - C
Vertex indices: (0, 1, 2)

Edges in the triangle:
  A - B
  B - C
  C - A
============================================================

================================================================================
Analysis complete.
================================================================================
```

## Pliki projektu

- `Graph.py` - Klasa Graph z implementacją wszystkich metod wykrywania C_3
- `utils.py` - Funkcje pomocnicze (wczytywanie, wyświetlanie, tworzenie przykładów)
- `main.py` - Interfejs wiersza poleceń
- `graphs/` - Katalog z przykładowymi grafami
- `README.md` - Ten plik
- `polecenie.md` - Treść zadania

## Struktura klasy Graph

```python
class Graph:
    # Naive methods
    has_c3_naive() -> bool
    find_one_c3_naive() -> Optional[Tuple[int, int, int]]
    find_all_c3_naive() -> List[Tuple[int, int, int]]
    
    # Matrix methods
    multiply_matrices(A, B) -> List[List[int]]
    has_c3_matrix() -> bool
    count_c3_matrix() -> int
    find_one_c3_matrix() -> Optional[Tuple[int, int, int]]
    find_all_c3_matrix_assisted() -> List[Tuple[int, int, int]]
```

## Złożoność obliczeniowa

| Metoda | Złożoność czasowa | Złożoność pamięciowa |
|--------|-------------------|----------------------|
| Naive - wykrywanie | O(n³) | O(1) |
| Naive - znajdowanie wszystkich | O(n³) | O(k) gdzie k to liczba trójkątów |
| Matrix - wykrywanie | O(n³) | O(n²) |
| Matrix - liczenie | O(n³) | O(n²) |
| Matrix - znajdowanie | O(n³) | O(n² + k) |

**Uwaga:** Obie metody mają złożoność O(n³), ale metoda macierzowa może być optymalizowana przez wykorzystanie szybszych algorytmów mnożenia macierzy (np. Strassen O(n^2.807)).

## Wymagania

- Python 3.6+
- Brak zewnętrznych bibliotek (czyste Python)

## Autor

Implementacja wykonana w ramach kursu Optymalizacji Kombinatorycznej 2025.
