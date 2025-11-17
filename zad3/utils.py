from TaskNetwork import TaskNetwork, Task
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, List, Tuple

def load_task_network_from_file(file_path: str) -> TaskNetwork:
    """
    Load task network from file.
    Format:
        First line: number of machines
        Subsequent lines: task_id duration predecessor1 predecessor2 ...
    """
    with open(file_path, 'r') as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]
    
    if not lines:
        raise ValueError("File is empty")
    
    # First line is number of machines
    num_machines = int(lines[0])
    
    network = TaskNetwork()
    network.num_machines = num_machines
    
    # Parse tasks
    for line in lines[1:]:
        parts = line.split()
        if len(parts) < 2:
            raise ValueError(f'Invalid line format: "{line}". Expected: task_id duration [predecessors...]')
        
        task_id = parts[0]
        duration = int(parts[1])
        predecessors = parts[2:] if len(parts) > 2 else []
        
        network.add_task(task_id, duration, predecessors)
    
    return network

def print_network_info(network: TaskNetwork):
    print(f"Number of tasks: {len(network.tasks)}")
    print(f"Number of machines: {network.num_machines}")
    print(f"Network type: {network.network_type if network.network_type else 'Not built yet'}")
    print()

def print_tasks(network: TaskNetwork):
    print("Tasks:")
    print(f"{'ID':<10} {'Duration':<10} {'Predecessors':<30}")
    print("=" * 50)
    for task_id, task in sorted(network.tasks.items()):
        pred_str = ', '.join(task.predecessors) if task.predecessors else 'None'
        print(f"{task_id:<10} {task.duration:<10} {pred_str:<30}")
    print()

def print_cpm_results(network: TaskNetwork):
    print(f"\n{'='*80}")
    print(f"CRITICAL PATH METHOD RESULTS")
    print(f"{'='*80}")
    print(f"Project makespan: {network.get_makespan()}")
    print(f"\n{'Task':<10} {'Duration':<10} {'ES':<8} {'EF':<8} {'LS':<8} {'LF':<8} {'Slack':<8} {'Critical':<10}")
    print("=" * 80)
    
    for task_id, task in sorted(network.tasks.items()):
        critical = "YES" if task.is_critical() else "NO"
        print(f"{task_id:<10} {task.duration:<10} {task.earliest_start:<8} {task.earliest_finish:<8} "
              f"{task.latest_start:<8} {task.latest_finish:<8} {task.slack:<8} {critical:<10}")
    print("=" * 80)

def print_critical_path(network: TaskNetwork):
    critical_path = network.find_critical_path()
    
    print(f"\n{'='*80}")
    print(f"CRITICAL PATH")
    print(f"{'='*80}")
    print(f"Critical path length: {network.get_makespan()}")
    print(f"Critical path: {' -> '.join(critical_path)}")
    print(f"Number of critical tasks: {len(critical_path)}")
    print("=" * 80)

def print_schedule(network: TaskNetwork, schedule: Dict[int, List[Tuple[str, int, int]]]):
    print(f"\n{'='*80}")
    print(f"MACHINE SCHEDULE (by earliest start times)")
    print(f"{'='*80}")
    
    for machine_id in sorted(schedule.keys()):
        tasks = schedule[machine_id]
        print(f"\nMachine {machine_id}:")
        if not tasks:
            print("  No tasks assigned")
        else:
            for task_id, start, end in tasks:
                duration = network.tasks[task_id].duration
                critical = "*" if network.tasks[task_id].is_critical() else " "
                print(f"  {critical} Task {task_id}: time [{start}, {end}] (duration: {duration})")
    
    print(f"\n{'='*80}")
    print(f"Total makespan: {network.get_makespan()}")
    print(f"{'='*80}\n")

def save_task_network_visualization(network: TaskNetwork, file_path: str):
    if network.network_type == 'AN':
        _save_AN_visualization(network, file_path)
    elif network.network_type == 'AA':
        _save_AA_visualization(network, file_path)
    else:
        print("Network not built yet. Cannot visualize.")

def _save_AN_visualization(network: TaskNetwork, file_path: str):
    G = nx.DiGraph()
    
    # Add nodes (tasks)
    for task_id, task in network.tasks.items():
        label = f"{task_id}\nD:{task.duration}\nES:{task.earliest_start}\nLS:{task.latest_start}"
        color = 'red' if task.is_critical() else 'lightblue'
        G.add_node(task_id, label=label, color=color)
    
    # Add edges (precedence)
    for task_id, successors in network.graph.items():
        for succ_id in successors:
            G.add_edge(task_id, succ_id)
    
    # Draw
    pos = nx.spring_layout(G, k=2, iterations=50)
    colors = [G.nodes[node]['color'] for node in G.nodes()]
    labels = {node: G.nodes[node]['label'] for node in G.nodes()}
    
    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, labels=labels, node_color=colors, node_size=3000, 
            font_size=8, font_weight='bold', arrows=True, arrowsize=20)
    
    plt.title(f"Activity-on-Node Network\nMakespan: {network.get_makespan()}", fontsize=14)
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to {file_path}")
    plt.close()

def _save_AA_visualization(network: TaskNetwork, file_path: str):
    G = nx.DiGraph()
    
    # Add nodes (events)
    for node in network.graph.keys():
        G.add_node(node)
    
    # Add edges (tasks and dummy tasks)
    edge_labels = {}
    edge_colors = []
    
    for start_node, end_nodes in network.graph.items():
        for end_node in end_nodes:
            arc = (start_node, end_node)
            task_id = network.arc_to_task.get(arc)
            
            if task_id and task_id not in network.dummy_tasks:
                task = network.tasks[task_id]
                label = f"{task_id}({task.duration})"
                edge_labels[arc] = label
                color = 'red' if task.is_critical() else 'black'
                edge_colors.append(color)
                G.add_edge(start_node, end_node, weight=task.duration)
            else:
                # Dummy arc
                edge_labels[arc] = "dummy"
                edge_colors.append('gray')
                G.add_edge(start_node, end_node, weight=0, style='dashed')
    
    # Draw
    pos = nx.spring_layout(G, k=3, iterations=50)
    
    plt.figure(figsize=(14, 10))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', 
            node_size=1500, font_size=10, font_weight='bold',
            edge_color=edge_colors, arrows=True, arrowsize=20, width=2)
    
    nx.draw_networkx_edge_labels(G, pos, edge_labels, font_size=8)
    
    plt.title(f"Activity-on-Arc Network\nMakespan: {network.get_makespan()}", fontsize=14)
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"Visualization saved to {file_path}")
    plt.close()

def save_gantt_chart(network: TaskNetwork, schedule: Dict[int, List[Tuple[str, int, int]]], file_path: str):
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Prepare data
    colors = []
    for task in network.tasks.values():
        colors.append('red' if task.is_critical() else 'skyblue')
    
    task_to_color = {task_id: ('red' if task.is_critical() else 'skyblue') 
                     for task_id, task in network.tasks.items()}
    
    # Plot bars for each machine
    y_pos = 0
    yticks = []
    ylabels = []
    
    for machine_id in sorted(schedule.keys()):
        tasks = schedule[machine_id]
        yticks.append(y_pos)
        ylabels.append(f"Machine {machine_id}")
        
        for task_id, start, end in tasks:
            duration = end - start
            color = task_to_color[task_id]
            ax.barh(y_pos, duration, left=start, height=0.6, 
                   color=color, edgecolor='black', linewidth=1)
            ax.text(start + duration/2, y_pos, task_id, 
                   ha='center', va='center', fontsize=9, fontweight='bold')
        
        y_pos += 1
    
    ax.set_yticks(yticks)
    ax.set_yticklabels(ylabels)
    ax.set_xlabel('Time', fontsize=12)
    ax.set_title(f'Gantt Chart - Machine Schedule\nMakespan: {network.get_makespan()}', fontsize=14)
    ax.grid(axis='x', alpha=0.3)
    
    # Add legend
    from matplotlib.patches import Patch
    legend_elements = [
        Patch(facecolor='red', edgecolor='black', label='Critical tasks'),
        Patch(facecolor='skyblue', edgecolor='black', label='Non-critical tasks')
    ]
    ax.legend(handles=legend_elements, loc='upper right')
    
    plt.tight_layout()
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    print(f"Gantt chart saved to {file_path}")
    plt.close()
