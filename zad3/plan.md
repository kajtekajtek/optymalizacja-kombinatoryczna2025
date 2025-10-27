<!-- da2c7681-957f-4d28-8235-96992ed027ee b53e54d0-cd0e-4cf3-bdd2-395ef6c04c8c -->
# Critical Path Method Implementation Plan

## 1. Rename and Restructure Core Classes

Rename `FlowNetwork.py` to `TaskNetwork.py` and transform the `FlowNetwork` class into a `TaskNetwork` class suitable for CPM:

- Remove flow-related attributes (`self.flow`)
- Add task-related attributes: task list, duration mapping, earliest/latest times
- Keep graph structure (`self.capacity` can be reused as adjacency representation)

## 2. Create Task Data Structure

In `TaskNetwork.py`, add:

- `Task` class or dictionary to store: `task_id`, `duration`, `predecessors`, `earliest_start`, `earliest_finish`, `latest_start`, `latest_finish`, `slack`
- Method to load tasks from input file (first line: number of machines, subsequent lines: `task_id duration pred1 pred2 ...`)

## 3. Implement Network Construction

Add two methods in `TaskNetwork`:

- `build_AN_network()`: Activity-on-Node - tasks are nodes, edges represent precedence
- `build_AA_network()`: Activity-on-Arc - tasks are arcs, add dummy tasks if needed for proper precedence

## 4. Implement CPM Calculations

Add methods to `TaskNetwork`:

- `calculate_earliest_times()`: Forward pass through network
- `calculate_latest_times()`: Backward pass through network  
- `find_critical_path()`: Identify tasks where earliest == latest (slack = 0)
- `get_makespan()`: Return total project duration

## 5. Implement Machine Scheduling

Add `create_schedule()` method in `TaskNetwork`:

- Use earliest start times by default
- Assign tasks to machines using greedy approach (earliest available machine)
- Return schedule as dictionary: `{machine_id: [(task_id, start_time, end_time), ...]}`

## 6. Update Utilities

Modify `utils.py`:

- Rename/replace `load_flow_network_from_file()` with `load_task_network_from_file()` supporting new format
- Add `print_cpm_results()` to display earliest/latest times for each task
- Add `print_critical_path()` to display the critical path
- Add `print_schedule()` to display machine assignments
- Update or add visualization functions for task networks (optional: Gantt chart)

## 7. Update Main Program

Modify `main.py`:

- Update argument parser: add `--network-type` (choices: 'AA', 'AN')
- Replace Edmonds-Karp execution with CPM workflow:
- Load task network
- Build selected network type (AA or AN)
- Calculate earliest/latest times
- Find and display critical path
- Generate and display schedule
- Show makespan

## 8. Create Sample Input Files

Create new input files in `flow_networks/` (or rename directory to `task_networks/`):

- Format: First line = number of machines, subsequent lines = `task_id duration predecessor1 predecessor2 ...`
- Create at least 2 example files with different task dependencies

## Key Files to Modify

- `FlowNetwork.py` → `TaskNetwork.py` (complete restructure)
- `main.py` (update CLI and execution flow)
- `utils.py` (replace utility functions)
- Create new sample input files

### To-dos

- [ ] Rename FlowNetwork.py to TaskNetwork.py and restructure class for CPM
- [ ] Create Task data structure and file loading method
- [ ] Implement build_AN_network() and build_AA_network() methods
- [ ] Implement earliest/latest time calculations and critical path finding
- [ ] Implement create_schedule() method for machine assignment
- [ ] Update utils.py with CPM-specific printing and loading functions
- [ ] Modify main.py for CPM workflow and network type selection
- [ ] Create sample input files with new format