#!/usr/bin/env python3
"""
Task 5 - Minimum Spanning Tree (MST)

This program finds the minimum spanning tree of a weighted, undirected, connected graph
using Prim's or Kruskal's algorithm.
"""

from utils import (
    load_graph_from_file,
    print_graph_info,
    print_adjacency_matrix,
    print_mst_result,
    print_mst_adjacency_matrix,
    save_mst_visualization
)
import argparse
import sys

def main():
    parser = argparse.ArgumentParser(
        description="Find Minimum Spanning Tree (MST) of a weighted graph",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py graphs/weighted_1.txt --algorithm prim
  python main.py graphs/weighted_2.txt --algorithm kruskal --verbose
  python main.py graphs/weighted_1.txt --algorithm both --visualize
        """
    )
    
    parser.add_argument('filename', type=str, nargs='?',
                       help='Path to the weighted graph file')
    
    parser.add_argument('--algorithm', type=str, choices=['prim', 'kruskal', 'both'], default='both',
                       help='Algorithm to use: prim, kruskal, or both (default: both)')
    
    parser.add_argument('--verbose', '-v', action='store_true',
                       help='Show detailed information including adjacency matrix')
    
    parser.add_argument('--visualize', action='store_true',
                       help='Generate visualization of the MST')
    
    parser.add_argument('--start-vertex', type=int, default=0,
                       help='Starting vertex for Prim\'s algorithm (default: 0)')
    
    args = parser.parse_args()
    
    # Check if filename is provided
    if not args.filename:
        parser.print_help()
        print("\nError: filename is required")
        sys.exit(1)
    
    print("="*80)
    print("MINIMUM SPANNING TREE (MST)")
    print("="*80)
    print()
    
    # Load graph
    print(f"Loading graph from: {args.filename}")
    try:
        graph = load_graph_from_file(args.filename)
    except Exception as e:
        print(f"Error loading graph: {e}")
        sys.exit(1)
    
    # Check if graph is undirected
    if graph.directed:
        print("Error: MST algorithms require an undirected graph")
        sys.exit(1)
    
    print("Graph loaded successfully.\n")
    
    # Print graph info
    print_graph_info(graph)
    
    # Print adjacency matrix if verbose
    if args.verbose:
        print_adjacency_matrix(graph)
    
    # Run Prim's algorithm
    if args.algorithm in ['prim', 'both']:
        print("\n" + "="*80)
        print("PRIM'S ALGORITHM")
        print("="*80)
        print()
        
        try:
            mst_edges, total_weight = graph.prim_mst(args.start_vertex)
            print_mst_result(graph, mst_edges, total_weight, "Prim's Algorithm")
            
            if args.verbose:
                print_mst_adjacency_matrix(graph, mst_edges)
        except Exception as e:
            print(f"Error running Prim's algorithm: {e}")
            if args.algorithm == 'prim':
                sys.exit(1)
    
    # Run Kruskal's algorithm
    if args.algorithm in ['kruskal', 'both']:
        print("\n" + "="*80)
        print("KRUSKAL'S ALGORITHM")
        print("="*80)
        print()
        
        try:
            mst_edges, total_weight = graph.kruskal_mst()
            print_mst_result(graph, mst_edges, total_weight, "Kruskal's Algorithm")
            
            if args.verbose:
                print_mst_adjacency_matrix(graph, mst_edges)
        except Exception as e:
            print(f"Error running Kruskal's algorithm: {e}")
            if args.algorithm == 'kruskal':
                sys.exit(1)
    
    # Generate visualization if requested
    if args.visualize:
        print("\n" + "="*80)
        print("VISUALIZATION")
        print("="*80)
        print()
        
        # Use the last computed MST (or Prim's if both were run)
        if args.algorithm in ['prim', 'both']:
            mst_edges, _ = graph.prim_mst(args.start_vertex)
        else:
            mst_edges, _ = graph.kruskal_mst()
        
        save_mst_visualization(graph, mst_edges)
    
    print("="*80)
    print("Analysis complete.")
    print("="*80)

if __name__ == "__main__":
    main()
