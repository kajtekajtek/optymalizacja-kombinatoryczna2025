from collections import deque
from typing import List, Dict, Tuple, Optional

class Task:
    def __init__(self, task_id: str, duration: int, predecessors: List[str] = None):
        self.task_id = task_id
        self.duration = duration
        self.predecessors = predecessors if predecessors else []
        self.earliest_start = 0
        self.earliest_finish = 0
        self.latest_start = 0
        self.latest_finish = 0
        self.slack = 0
    
    def calculate_slack(self):
        self.slack = self.latest_start - self.earliest_start
    
    def is_critical(self) -> bool:
        return self.slack == 0
    
    def __repr__(self):
        return f"Task({self.task_id}, duration={self.duration}, ES={self.earliest_start}, EF={self.earliest_finish}, LS={self.latest_start}, LF={self.latest_finish}, slack={self.slack})"

class TaskNetwork:
    
    def __init__(self):
        self.tasks: Dict[str, Task] = {}
        self.num_machines = 0
        self.network_type = None  # 'AA' or 'AN'
        self.graph = {}  # adjacency list representation
        self.makespan = 0
        
        # For AA network
        self.dummy_tasks = []  # List of dummy task IDs
        self.arc_to_task = {}  # Maps (u, v) arc to task_id
    
    def add_task(self, task_id: str, duration: int, predecessors: List[str] = None):
        task = Task(task_id, duration, predecessors)
        self.tasks[task_id] = task
    
    def build_AN_network(self):
        self.network_type = 'AN'
        self.graph = {task_id: [] for task_id in self.tasks}
        
        # Add edges based on predecessors
        for task_id, task in self.tasks.items():
            for pred_id in task.predecessors:
                if pred_id in self.graph:
                    self.graph[pred_id].append(task_id)
                else:
                    self.graph[pred_id] = [task_id]
        
        # Ensure all tasks are in graph
        for task_id in self.tasks:
            if task_id not in self.graph:
                self.graph[task_id] = []
    
    def build_AA_network(self):
        self.network_type = 'AA'
        self.graph = {}
        self.arc_to_task = {}
        self.dummy_tasks = []
        
        # Create nodes: start node, end node, and intermediate event nodes
        nodes = set(['START', 'END'])
        node_counter = 0
        task_start_nodes = {}
        task_end_nodes = {}
        
        # For tasks without predecessors, they start from START
        # For tasks without successors, they end at END
        
        # Create a node for each unique event (start/end of tasks)
        for task_id, task in self.tasks.items():
            if not task.predecessors:
                task_start_nodes[task_id] = 'START'
            else:
                # Create a node representing the event when all predecessors are done
                node_id = f"N{node_counter}"
                node_counter += 1
                nodes.add(node_id)
                task_start_nodes[task_id] = node_id
            
            # Check if this task has successors
            has_successors = any(task_id in t.predecessors for t in self.tasks.values())
            if not has_successors:
                task_end_nodes[task_id] = 'END'
            else:
                node_id = f"N{node_counter}"
                node_counter += 1
                nodes.add(node_id)
                task_end_nodes[task_id] = node_id
        
        # Initialize graph
        self.graph = {node: [] for node in nodes}
        
        # Add arcs for actual tasks
        for task_id, task in self.tasks.items():
            start_node = task_start_nodes[task_id]
            end_node = task_end_nodes[task_id]
            self.graph[start_node].append(end_node)
            self.arc_to_task[(start_node, end_node)] = task_id
        
        # Add dummy arcs for dependencies
        for task_id, task in self.tasks.items():
            for pred_id in task.predecessors:
                pred_end = task_end_nodes[pred_id]
                task_start = task_start_nodes[task_id]
                
                # Add dummy arc if not already connected
                if pred_end != task_start:
                    if task_start not in self.graph[pred_end]:
                        self.graph[pred_end].append(task_start)
                        dummy_id = f"DUMMY_{pred_end}_{task_start}"
                        self.arc_to_task[(pred_end, task_start)] = dummy_id
                        self.dummy_tasks.append(dummy_id)
    
    def calculate_earliest_times(self):
        if self.network_type == 'AN':
            self._calculate_earliest_times_AN()
        else:  # AA
            self._calculate_earliest_times_AA()
    
    def _calculate_earliest_times_AN(self):
        # Topological sort
        in_degree = {task_id: len(task.predecessors) for task_id, task in self.tasks.items()}
        queue = deque([task_id for task_id, task in self.tasks.items() if len(task.predecessors) == 0])
        
        while queue:
            current_id = queue.popleft()
            current_task = self.tasks[current_id]
            
            # Calculate earliest start: max of all predecessor earliest finishes
            if current_task.predecessors:
                current_task.earliest_start = max(
                    self.tasks[pred_id].earliest_finish for pred_id in current_task.predecessors
                )
            else:
                current_task.earliest_start = 0
            
            current_task.earliest_finish = current_task.earliest_start + current_task.duration
            
            # Process successors
            for successor_id in self.graph.get(current_id, []):
                in_degree[successor_id] -= 1
                if in_degree[successor_id] == 0:
                    queue.append(successor_id)
        
        # Calculate makespan
        self.makespan = max(task.earliest_finish for task in self.tasks.values())
    
    def _calculate_earliest_times_AA(self):
        # Calculate earliest event times for each node
        event_times = {'START': 0}
        
        # Topological sort on nodes
        in_degree = {node: 0 for node in self.graph}
        for node in self.graph:
            for successor in self.graph[node]:
                in_degree[successor] = in_degree.get(successor, 0) + 1
        
        queue = deque([node for node in self.graph if in_degree[node] == 0])
        
        while queue:
            current_node = queue.popleft()
            
            for successor_node in self.graph[current_node]:
                # Get duration of arc
                arc = (current_node, successor_node)
                task_id = self.arc_to_task.get(arc)
                
                if task_id and task_id not in self.dummy_tasks:
                    duration = self.tasks[task_id].duration
                else:
                    duration = 0  # Dummy arc
                
                # Update earliest time for successor
                new_time = event_times[current_node] + duration
                event_times[successor_node] = max(event_times.get(successor_node, 0), new_time)
                
                in_degree[successor_node] -= 1
                if in_degree[successor_node] == 0:
                    queue.append(successor_node)
        
        # Assign earliest times to tasks
        for (start_node, end_node), task_id in self.arc_to_task.items():
            if task_id not in self.dummy_tasks:
                task = self.tasks[task_id]
                task.earliest_start = event_times[start_node]
                task.earliest_finish = event_times[end_node]
        
        self.makespan = event_times.get('END', 0)
    
    def calculate_latest_times(self):
        if self.network_type == 'AN':
            self._calculate_latest_times_AN()
        else:  # AA
            self._calculate_latest_times_AA()
        
        # Calculate slack for all tasks
        for task in self.tasks.values():
            task.calculate_slack()
    
    def _calculate_latest_times_AN(self):
        # Initialize all latest finish times to makespan
        for task in self.tasks.values():
            task.latest_finish = self.makespan
        
        # Build reverse graph
        reverse_graph = {task_id: [] for task_id in self.tasks}
        for task_id, successors in self.graph.items():
            for succ_id in successors:
                reverse_graph[succ_id].append(task_id)
        
        # Topological sort in reverse (start from tasks with no successors)
        out_degree = {task_id: len(successors) for task_id, successors in self.graph.items()}
        queue = deque([task_id for task_id in self.tasks if out_degree.get(task_id, 0) == 0])
        
        while queue:
            current_id = queue.popleft()
            current_task = self.tasks[current_id]
            
            # Calculate latest finish: min of all successor latest starts
            successors = self.graph.get(current_id, [])
            if successors:
                current_task.latest_finish = min(
                    self.tasks[succ_id].latest_start for succ_id in successors
                )
            else:
                current_task.latest_finish = self.makespan
            
            current_task.latest_start = current_task.latest_finish - current_task.duration
            
            # Process predecessors
            for pred_id in reverse_graph.get(current_id, []):
                out_degree[pred_id] -= 1
                if out_degree[pred_id] == 0:
                    queue.append(pred_id)
    
    def _calculate_latest_times_AA(self):
        # Calculate latest event times for each node (backward from END)
        event_times = {'END': self.makespan}
        
        # Build reverse graph
        reverse_graph = {node: [] for node in self.graph}
        for node in self.graph:
            for successor in self.graph[node]:
                reverse_graph[successor].append(node)
        
        # Reverse topological sort
        out_degree = {node: len(self.graph[node]) for node in self.graph}
        queue = deque([node for node in self.graph if out_degree[node] == 0])
        
        while queue:
            current_node = queue.popleft()
            
            for predecessor_node in reverse_graph[current_node]:
                # Get duration of arc
                arc = (predecessor_node, current_node)
                task_id = self.arc_to_task.get(arc)
                
                if task_id and task_id not in self.dummy_tasks:
                    duration = self.tasks[task_id].duration
                else:
                    duration = 0  # Dummy arc
                
                # Update latest time for predecessor
                new_time = event_times[current_node] - duration
                if predecessor_node in event_times:
                    event_times[predecessor_node] = min(event_times[predecessor_node], new_time)
                else:
                    event_times[predecessor_node] = new_time
                
                out_degree[predecessor_node] -= 1
                if out_degree[predecessor_node] == 0:
                    queue.append(predecessor_node)
        
        # Assign latest times to tasks
        for (start_node, end_node), task_id in self.arc_to_task.items():
            if task_id not in self.dummy_tasks:
                task = self.tasks[task_id]
                task.latest_start = event_times[start_node]
                task.latest_finish = event_times[end_node]
    
    def find_critical_path(self) -> List[str]:
        critical_tasks = [task_id for task_id, task in self.tasks.items() if task.is_critical()]
        
        # Order critical tasks by earliest start time
        critical_tasks.sort(key=lambda tid: self.tasks[tid].earliest_start)
        
        return critical_tasks
    
    def get_makespan(self) -> int:
        return self.makespan
    
    def create_schedule(self) -> Dict[int, List[Tuple[str, int, int]]]:
        """
        Create a machine schedule using earliest start times.
        Returns: {machine_id: [(task_id, start_time, end_time), ...]}
        """
        schedule = {i: [] for i in range(self.num_machines)}
        machine_available_time = [0] * self.num_machines
        
        # Sort tasks by earliest start time
        sorted_tasks = sorted(self.tasks.values(), key=lambda t: (t.earliest_start, t.task_id))
        
        for task in sorted_tasks:
            # Find the machine that becomes available earliest and can start the task
            best_machine = 0
            best_start_time = max(task.earliest_start, machine_available_time[0])
            
            for machine_id in range(1, self.num_machines):
                candidate_start = max(task.earliest_start, machine_available_time[machine_id])
                if candidate_start < best_start_time:
                    best_machine = machine_id
                    best_start_time = candidate_start
            
            # Assign task to best machine
            start_time = best_start_time
            end_time = start_time + task.duration
            schedule[best_machine].append((task.task_id, start_time, end_time))
            machine_available_time[best_machine] = end_time
        
        return schedule

