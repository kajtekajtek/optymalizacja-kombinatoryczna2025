# Critical Path Method (CPM) - Task Scheduling

This project implements the Critical Path Method for project scheduling and analysis.

## Features

- **Network Construction**: Supports both Activity-on-Node (AN) and Activity-on-Arc (AA) networks
- **CPM Analysis**: Calculates earliest/latest start and finish times for all tasks
- **Critical Path**: Identifies the critical path and critical tasks
- **Machine Scheduling**: Assigns tasks to machines based on earliest start times
- **Visualization**: Generates network diagrams and Gantt charts

## Input Format

Input files should follow this format:
```
<number_of_machines>
<task_id> <duration> [predecessor1] [predecessor2] ...
<task_id> <duration> [predecessor1] [predecessor2] ...
...
```

### Example Input File

```
3
A 3
B 4 A
C 2 A
D 5 B C
E 3 D
F 2 C
G 4 E F
```

This defines:
- 3 machines available
- 7 tasks (A through G)
- Task A has duration 3 and no predecessors
- Task B has duration 4 and depends on A
- Task D depends on both B and C
- etc.

## Usage

Basic usage:
```bash
python main.py <task_file> --network-type <AN|AA>
```

### Options

- `filename`: Path to the task file (required)
- `--network-type <AN|AA>`: Type of network to build (default: AN)
  - `AN`: Activity-on-Node network (tasks are nodes)
  - `AA`: Activity-on-Arc network (tasks are arcs)
- `--verbose`, `-v`: Show detailed task information
- `--visualize`: Generate visualization images (network graph and Gantt chart)

### Examples

1. Run CPM with Activity-on-Node network:
```bash
python main.py task_networks/tasks_1.txt --network-type AN
```

2. Run with Activity-on-Arc network and verbose output:
```bash
python main.py task_networks/tasks_1.txt --network-type AA --verbose
```

3. Generate visualizations:
```bash
python main.py task_networks/tasks_1.txt --network-type AN --visualize
```

## Output

The program provides:

### 1. CPM Results Table
Shows for each task:
- Duration
- Earliest Start (ES) and Finish (EF) times
- Latest Start (LS) and Finish (LF) times
- Slack time (LS - ES)
- Whether task is critical (slack = 0)

### 2. Critical Path
Lists the sequence of critical tasks that determine the minimum project duration.

### 3. Machine Schedule
Shows task assignments to machines with start and end times. Critical tasks are marked with an asterisk (*).

### 4. Project Makespan
The total project duration (length of the critical path).

### 5. Visualizations (optional)
When `--visualize` is used:
- `task_network_an.png` or `task_network_aa.png`: Network diagram
- `gantt_chart.png`: Gantt chart showing task scheduling on machines

## Example Output

```
================================================================================
CRITICAL PATH METHOD RESULTS
================================================================================
Project makespan: 19

Task       Duration   ES       EF       LS       LF       Slack    Critical  
================================================================================
A          3          0        3        0        3        0        YES       
B          4          3        7        3        7        0        YES       
C          2          3        5        5        7        2        NO        
D          5          7        12       7        12       0        YES       
E          3          12       15       12       15       0        YES       
F          2          5        7        13       15       8        NO        
G          4          15       19       15       19       0        YES       
================================================================================

================================================================================
CRITICAL PATH
================================================================================
Critical path length: 19
Critical path: A -> B -> D -> E -> G
Number of critical tasks: 5
================================================================================

================================================================================
MACHINE SCHEDULE (by earliest start times)
================================================================================

Machine 0:
  * Task A: time [0, 3] (duration: 3)
  * Task B: time [3, 7] (duration: 4)
  * Task D: time [7, 12] (duration: 5)
  * Task E: time [12, 15] (duration: 3)
  * Task G: time [15, 19] (duration: 4)

Machine 1:
    Task C: time [3, 5] (duration: 2)
    Task F: time [5, 7] (duration: 2)

Machine 2:
  No tasks assigned

================================================================================
Total makespan: 19
================================================================================
```

## Implementation Details

### Classes

- **Task**: Represents a single task with duration, predecessors, and timing information
- **TaskNetwork**: Main class for CPM analysis
  - Manages tasks and network structure
  - Builds AN or AA networks
  - Performs forward/backward pass calculations
  - Generates machine schedules

### Key Methods

- `build_AN_network()`: Constructs Activity-on-Node network
- `build_AA_network()`: Constructs Activity-on-Arc network
- `calculate_earliest_times()`: Forward pass (topological sort)
- `calculate_latest_times()`: Backward pass (reverse topological sort)
- `find_critical_path()`: Identifies critical tasks
- `create_schedule()`: Assigns tasks to machines using greedy algorithm

## Files

- `main.py`: Command-line interface
- `TaskNetwork.py`: Core CPM implementation
- `utils.py`: Utility functions for I/O and visualization
- `task_networks/`: Directory containing example task files
- `README.md`: This file

## Requirements

- Python 3.6+
- networkx (for visualization)
- matplotlib (for visualization)

## Notes

- The Activity-on-Node (AN) network is the recommended and more commonly used representation
- The machine scheduling uses a greedy approach based on earliest start times
- Critical tasks (slack = 0) are marked with an asterisk (*) in the schedule
- Visualization files are saved in the current directory

