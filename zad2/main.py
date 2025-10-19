from utils import (
    load_flow_network_from_file, 
    print_network_info, 
    print_capacity_matrix,
    print_flow_results,
    save_flow_network_visualization
)
import argparse

def main():
    parser = argparse.ArgumentParser(description="Maximum Flow - Edmonds-Karp Algorithm")
    parser.add_argument('filename', type=str, help='Path to the flow network file (format: u v capacity)')
    parser.add_argument('--verbose', '-v', action='store_true', help='Show detailed iteration information')
    parser.add_argument('--visualize', action='store_true', help='Generate visualization images')
    args = parser.parse_args()

    print("Loading flow network from file...")
    network = load_flow_network_from_file(args.filename)
    
    print_network_info(network)
    print_capacity_matrix(network)
    
    source = 0
    sink = network.n - 1
    
    print(f"\nRunning Edmonds-Karp algorithm...")
    print(f"Source: {source}, Sink: {sink}\n")
    
    max_flow, augmenting_paths = network.edmonds_karp(source, sink, verbose=args.verbose)
    
    print_flow_results(network, max_flow, augmenting_paths, source, sink)
    
    if args.visualize:
        print("Generating visualizations...")
        save_flow_network_visualization(network, 'flow_network_capacities.png', show_flow=False)
        save_flow_network_visualization(network, 'flow_network_final.png', show_flow=True)
        print()

if __name__ == "__main__":
    main()