# Edmonds-Karp Maximum Flow Implementation

## Overview

Implement the Edmonds-Karp algorithm with vertex labeling for finding maximum flow in a flow network. The algorithm uses BFS to find augmenting paths from source (node 0) to sink (node n-1).

## Key Changes

### 1. Modify `Graph.py`

Transform the Graph class into a FlowNetwork class:

- Replace binary adjacency matrix with capacity matrix (storing edge capacities)
- Add residual graph tracking
- Remove methods irrelevant to flow networks (degree counting, etc.)
- Keep only: `n`, `directed=True`, capacity matrix operations

### 2. Implement Edmonds-Karp in `Graph.py`

Add the main algorithm method:

- `edmonds_karp(source, sink)` - returns maximum flow value
- `bfs_find_augmenting_path(source, sink)` - finds augmenting path using BFS with vertex labeling
- Vertex labels track: (parent_node, edge_capacity_used, flow_increment)
- Build residual graph during execution
- Return final flow value and optionally the flow matrix

### 3. Update `utils.py`

Modify file loading function:

- Change `load_graph_from_file()` to parse `u v capacity` format
- Remove the 'd'/'u' line (flow networks are always directed)
- Determine n from max node index
- Store capacities in the matrix

Update or remove visualization function to show capacities on edges.

### 4. Update `main.py`

Modify to:

- Load flow network from file
- Determine source (0) and sink (n-1) automatically
- Run Edmonds-Karp algorithm
- Display results: maximum flow value, augmenting paths found, final flow on each edge

### 5. Create Example Flow Network Files

Add new test files in `graphs/` directory with flow network format:

- `flow_network_1.txt` - simple example
- `flow_network_2.txt` - more complex example

Each file format: lines with `u v capacity`

## Implementation Details

**Edmonds-Karp with Vertex Labeling:**

- Use BFS to find shortest augmenting path
- Label format: `label[v] = (parent, edge_capacity, min_flow_to_v)`
- Track residual capacities: `residual[u][v] = capacity[u][v] - flow[u][v]`
- Update flow along augmenting path
- Repeat until no augmenting path exists

## TO-DO
- [x] Transform Graph.py into a FlowNetwork class with capacity matrix
- [x] Implement Edmonds-Karp algorithm with BFS and vertex labelling
- [ ] Update utils.py to load flow networks with u v capacity format
- [ ] Udate main.py to run  max flow algorithm and display results
- [ ] Create example network files