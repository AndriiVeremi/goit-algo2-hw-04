from collections import deque

# Path search in graph (BFS)
def bfs(graph, s, t, p):
    visited = [False] * len(graph)
    queue = deque()
    queue.append(s)
    visited[s] = True
    p[s] = -1

    while queue:
        u = queue.popleft()
        for v, capacity in enumerate(graph[u]):
            if not visited[v] and capacity > 0:
                queue.append(v)
                visited[v] = True
                p[v] = u
                if v == t:
                    return True
    return False

# Edmonds-Karp Algorithm
def edmonds_karp(graph, source, sink):
    num_nodes = len(graph)
    r_graph = [row[:] for row in graph] # make a copy of the graph
    p = [0] * num_nodes
    max_flow = 0
    found_paths = []

    while bfs(r_graph, source, sink, p):
        path_flow = float('Inf')
        s = sink
        path = []
        while s != source:
            path.append(s)
            path_flow = min(path_flow, r_graph[p[s]][s])
            s = p[s]
        path.append(source)
        path.reverse()
        found_paths.append((path, path_flow))

        max_flow += path_flow

        v = sink
        while v != source:
            u = p[v]
            r_graph[u][v] -= path_flow
            r_graph[v][u] += path_flow
            v = p[v]

    return max_flow, r_graph, found_paths

def main():
    # All points in the network
    nodes = [
        'Source', 'Terminal 1', 'Terminal 2', 'Warehouse 1', 'Warehouse 2', 'Warehouse 3', 'Warehouse 4',
        'Shop 1', 'Shop 2', 'Shop 3', 'Shop 4', 'Shop 5', 'Shop 6', 'Shop 7',
        'Shop 8', 'Shop 9', 'Shop 10', 'Shop 11', 'Shop 12', 'Shop 13', 'Shop 14', 'Sink'
    ]
    node_to_idx = {name: i for i, name in enumerate(nodes)}
    num_nodes = len(nodes)

    # Create the graph
    graph = [[0] * num_nodes for _ in range(num_nodes)]

    # Add edges
    edges = {
        ('Source', 'Terminal 1'): 60,
        ('Source', 'Terminal 2'): 55,
        ('Terminal 1', 'Warehouse 1'): 25,
        ('Terminal 1', 'Warehouse 2'): 20,
        ('Terminal 1', 'Warehouse 3'): 15,
        ('Terminal 2', 'Warehouse 2'): 10,
        ('Terminal 2', 'Warehouse 3'): 15,
        ('Terminal 2', 'Warehouse 4'): 30,
        ('Warehouse 1', 'Shop 1'): 15,
        ('Warehouse 1', 'Shop 2'): 10,
        ('Warehouse 1', 'Shop 3'): 20,
        ('Warehouse 2', 'Shop 4'): 15,
        ('Warehouse 2', 'Shop 5'): 10,
        ('Warehouse 2', 'Shop 6'): 25,
        ('Warehouse 3', 'Shop 7'): 20,
        ('Warehouse 3', 'Shop 8'): 15,
        ('Warehouse 3', 'Shop 9'): 10,
        ('Warehouse 4', 'Shop 10'): 20,
        ('Warehouse 4', 'Shop 11'): 10,
        ('Warehouse 4', 'Shop 12'): 15,
        ('Warehouse 4', 'Shop 13'): 5,
        ('Warehouse 4', 'Shop 14'): 10,
    }

    for (u, v), capacity in edges.items():
        graph[node_to_idx[u]][node_to_idx[v]] = capacity

    # Connect shops to the sink
    for i in range(1, 15):
        shop_name = f'Shop {i}'
        graph[node_to_idx[shop_name]][node_to_idx['Sink']] = float('Inf')

    source = node_to_idx['Source']
    sink = node_to_idx['Sink']

    max_flow, residual_graph, augmenting_paths = edmonds_karp(graph, source, sink)

    print(f"Maximum flow: {max_flow}\n")

    print("Found paths for the flow:")
    for i, (path_nodes, flow) in enumerate(augmenting_paths):
        path_str = " -> ".join([nodes[n] for n in path_nodes])
        print(f"  Step {i+1}: {path_str}, flow: {flow}")

    print("\n--- Results Analysis ---")

    # Calculate the actual flow for each edge
    flow_graph = [[0] * num_nodes for _ in range(num_nodes)]
    for i in range(num_nodes):
        for j in range(num_nodes):
            if graph[i][j] > 0:
                flow_graph[i][j] = graph[i][j] - residual_graph[i][j]

    # Calculating Terminal -> Shop flows
    result_flows = {
        'Terminal 1': {f'Shop {i}': 0 for i in range(1, 15)},
        'Terminal 2': {f'Shop {i}': 0 for i in range(1, 15)}
    }

    for i in range(1, 5):
        wh_name = f'Warehouse {i}'
        wh_node = node_to_idx[wh_name]

        flow_from_t1 = flow_graph[node_to_idx['Terminal 1']][wh_node]
        flow_from_t2 = flow_graph[node_to_idx['Terminal 2']][wh_node]
        total_in_flow = flow_from_t1 + flow_from_t2

        if total_in_flow == 0:
            continue

        ratio1 = flow_from_t1 / total_in_flow
        ratio2 = flow_from_t2 / total_in_flow

        for j in range(1, 15):
            shop_name = f'Shop {j}'
            shop_node = node_to_idx[shop_name]
            
            flow_wh_to_shop = flow_graph[wh_node][shop_node]

            if flow_wh_to_shop > 0:
                result_flows['Terminal 1'][shop_name] += flow_wh_to_shop * ratio1
                result_flows['Terminal 2'][shop_name] += flow_wh_to_shop * ratio2

    print("\nFlow table from terminals to shops:")
    print("----------------------------------------")
    for shop_name, flow in result_flows['Terminal 1'].items():
        if flow > 0:
            print(f"Terminal 1 -> {shop_name} = {flow:.2f}")
    for shop_name, flow in result_flows['Terminal 2'].items():
        if flow > 0:
            print(f"Terminal 2 -> {shop_name} = {flow:.2f}")
    print("----------------------------------------")

    # Answering questions
    print("\n--- Answering Questions ---")
    terminal1_flow = sum(flow_graph[node_to_idx['Terminal 1']])
    terminal2_flow = sum(flow_graph[node_to_idx['Terminal 2']])
    shop_flows = {}
    for i in range(1, 15):
        shop_name = f'Shop {i}'
        shop_node = node_to_idx[shop_name]
        in_flow = sum(flow_graph[j][shop_node] for j in range(num_nodes))
        shop_flows[shop_name] = in_flow

    print("\n1. Which terminals provide the most flow?")
    if terminal1_flow > terminal2_flow:
        print(f"   Answer: Terminal 1 ({terminal1_flow:.2f}) provides more than Terminal 2 ({terminal2_flow:.2f})")
    else:
        print(f"   Answer: Terminal 2 ({terminal2_flow:.2f}) provides more than Terminal 1 ({terminal1_flow:.2f})")

    print("\n2. Which routes are the weakest?")
    min_cap_val = min(c for (u,v), c in edges.items() if c > 0 and 'Source' not in u)
    min_routes = [f'{u} -> {v}' for (u,v), c in edges.items() if c == min_cap_val]
    print(f"   Answer: The lowest capacity is {min_cap_val}. Routes: {min_routes}")

    print("\n3. Which shops received the least goods?")
    min_flow_val = min(shop_flows.values())
    min_flow_shops = [shop for shop, flow in shop_flows.items() if flow == min_flow_val]
    print(f"   Answer: The least goods ({min_flow_val:.2f}) were received by: {min_flow_shops}")

    print("\n4. Where are the 'bottlenecks'?")
    bottlenecks = []
    for i in range(num_nodes):
        for j in range(num_nodes):
            if graph[i][j] > 0 and flow_graph[i][j] == graph[i][j]:
                bottlenecks.append(f'{nodes[i]} -> {nodes[j]}')
    print(f"   Answer: Fully loaded routes: {bottlenecks}")

if __name__ == "__main__":
    main()
