#!/usr/bin/env python3
"""
Task 4 - C_3 Cycle Detection in Graphs

This program detects triangles (C_3 cycles) in graphs represented as adjacency matrices.

Implements three approaches:
1. Naive approach - checks all triples of vertices (O(n^3))
2. Find and print at least one C_3 cycle
3. Matrix multiplication approach - uses A^3 to detect cycles
"""

from utils import (
    load_graph_from_file,
    print_graph_info,
    print_adjacency_matrix,
    print_c3_result,
    print_c3_cycles,
    print_single_c3_cycle,
    print_matrix_multiplication_demo,
    create_sample_graphs
)
import argparse
import sys
import time

def main():
    parser = argparse.ArgumentParser(
        description="Detect C_3 cycles (triangles) in graphs using adjacency matrix representation",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py graphs/triangle.txt --method naive
  python main.py graphs/multiple_triangles.txt --method matrix --show-all
  python main.py graphs/complete_k4.txt --verbose --demo
  python main.py --create-samples
        """
    )
    
    parser.add_argument('filename', type=str, nargs='?',
                       help='Path to the graph file')
    
    parser.add_argument('--method', type=str, choices=['naive', 'matrix', 'both'], default='both',
                       help='Method to use for detection: naive, matrix, or both (default: both)')
    
    parser.add_argument('--show-all', action='store_true',
                       help='Show all C_3 cycles found (not just existence)')
    
    parser.add_argument('--demo', action='store_true',
                       help='Show detailed matrix multiplication demonstration')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed information including adjacency matrix')
    
    parser.add_argument('--benchmark', '-b', action='store_true',
                       help='Benchmark and compare different methods')
    
    parser.add_argument('--create-samples', action='store_true',
                       help='Create sample graph files in graphs/ directory')
    
    args = parser.parse_args()
    
    # Handle create samples option
    if args.create_samples:
        create_sample_graphs()
        return
    
    # Check if filename is provided
    if not args.filename:
        parser.print_help()
        print("\nError: filename is required (unless using --create-samples)")
        sys.exit(1)
    
    print("="*80)
    print("C_3 CYCLE (TRIANGLE) DETECTION IN GRAPHS")
    print("="*80)
    print()
    
    # Load graph
    print(f"Loading graph from: {args.filename}")
    try:
        graph = load_graph_from_file(args.filename)
    except Exception as e:
        print(f"Error loading graph: {e}")
        sys.exit(1)
    
    print("Graph loaded successfully.\n")
    
    # Print graph info
    print_graph_info(graph)
    
    # Print adjacency matrix if verbose
    if args.verbose:
        print_adjacency_matrix(graph)
    
    # Method 1: Naive approach
    if args.method in ['naive', 'both']:
        print("\n" + "="*80)
        print("METHOD 1: NAIVE APPROACH")
        print("="*80)
        print("Checking all possible triples of vertices...")
        print()
        
        start_time = time.time()
        
        if args.show_all:
            triangles = graph.find_all_c3_naive()
            elapsed = time.time() - start_time
            
            has_c3 = len(triangles) > 0
            print_c3_result(graph, has_c3, "Naive - All cycles")
            print_c3_cycles(graph, triangles)
        else:
            # Just find one
            triangle = graph.find_one_c3_naive()
            elapsed = time.time() - start_time
            
            has_c3 = triangle is not None
            print_c3_result(graph, has_c3, "Naive")
            
            if triangle:
                print_single_c3_cycle(graph, triangle)
        
        if args.benchmark:
            print(f"Time elapsed: {elapsed*1000:.4f} ms\n")
    
    # Method 2: Matrix multiplication approach
    if args.method in ['matrix', 'both']:
        print("\n" + "="*80)
        print("METHOD 2: MATRIX MULTIPLICATION APPROACH")
        print("="*80)
        print("Using A³ to detect cycles...")
        print()
        
        start_time = time.time()
        
        # Check if C_3 exists
        has_c3 = graph.has_c3_matrix()
        count = graph.count_c3_matrix()
        
        check_time = time.time() - start_time
        
        print_c3_result(graph, has_c3, "Matrix Multiplication")
        
        if has_c3:
            print(f"Number of C_3 cycles: {count}\n")
            
            # Find one or all cycles
            if args.show_all:
                start_find = time.time()
                triangles = graph.find_all_c3_matrix_assisted()
                find_time = time.time() - start_find
                print_c3_cycles(graph, triangles)
                
                if args.benchmark:
                    print(f"Time for detection: {check_time*1000:.4f} ms")
                    print(f"Time for finding all cycles: {find_time*1000:.4f} ms")
                    print(f"Total time: {(check_time + find_time)*1000:.4f} ms\n")
            else:
                start_find = time.time()
                triangle = graph.find_one_c3_matrix()
                find_time = time.time() - start_find
                
                if triangle:
                    print_single_c3_cycle(graph, triangle)
                
                if args.benchmark:
                    print(f"Time for detection: {check_time*1000:.4f} ms")
                    print(f"Time for finding one cycle: {find_time*1000:.4f} ms")
                    print(f"Total time: {(check_time + find_time)*1000:.4f} ms\n")
        else:
            if args.benchmark:
                print(f"Time elapsed: {check_time*1000:.4f} ms\n")
    
    # Show matrix multiplication demo if requested
    if args.demo:
        print_matrix_multiplication_demo(graph)
    
    print("="*80)
    print("Analysis complete.")
    print("="*80)

if __name__ == "__main__":
    main()
