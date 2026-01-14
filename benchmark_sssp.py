import time
import heapq
import math
import random
import statistics
import sys

try:
    import networkx as nx
    from compiled_graph import CompiledGraph, compile_graph
    print("[+] NetworkX and CompiledGraph detected.")
except ImportError as e:
    print(f"[!] Error: {e}")
    sys.exit(1)

def generate_large_sparse_graph(n=10000, avg_degree=8):
    """Generates a realistic large sparse graph (NetworkX object)."""
    print(f"[*] Generating {n}-node graph...")
    start = time.time()
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    # Ensure connectivity roughly
    for i in range(n-1):
        G.add_edge(i, i+1, weight=random.randint(1, 10))
        
    # Add random edges
    num_extra_edges = (n * avg_degree) // 2
    for _ in range(num_extra_edges):
        u = random.randint(0, n-1)
        v = random.randint(0, n-1)
        if u != v:
            G.add_edge(u, v, weight=random.randint(1, 10))
            
    print(f"    -> Done in {time.time() - start:.2f}s. Edges: {G.number_of_edges()}")
    return G

def benchmark_single(name, func, args_generator, num_queries):
    """Runs a benchmark for a single function."""
    print(f"[*] Running {name} ({num_queries} queries)...")
    times = []
    
    # Warmup
    try:
        args = args_generator(0)
        _ = func(*args)
    except Exception as e:
        print(f"[!] {name} failed warmup: {e}")
        return []

    for i in range(num_queries):
        args = args_generator(i)
        t0 = time.perf_counter()
        try:
            _ = func(*args)
            times.append((time.perf_counter() - t0) * 1000) # ms
        except Exception:
            continue
            
    return times

def print_report(nx_times, ev_times, compile_cost):
    print("\n" + "="*80)
    print(f"{'BENCHMARK REPORT: GRAPH SSSP OPTIMIZATION':^80}")
    print("="*80)
    print(f"Graph Size:       10,000 Nodes, ~80,000 Edges")
    print(f"Workload:         {len(nx_times)} Randomized Queries")
    print("-" * 80)
    print(f"{'Metric':<20} | {'NetworkX':<15} | {'Optimized':<15}")
    print("-" * 80)
    
    def get_stats(times):
        if not times: return 0, 0, 0
        return statistics.mean(times), min(times), max(times)

    nx_avg, nx_min, nx_max = get_stats(nx_times)
    ev_avg, ev_min, ev_max = get_stats(ev_times)

    print(f"{'Avg Latency (ms)':<20} | {nx_avg:<15.2f} | {ev_avg:<15.2f}")
    print(f"{'Min Latency (ms)':<20} | {nx_min:<15.2f} | {ev_min:<15.2f}")
    print(f"{'Max Latency (ms)':<20} | {nx_max:<15.2f} | {ev_max:<15.2f}")
    print("-" * 80)
    
    speedup = nx_avg / ev_avg if ev_avg > 0 else 0
    
    print(f"{'SPEEDUP':<20} | {'1.00x':<15} | {speedup:<15.2f}x")
    print("-" * 80)
    
    # Amortization Analysis
    if ev_avg > 0 and nx_avg > ev_avg:
        break_even = compile_cost / (nx_avg - ev_avg)
        be_str = f"~{math.ceil(break_even)} queries"
    else:
        be_str = "N/A"
        
    print(f"Arch. Compilation: {compile_cost:.2f} ms (One-time cost)")
    print(f"Break-even Point:  {be_str} (vs NetworkX)")
    print("="*80)

def main():
    print("--- [Benchmark Hero] Initialization ---")
    
    # 1. Setup Data
    G = generate_large_sparse_graph(n=10000, avg_degree=8)
    num_queries = 100
    sources = [random.randint(0, len(G)-1) for _ in range(num_queries)]
    
    # 2. NetworkX Baseline
    nx_times = benchmark_single(
        "NetworkX", 
        nx.single_source_dijkstra_path_length, 
        lambda i: (G, sources[i]), 
        num_queries
    )
    
    # 3. Compiled/Optimized Solution
    print("[*] Compiling Graph for Optimized Architecture...")
    t_start = time.perf_counter()
    CG = compile_graph(G)
    compile_cost = (time.perf_counter() - t_start) * 1000
    
    ev_times = benchmark_single(
        "Optimized Arch",
        CG.single_source_shortest_paths,
        lambda i: (sources[i],),
        num_queries
    )
    
    # 4. Report
    print_report(nx_times, ev_times, compile_cost)

if __name__ == "__main__":
    main()