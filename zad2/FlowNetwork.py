from collections import deque
from typing import Optional, Tuple, List

class FlowNetwork:
    def __init__(self, n: int):
        self.n = n
        self.capacity = [[0] * n for _ in range(n)]
        self.flow = [[0] * n for _ in range(n)]
    
    def add_edge(self, u: int, v: int, capacity: int):
        self.capacity[u][v] = capacity
    
    def get_residual_capacity(self, u: int, v: int) -> int:
        return self.capacity[u][v] - self.flow[u][v]
    
    def bfs_find_augmenting_path(self, source: int, sink: int) -> Optional[Tuple[dict, int]]:
        """
        Find augmenting path from source to sink using BFS with vertex labeling.
        Returns tuple of (labels, bottleneck_flow) or None if no path exists.
        
        Label format: label[v] = (parent, edge_capacity, min_flow_to_v)
        """
        # initialize labels: label[v] = (parent, edge_capacity, min_flow_to_v)
        labels = {source: (None, float('inf'), float('inf'))}
        visited = {source}
        queue = deque([source])
        
        while queue:
            u = queue.popleft()
            
            # if we reached the sink, we found an augmenting path
            if u == sink:
                break
            
            # check all neighbors
            for v in range(self.n):
                residual_cap = self.get_residual_capacity(u, v)
                
                # if there's residual capacity and v is not visited
                if residual_cap > 0 and v not in visited:
                    # calculate min flow to v through this path
                    min_flow = min(labels[u][2], residual_cap)
                    labels[v] = (u, residual_cap, min_flow)
                    visited.add(v)
                    queue.append(v)
        
        # if sink was reached, return labels and bottleneck flow
        if sink in labels:
            return labels, labels[sink][2]
        return None
    
    def augment_flow(self, source: int, sink: int, labels: dict, bottleneck: int):
        """Augment flow along the path from source to sink."""
        # reconstruct path from sink to source
        path = []
        v = sink
        while v != source:
            parent = labels[v][0]
            path.append((parent, v))
            v = parent
        
        # augment flow along the path
        for u, v in path:
            self.flow[u][v] += bottleneck
            self.flow[v][u] -= bottleneck
        
        return path
    
    def edmonds_karp(self, source: int, sink: int, verbose: bool = False) -> Tuple[int, List[Tuple[List, int]]]:
        """
        Find maximum flow from source to sink using Edmonds-Karp algorithm.
        Returns tuple of (max_flow_value, list of augmenting paths with their flows).
        """
        max_flow = 0
        augmenting_paths = []
        iteration = 0
        
        while True:
            # find augmenting path using BFS
            result = self.bfs_find_augmenting_path(source, sink)
            
            if result is None:
                # no more augmenting paths
                break
            
            labels, bottleneck = result
            iteration += 1
            
            # augment flow
            path = self.augment_flow(source, sink, labels, bottleneck)
            augmenting_paths.append((path, bottleneck))
            max_flow += bottleneck
            
            if verbose:
                print(f"\nIteration {iteration}:")
                print(f"  Augmenting path: {' -> '.join(str(u) for u, _ in reversed(path))} -> {sink}")
                print(f"  Bottleneck capacity: {bottleneck}")
                print(f"  Current flow: {max_flow}")
        
        return max_flow, augmenting_paths
    
    def get_flow_matrix(self) -> List[List[int]]:
        return self.flow
    
    def get_capacity_matrix(self) -> List[List[int]]:
        return self.capacity
    
    def get_number_of_nodes(self) -> int:
        return self.n