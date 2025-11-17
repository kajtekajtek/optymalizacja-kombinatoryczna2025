#!/usr/bin/env python3
"""
Test script to verify correctness of C_3 cycle detection implementations.
"""

from Graph import Graph

def test_simple_triangle():
    """Test with a simple triangle."""
    print("Test 1: Simple triangle (3 vertices)")
    g = Graph(3, directed=False)
    g.set_vertex_labels(['A', 'B', 'C'])
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    
    # Test naive approach
    has_c3_naive = g.has_c3_naive()
    one_c3_naive = g.find_one_c3_naive()
    all_c3_naive = g.find_all_c3_naive()
    
    # Test matrix approach
    has_c3_matrix = g.has_c3_matrix()
    count_c3_matrix = g.count_c3_matrix()
    one_c3_matrix = g.find_one_c3_matrix()
    all_c3_matrix = g.find_all_c3_matrix_assisted()
    
    print(f"  Naive: has_c3={has_c3_naive}, count={len(all_c3_naive)}")
    print(f"  Matrix: has_c3={has_c3_matrix}, count={count_c3_matrix}")
    
    assert has_c3_naive == True, "Naive should find triangle"
    assert has_c3_matrix == True, "Matrix should find triangle"
    assert len(all_c3_naive) == 1, "Should find exactly 1 triangle"
    assert count_c3_matrix == 1, "Should count exactly 1 triangle"
    assert len(all_c3_matrix) == 1, "Matrix-assisted should find exactly 1 triangle"
    
    print("  ✓ PASSED\n")

def test_no_triangles():
    """Test with a tree (no triangles)."""
    print("Test 2: Tree with no triangles (5 vertices)")
    g = Graph(5, directed=False)
    g.add_edge(0, 1)
    g.add_edge(0, 2)
    g.add_edge(1, 3)
    g.add_edge(1, 4)
    
    has_c3_naive = g.has_c3_naive()
    has_c3_matrix = g.has_c3_matrix()
    count_c3 = g.count_c3_matrix()
    all_c3_naive = g.find_all_c3_naive()
    
    print(f"  Naive: has_c3={has_c3_naive}, count={len(all_c3_naive)}")
    print(f"  Matrix: has_c3={has_c3_matrix}, count={count_c3}")
    
    assert has_c3_naive == False, "Should not find triangles in tree"
    assert has_c3_matrix == False, "Matrix should not find triangles in tree"
    assert len(all_c3_naive) == 0, "Should find 0 triangles"
    assert count_c3 == 0, "Should count 0 triangles"
    
    print("  ✓ PASSED\n")

def test_complete_k4():
    """Test with complete graph K4 (4 triangles)."""
    print("Test 3: Complete graph K4 (4 vertices, 4 triangles)")
    g = Graph(4, directed=False)
    # Add all edges
    for i in range(4):
        for j in range(i+1, 4):
            g.add_edge(i, j)
    
    has_c3_naive = g.has_c3_naive()
    has_c3_matrix = g.has_c3_matrix()
    count_c3 = g.count_c3_matrix()
    all_c3_naive = g.find_all_c3_naive()
    all_c3_matrix = g.find_all_c3_matrix_assisted()
    
    print(f"  Naive: has_c3={has_c3_naive}, count={len(all_c3_naive)}")
    print(f"  Matrix: has_c3={has_c3_matrix}, count={count_c3}")
    
    assert has_c3_naive == True, "Should find triangles in K4"
    assert has_c3_matrix == True, "Matrix should find triangles in K4"
    assert len(all_c3_naive) == 4, "K4 has exactly 4 triangles"
    assert count_c3 == 4, "Should count exactly 4 triangles"
    assert len(all_c3_matrix) == 4, "Matrix-assisted should find exactly 4 triangles"
    
    print("  ✓ PASSED\n")

def test_directed_cycle():
    """Test with directed graph."""
    print("Test 4: Directed graph with one C3 cycle")
    g = Graph(4, directed=True)
    g.set_vertex_labels(['A', 'B', 'C', 'D'])
    # Create cycle A->B->C->A
    g.add_edge(0, 1)  # A->B
    g.add_edge(1, 2)  # B->C
    g.add_edge(2, 0)  # C->A
    # Add extra edges that don't form cycles
    g.add_edge(1, 3)  # B->D
    g.add_edge(3, 2)  # D->C
    
    has_c3_naive = g.has_c3_naive()
    has_c3_matrix = g.has_c3_matrix()
    count_c3 = g.count_c3_matrix()
    one_c3_naive = g.find_one_c3_naive()
    
    print(f"  Naive: has_c3={has_c3_naive}")
    print(f"  Matrix: has_c3={has_c3_matrix}, count={count_c3}")
    
    assert has_c3_naive == True, "Should find cycle in directed graph"
    assert has_c3_matrix == True, "Matrix should find cycle in directed graph"
    assert count_c3 == 1, "Should count exactly 1 cycle"
    assert one_c3_naive is not None, "Should find the cycle"
    
    print("  ✓ PASSED\n")

def test_matrix_multiplication():
    """Test matrix multiplication implementation."""
    print("Test 5: Matrix multiplication correctness")
    g = Graph(3, directed=False)
    
    # Simple test: 3x3 identity matrix
    A = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
    B = [[2, 0, 0], [0, 3, 0], [0, 0, 4]]
    result = g.multiply_matrices(A, B)
    expected = [[2, 0, 0], [0, 3, 0], [0, 0, 4]]
    
    assert result == expected, f"Matrix multiplication failed: {result} != {expected}"
    
    # Test 2: General multiplication
    A = [[1, 2], [3, 4]]
    B = [[5, 6], [7, 8]]
    result = g.multiply_matrices(A, B)
    expected = [[19, 22], [43, 50]]
    
    assert result == expected, f"Matrix multiplication failed: {result} != {expected}"
    
    print("  Matrix multiplication: correct")
    print("  ✓ PASSED\n")

def test_multiple_triangles():
    """Test with graph containing multiple triangles."""
    print("Test 6: Graph with multiple overlapping triangles")
    g = Graph(5, directed=False)
    # Create triangles: (0,1,2), (0,2,3), (2,3,4)
    g.add_edge(0, 1)
    g.add_edge(1, 2)
    g.add_edge(2, 0)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    g.add_edge(4, 2)
    g.add_edge(0, 3)
    
    count_c3 = g.count_c3_matrix()
    all_c3 = g.find_all_c3_naive()
    
    print(f"  Matrix count: {count_c3}")
    print(f"  Naive count: {len(all_c3)}")
    
    assert count_c3 == 3, "Should count exactly 3 triangles"
    assert len(all_c3) == 3, "Should find exactly 3 triangles"
    
    print("  ✓ PASSED\n")

def main():
    print("="*60)
    print("C_3 CYCLE DETECTION - CORRECTNESS TESTS")
    print("="*60)
    print()
    
    try:
        test_simple_triangle()
        test_no_triangles()
        test_complete_k4()
        test_directed_cycle()
        test_matrix_multiplication()
        test_multiple_triangles()
        
        print("="*60)
        print("ALL TESTS PASSED! ✓")
        print("="*60)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        print("="*60)
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("="*60)
        return 1

if __name__ == "__main__":
    exit(main())

