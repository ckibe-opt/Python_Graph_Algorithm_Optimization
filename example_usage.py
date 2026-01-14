import networkx as nx
from compiled_graph import CompiledGraph
import time

def main():
    print("--- Graph Optimization Demo ---")
    
    # 1. Setup a dummy graph (Social Network style)
    print("Creating social graph (10,000 users)...")
    G = nx.erdos_renyi_graph(n=10000, p=0.0008, seed=42)
    print(f"Graph created: {len(G.nodes)} nodes, {len(G.edges)} edges")

    # 2. Compile it
    print("\nCompiling graph structure...")
    t0 = time.time()
    cg = CompiledGraph(G)
    print(f"Compilation finished in {(time.time()-t0)*1000:.2f}ms")

    # 3. Compare SSSP (One-to-Many)
    source = 0
    print(f"\n[Query 1] Shortest paths from User {source} to ALL users:")
    
    t0 = time.perf_counter()
    nx_res = nx.single_source_dijkstra_path_length(G, source)
    t_nx = (time.perf_counter() - t0) * 1000
    print(f"  NetworkX: {t_nx:.2f} ms")

    t0 = time.perf_counter()
    opt_res = cg.single_source_shortest_paths(source)
    t_opt = (time.perf_counter() - t0) * 1000
    print(f"  Optimized: {t_opt:.2f} ms")
    print(f"  >> Speedup: {t_nx/t_opt:.1f}x")

    # 4. Compare Bidirectional (One-to-One)
    target = 5000
    print(f"\n[Query 2] Find connection between User {source} and User {target}:")
    
    t0 = time.perf_counter()
    try:
        nx.shortest_path_length(G, source, target)
    except: pass
    t_nx = (time.perf_counter() - t0) * 1000
    print(f"  NetworkX: {t_nx:.2f} ms")

    t0 = time.perf_counter()
    cg.bidirectional_shortest_path(source, target)
    t_opt = (time.perf_counter() - t0) * 1000
    print(f"  Optimized: {t_opt:.2f} ms")
    print(f"  >> Speedup: {t_nx/t_opt:.1f}x")

if __name__ == "__main__":
    main()