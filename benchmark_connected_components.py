import time
import statistics
import networkx as nx
from compiled_graph import CompiledGraph

def generate_benchmark_graph(n=20000, p=0.0005):
    """Generate a large sparse graph."""
    print(f"[*] Generating {n}-node graph...")
    start = time.time()
    G = nx.erdos_renyi_graph(n, p, seed=42)
    print(f"    -> Done in {time.time() - start:.2f}s. Edges: {G.number_of_edges()}")
    return G

def benchmark():
    print("--- [Benchmark: Connected Components] ---")
    
    # Setup Data
    G = generate_benchmark_graph(n=20000, p=0.0005)
    print("-" * 60)

    # NetworkX Baseline
    print("Running NetworkX...", end="", flush=True)
    t0 = time.perf_counter()
    nx_comps = list(nx.connected_components(G))
    nx_time = (time.perf_counter() - t0) * 1000
    print(f" Done ({nx_time:.2f} ms)")

    # CompiledGraph Reference
    print("Running CompiledGraph...", end="", flush=True)
    cg = CompiledGraph(G) 
    t0 = time.perf_counter()
    ref_comps = cg.connected_components()
    ref_time = (time.perf_counter() - t0) * 1000
    print(f" Done ({ref_time:.2f} ms)")

    # Verification
    print("-" * 60)
    print(f"NetworkX Found: {len(nx_comps)} components")
    print(f"Compiled Found: {len(ref_comps)} components")
    
    if len(nx_comps) != len(ref_comps):
        print("[!] WARNING: Component counts disagree!")
    else:
        print("[+] Correctness Check: PASS")

    # Report
    speedup = nx_time / ref_time
    print("="*60)
    print(f"{'Metric':<20} | {'NetworkX':<15} | {'CompiledGraph':<15}")
    print("-" * 60)
    print(f"{'Time (ms)':<20} | {nx_time:<15.2f} | {ref_time:<15.2f}")
    print(f"{'Speedup':<20} | {'1.00x':<15} | {speedup:<15.2f}x")
    print("="*60)

if __name__ == "__main__":
    benchmark()