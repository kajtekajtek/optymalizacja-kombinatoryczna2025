# Quick Usage Guide - C_3 Cycle Detection

## Quick Start

### 1. Create sample graphs
```bash
python main.py --create-samples
```

This creates a `graphs/` directory with 5 example files.

### 2. Basic usage
```bash
python main.py graphs/triangle.txt
```

This runs both naive and matrix multiplication methods on the input graph.

### 3. Run tests
```bash
python test_correctness.py
```

Verifies that all implementations work correctly.

## Common Commands

### Show only naive method
```bash
python main.py graphs/triangle.txt --method naive
```

### Show only matrix method
```bash
python main.py graphs/triangle.txt --method matrix
```

### Find and show all triangles
```bash
python main.py graphs/complete_k4.txt --show-all
```

### Show adjacency matrix
```bash
python main.py graphs/triangle.txt --verbose
```

### Demonstrate matrix multiplication
```bash
python main.py graphs/triangle.txt --demo
```

This shows:
- Matrix A (adjacency matrix)
- Matrix A² (paths of length 2)
- Matrix A³ (paths of length 3)
- Calculation of number of triangles

### Benchmark both methods
```bash
python main.py graphs/complete_k4.txt --benchmark
```

### Combine options
```bash
python main.py graphs/complete_k4.txt --verbose --show-all --demo --benchmark
```

## Sample Graphs

### triangle.txt
Simple triangle with 3 vertices (A, B, C).
- **Expected result:** 1 triangle

### multiple_triangles.txt
Graph with 5 vertices and multiple overlapping triangles.
- **Expected result:** 3 triangles

### no_triangles.txt
Tree structure with no cycles.
- **Expected result:** 0 triangles

### complete_k4.txt
Complete graph with 4 vertices (all vertices connected to each other).
- **Expected result:** 4 triangles

### directed_cycle.txt
Directed graph with one C_3 cycle.
- **Expected result:** 1 directed cycle

## Input File Format

```
<num_vertices> <directed|undirected>
[optional: vertex labels separated by spaces]
<vertex1> <vertex2>
<vertex1> <vertex2>
...
```

### Example

```
3 undirected
A B C
0 1
1 2
2 0
```

- Line 1: 3 vertices, undirected graph
- Line 2: Labels for vertices (optional)
- Lines 3-5: Edges (can use indices 0-2 or labels A, B, C)

## Understanding the Output

### Has C_3?
Both methods will report if the graph contains at least one C_3 cycle.

### Count
Matrix method can efficiently count total number of triangles using trace(A³).

### Finding cycles
Use `--show-all` to list all triangles found.

### Matrix demonstration
Use `--demo` to see the mathematical basis:
- **A²[i][j]** = number of paths of length 2 from i to j
- **A³[i][i]** = number of closed walks of length 3 starting at i
- **trace(A³) / 6** = number of triangles (undirected)
- **trace(A³) / 3** = number of cycles (directed)

## Implementation Details

### Naive Method
- **Complexity:** O(n³)
- **Method:** Check all triples of vertices (i, j, k) where i < j < k
- **Advantage:** Simple, no extra memory needed

### Matrix Method
- **Complexity:** O(n³) for matrix multiplication
- **Method:** Compute A³ and check diagonal elements
- **Advantage:** Can count triangles efficiently, potential for optimization with faster matrix multiplication algorithms

Both methods have the same asymptotic complexity, but the matrix method:
1. Provides count directly from trace(A³)
2. Can be optimized with advanced matrix multiplication (Strassen, etc.)
3. More elegant mathematical approach

## Scoring Criteria

✓ **Naive version** (1 point): Implemented in `has_c3_naive()`

✓ **Print at least one C_3 cycle** (1 point): Implemented in `find_one_c3_naive()` and `find_one_c3_matrix()`

✓ **Matrix multiplication version** (2 points): 
- Custom matrix multiplication: `multiply_matrices()`
- Detection: `has_c3_matrix()`
- Counting: `count_c3_matrix()`

**Total: 4 points**

## Tips

1. Use `--verbose` to see the adjacency matrix
2. Use `--demo` to understand the math behind matrix method
3. Use `--benchmark` to compare performance
4. Use `--show-all` to see all triangles, not just check existence
5. Test with different graph types: undirected, directed, with/without cycles

