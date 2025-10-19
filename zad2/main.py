from utils import load_graph_from_file, print_statistics, print_matrix, save_graph_visualization_to_file
import argparse

def main():
    parser = argparse.ArgumentParser(description="Graph processing program")
    parser.add_argument('filename', type=str, help='Path to the graph file')
    args = parser.parse_args()

    graph = load_graph_from_file(args.filename)
    print_statistics(graph)
    print_matrix(graph)
    save_graph_visualization_to_file(graph, 'graph_visualization.png')

if __name__ == "__main__":
    main()