import time
import random
import statistics
import networkx as nx
from compiled_graph import CompiledGraph

def generate_benchmark_graph(n=10000, avg_degree=8):
    """Generate a realistic sparse graph."""
    print(f"[*] Generating {n}-node graph...")
    start = time.time()
    
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    for i in range(n-1):
        G.add_edge(i, i+1, weight=random.randint(1, 10))
        
    num_extra_edges = (n * avg_degree) // 2
    for _ in range(num_extra_edges):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v:
            G.add_edge(u, v, weight=random.randint(1, 10))
            
    print(f"    -> Done in {time.time() - start:.2f}s. Nodes: {n}, Edges: {G.number_of_edges()}")
    return G

def benchmark():
    N_NODES = 10000
    N_QUERIES = 100
    G = generate_benchmark_graph(n=N_NODES, avg_degree=8)
    
    pairs = []
    for _ in range(N_QUERIES):
        u = random.randint(0, N_NODES-1)
        v = random.randint(0, N_NODES-1)
        pairs.append((u, v))
        
    print(f"[*] Benchmarking {N_QUERIES} random path queries...")
    print("-" * 60)

    # NetworkX
    nx_times = []
    print("Running NetworkX...", end="", flush=True)
    start_global = time.time()
    for u, v in pairs:
        t0 = time.perf_counter()
        try:
            _ = nx.shortest_path_length(G, u, v, weight='weight')
        except nx.NetworkXNoPath:
            pass
        dt = (time.perf_counter() - t0) * 1000
        nx_times.append(dt)
    print(f" Done ({time.time() - start_global:.2f}s)")

    # CompiledGraph
    print("Running CompiledGraph...", end="", flush=True)
    t0 = time.perf_counter()
    cg = CompiledGraph(G)
    compile_time_ms = (time.perf_counter() - t0) * 1000
    
    cg_times = []
    for u, v in pairs:
        t0 = time.perf_counter()
        _ = cg.bidirectional_shortest_path(u, v)
        dt = (time.perf_counter() - t0) * 1000
        cg_times.append(dt)
    print(" Done")

    nx_avg = statistics.mean(nx_times)
    cg_avg = statistics.mean(cg_times)
    speedup = nx_avg / cg_avg
    
    print("\n" + "="*60)
    print(f"{'BIDIRECTIONAL SEARCH BENCHMARK':^60}")
    print("="*60)
    print(f"{'Metric':<20} | {'NetworkX':<15} | {'CompiledGraph':<15}")
    print("-" * 60)
    print(f"{'Avg Latency':<20} | {nx_avg:<15.2f} | {cg_avg:<15.2f}")
    print(f"{'Min Latency':<20} | {min(nx_times):<15.2f} | {min(cg_times):<15.2f}")
    print(f"{'Max Latency':<20} | {max(nx_times):<15.2f} | {max(cg_times):<15.2f}")
    print("-" * 60)
    print(f"SPEEDUP:           {speedup:.2f}x")
    print(f"Compilation Cost:  {compile_time_ms:.2f} ms")
    print("="*60)

if __name__ == "__main__":
    benchmark()