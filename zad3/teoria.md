# Metoda Ścieżki Krytycznej

**Metoda Ścieżki Krytycznej (CPM)** to algorytm używany w zarządzaniu projektami do analizy i planowania złożonych projektów. Jego głównym celem jest **identyfikacja najdłuższej sekwencji zależnych od siebie zadań, która określa minimalny możliwy czas ukończenia wszystkich czynności.**

## 1. Reprezentacja Sieci Projektu (AA vs AN)

### Sieć AN (Activity-on-Node)

W tym podejściu zadania (Activity) są reprezentowane przez węzły (Node), a strzałki (łuki) pokazują zależności (precedencje) między nimi. Jeśli zadanie B może się rozpocząć dopiero po zakończeniu zadania A, rysuje się strzałkę od węzła A do węzła B.

``` Python
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
```
### Sieć AA (Activity-on-Arc)

W podejściu zadania (Activity) są reprezentowane przez łuki (Arc), czyli strzałki. Węzły natomiast reprezentują "zdarzenia" – momenty rozpoczęcia lub zakończenia jednego lub więcej zadań.

Podejście to często wymaga wprowadzenia zadań pozornych (dummy tasks) – zadań o zerowym czasie trwania, które służą jedynie do pokazania skomplikowanych zależności, których nie dałoby się inaczej zamodelować (np. gdy zadanie C zależy od A, a D zależy od A i B).

Implementacja w kodzie: Metoda build_AA_network jest znacznie bardziej złożona. Tworzy węzły zdarzeń (np. `N0`, `N1`, `START`, `END`) i mapuje zadania na łuki (krawędzie) między tymi węzłami. Wprowadza również koncepcję zadań pozornych (dummy_tasks).

``` Python
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
```

## 2. Najwcześniejszy i Najpóźniejszy Moment Wykonania Zadania

Aby znaleźć ścieżkę krytyczną, CPM wykonuje dwa przejścia przez sieć: **"w przód"** (do obliczenia najwcześniejszych czasów) i **"w tył"** (do obliczenia najpóźniejszych czasów).

### Najwcześniejszy Moment (ES i EF) - Przejście "w przód"

Obliczenia te określają **najwcześniejsze możliwe terminy rozpoczęcia i zakończenia każdego zadania**, zakładając, że wszystkie poprzedzające zadania również rozpoczną się najwcześniej jak to możliwe.

- **Earliest Start (ES):** Najwcześniejszy moment rozpoczęcia zadania. Dla zadania bez poprzedników `ES = 0`. Dla pozostałych zadań ES jest równe `maksimum z czasów Earliest Finish (EF)` wszystkich jego bezpośrednich poprzedników.

- **Earliest Finish (EF):** Najwcześniejszy moment zakończenia zadania. Oblicza się go jako: `EF = ES + Czas Trwania Zadania`.

Implementacja w kodzie: Metoda `_calculate_earliest_times_AN` (dla sieci AN) wykorzystuje sortowanie topologiczne. Przechodzi przez zadania od początku do końca, obliczając ES i EF.
Python

```Python
def _calculate_earliest_times_AN(self):
    # Topological sort
    in_degree = {
        task_id: len(task.predecessors) 
        for task_id, task 
        in self.tasks.items()
    }
    queue = deque([
        task_id 
        for task_id, task 
        in self.tasks.items() 
        if len(task.predecessors) == 0
    ])
    
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
```

### Najpóźniejszy Moment (LS i LF) - Przejście "w tył"

Obliczenia te określają **najpóźniejsze terminy, w których zadania muszą się rozpocząć i zakończyć, aby nie opóźnić całego projektu**.

- **Latest Finish (LF)**: Najpóźniejszy moment zakończenia zadania. 
    - Dla zadań końcowych (bez następców) LF jest równe czasowi trwania całego projektu (makespan). 
    - Dla pozostałych zadań LF jest równe minimum z czasów Latest Start (LS) wszystkich jego bezpośrednich następców.

- **Latest Start (LS)**: Najpóźniejszy moment rozpoczęcia zadania. Oblicza się go jako: `LS = LF - Czas Trwania Zadania`.

Implementacja w kodzie: Metoda `_calculate_latest_times_AN` wykonuje podobny proces, ale "od tyłu" – zaczynając od zadań końcowych i cofając się do początkowych.
Python

``` Python
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
```

## 3. Ścieżka Krytyczna i Długość Uszeregowania

### Ścieżka Krytyczna (Critical Path)

Ścieżka krytyczna to sekwencja zadań, która determinuje całkowity czas trwania projektu. Są to zadania, które nie mają żadnej rezerwy czasowej (slack).

Rezerwa Czasowa (Slack): Jest to czas, o jaki można opóźnić zadanie, nie wpływając na termin końcowy całego projektu. Oblicza się ją jako: Slack = LS - ES (lub LF - EF).

Zadania na ścieżce krytycznej mają Slack = 0. Oznacza to, że ich "najwcześniejszy start" (ES) jest taki sam jak "najpóźniejszy start" (LS). Każde opóźnienie na zadaniu krytycznym bezpośrednio opóźnia cały projekt.

Implementacja w kodzie: Najpierw klasa Task oblicza rezerwę (slack) i sprawdza, czy zadanie jest krytyczne.

```Python
# (TaskNetwork.py, Task class)
class Task:
    # ...
    def calculate_slack(self):
        self.slack = self.latest_start - self.earliest_start
    
    def is_critical(self) -> bool:
        return self.slack == 0

    def find_critical_path(self) -> List[str]:
        critical_tasks = [
            task_id 
            for task_id, task 
            in self.tasks.items() 
            if task.is_critical()
        ]
        
        # Order critical tasks by earliest start time
        critical_tasks.sort(key=lambda tid: self.tasks[tid].earliest_start)
        
        return critical_tasks
```

### Długość Uszeregowania (Makespan)

Długość uszeregowania (Project Makespan) to **całkowity, minimalny czas potrzebny na ukończenie wszystkich zadań w projekcie**. Jest on równy długości ścieżki krytycznej, co odpowiada największemu czasowi Earliest Finish (EF) spośród wszystkich zadań w projekcie (szczególnie zadań końcowych).

Implementacja w kodzie: Makespan jest obliczany na końcu przejścia "w przód" (calculate_earliest_times).
Python

```Python
# (TaskNetwork.py, _calculate_earliest_times_AN)
    # ... (po pętli while)
    # Oblicz makespan
    self.makespan = max(task.earliest_finish for task in self.tasks.values())
```

## 4. Harmonogram (Schedule)

Podczas gdy CPM określa zależności i czasy, nie mówi nic o alokacji zasobów (w tym przypadku maszyn). Harmonogram (Schedule) to plan przypisania konkretnych zadań do dostępnych maszyn w określonych oknach czasowych.

Dostarczony kod implementuje prosty, chciwy algorytm harmonogramowania oparty na najwcześniejszych czasach startu (ES).

- Zadania są sortowane według ich czasu Earliest Start (ES).

- Program iteruje po posortowanych zadaniach.

- Dla każdego zadania szuka maszyny, która będzie wolna najwcześniej (ale nie wcześniej niż ES zadania).

- Zadanie jest przypisywane do tej maszyny, a czas dostępności maszyny jest aktualizowany na czas zakończenia tego zadania.

Implementacja w kodzie: Metoda create_schedule realizuje tę logikę.
Python

```Python
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
```

Wynikowy harmonogram jest następnie drukowany (przez utils.py) z oznaczeniem zadań krytycznych (*), jak w przykładzie README.md.

## 5. Działanie Programu Krok po Kroku

Opierając się na pliku main.py, oto jak program wykonuje analizę CPM:

1. Parsowanie Argumentów: Program uruchamia się z linii poleceń. main.py używa argparse do wczytania argumentów, takich jak ścieżka do pliku z zadaniami (filename) i typ sieci (--network-type).

```Python
# (main.py)
parser = argparse.ArgumentParser(...)
parser.add_argument('filename', type=str, ...)
parser.add_argument('--network-type', type=str, choices=['AA', 'AN'], ...)
args = parser.parse_args()
```

2. Wczytanie Danych: Funkcja load_task_network_from_file (z utils.py) otwiera wskazany plik. Odczytuje liczbę maszyn z pierwszej linii, a następnie parsuje kolejne linie, tworząc instancję TaskNetwork i wypełniając ją obiektami Task (z ich czasem trwania i poprzednikami).

3. Budowa Sieci: W zależności od argumentu --network-type, wywoływana jest metoda network.build_AN_network() lub network.build_AA_network(). Tworzy to wewnętrzną strukturę grafu (self.graph) gotową do analizy.

4. Obliczenia CPM (Przejście "w przód" i "w tył"):

    1. Najpierw wywoływane jest network.calculate_earliest_times(). Ta metoda (używając _AN lub _AA) przechodzi przez sieć "w przód" i oblicza earliest_start i earliest_finish dla każdego zadania oraz ustala self.makespan (całkowitą długość uszeregowania).

    2. Następnie wywoływane jest network.calculate_latest_times(). Ta metoda przechodzi przez sieć "w tył", używając makespan jako punktu startowego, i oblicza latest_start i latest_finish dla każdego zadania. Na koniec oblicza także rezerwę (slack) dla każdego z nich.

5. Generowanie Harmonogramu: Wywoływana jest metoda network.create_schedule(), która przypisuje zadania do maszyn, używając opisanej wcześniej chciwej strategii opartej na ES.

6. Wyświetlanie Wyników: Skrypt main.py wywołuje serię funkcji z utils.py:

    1. print_cpm_results: Drukuje tabelę ze wszystkimi zadaniami, ich czasami ES/EF/LS/LF, rezerwą (slack) i oznaczeniem, czy są krytyczne.

    2. print_critical_path: Znajduje ścieżkę krytyczną (network.find_critical_path()) i drukuje ją jako sekwencję zadań.

    3. print_schedule: Drukuje uporządkowany harmonogram, pokazując, która maszyna wykonuje jakie zadanie i w jakim czasie.

7. (Opcjonalnie) Wizualizacja: Jeśli użytkownik podał flagę --visualize, program dodatkowo wywołuje save_task_network_visualization (do stworzenia grafu sieciowego) i save_gantt_chart (do stworzenia wykresu Gantta harmonogramu), używając bibliotek networkx i matplotlib.