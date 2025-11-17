from utils import (
    load_task_network_from_file,
    print_network_info,
    print_tasks,
    print_cpm_results,
    print_critical_path,
    print_schedule,
    save_task_network_visualization,
    save_gantt_chart
)
import argparse

def main():
    parser = argparse.ArgumentParser(description="Critical Path Method - Task Scheduling")
    parser.add_argument('filename', type=str, 
                       help='Path to the task file (format: first line = num_machines, then: task_id duration pred1 pred2 ...)')
    parser.add_argument('--network-type', type=str, choices=['AA', 'AN'], default='AN',
                       help='Type of network to build: AA (Activity-on-Arc) or AN (Activity-on-Node)')
    parser.add_argument('--verbose', '-v', action='store_true', 
                       help='Show detailed information')
    parser.add_argument('--visualize', action='store_true', 
                       help='Generate visualization images (network graph and Gantt chart)')
    args = parser.parse_args()

    print("="*80)
    print("CRITICAL PATH METHOD - TASK SCHEDULING")
    print("="*80)
    
    print("\nLoading task network from file...")
    network = load_task_network_from_file(args.filename)
    
    print_network_info(network)
    
    if args.verbose:
        print_tasks(network)
    
    print(f"Building {args.network_type} network...")
    if args.network_type == 'AN':
        network.build_AN_network()
    else:
        network.build_AA_network()
    print(f"{args.network_type} network built successfully.\n")
    
    print("Calculating earliest and latest times...")
    network.calculate_earliest_times()
    network.calculate_latest_times()
    print("Calculations complete.\n")
    
    # Print results
    print_cpm_results(network)
    print_critical_path(network)
    
    print("\nGenerating machine schedule...")
    schedule = network.create_schedule()
    print_schedule(network, schedule)
    
    if args.visualize:
        print("Generating visualizations...")
        network_file = f'task_network_{args.network_type.lower()}.png'
        save_task_network_visualization(network, network_file)
        save_gantt_chart(network, schedule, 'gantt_chart.png')
        print()

if __name__ == "__main__":
    main()
