"""
Test Suite for CompiledGraph

Validates correctness against NetworkX ground truth.
"""

import networkx as nx
import random
from compiled_graph import CompiledGraph


def test_single_source_shortest_paths():
    """Test SSSP against NetworkX."""
    print("\n=== Testing Single-Source Shortest Paths ===")
    
    # Test 1: Simple chain
    G = nx.Graph()
    G.add_edge('A', 'B', weight=1)
    G.add_edge('B', 'C', weight=2)
    G.add_edge('C', 'D', weight=3)
    
    compiled = CompiledGraph(G)
    
    # Compare with NetworkX
    for source in ['A', 'B', 'C', 'D']:
        nx_result = nx.single_source_dijkstra_path_length(G, source)
        compiled_result = compiled.single_source_shortest_paths(source)
        
        assert nx_result == compiled_result, f"SSSP mismatch for source {source}"
        print(f"  ✓ SSSP from {source}: PASS")
    
    # Test 2: Diamond graph
    G2 = nx.Graph()
    G2.add_edge('A', 'B', weight=1)
    G2.add_edge('A', 'C', weight=4)
    G2.add_edge('B', 'D', weight=2)
    G2.add_edge('C', 'D', weight=1)
    
    compiled2 = CompiledGraph(G2)
    
    for source in ['A', 'B', 'C', 'D']:
        nx_result = nx.single_source_dijkstra_path_length(G2, source)
        compiled_result = compiled2.single_source_shortest_paths(source)
        
        assert nx_result == compiled_result, f"Diamond SSSP mismatch for source {source}"
        print(f"  ✓ Diamond SSSP from {source}: PASS")
    
    print("\n✅ All SSSP tests passed!")


def test_bidirectional_shortest_path():
    """Test bidirectional search against NetworkX."""
    print("\n=== Testing Bidirectional Shortest Path ===")
    
    # Test 1: Simple path
    G = nx.Graph()
    G.add_edge('A', 'B', weight=1)
    G.add_edge('B', 'C', weight=2)
    G.add_edge('C', 'D', weight=3)
    
    compiled = CompiledGraph(G)
    
    # Test all pairs
    pairs = [('A', 'D'), ('A', 'C'), ('B', 'D'), ('A', 'A')]
    
    for src, tgt in pairs:
        nx_dist = nx.shortest_path_length(G, src, tgt, weight='weight')
        
        result = compiled.bidirectional_shortest_path(src, tgt)
        assert result is not None, f"No path found for {src} -> {tgt}"
        
        compiled_dist, path = result
        
        # Check distance matches
        assert abs(compiled_dist - nx_dist) < 1e-9, f"Distance mismatch: {compiled_dist} vs {nx_dist}"
        
        # Check path is valid
        assert path[0] == src and path[-1] == tgt, f"Path endpoints wrong: {path}"
        
        print(f"  ✓ {src} -> {tgt}: distance={compiled_dist:.1f}, path={' -> '.join(path)}")
    
    # Test 2: Disconnected nodes
    G2 = nx.Graph()
    G2.add_edge('A', 'B', weight=1)
    G2.add_node('C')  # Isolated node
    
    compiled2 = CompiledGraph(G2)
    result = compiled2.bidirectional_shortest_path('A', 'C')
    
    assert result is None, "Should return None for disconnected nodes"
    print(f"  ✓ Disconnected nodes: correctly returns None")
    
    print("\n✅ All bidirectional tests passed!")


def test_bfs():
    """Test BFS traversal."""
    print("\n=== Testing BFS Traversal ===")
    
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(0, 2)
    G.add_edge(1, 3)
    G.add_edge(2, 4)
    
    compiled = CompiledGraph(G)
    
    # BFS from node 0
    bfs_result = compiled.bfs(0)
    
    # Check all nodes visited
    assert set(bfs_result) == set(G.nodes()), "Not all nodes visited in BFS"
    
    # Check source is first
    assert bfs_result[0] == 0, "Source should be first in BFS order"
    
    print(f"  ✓ BFS order: {bfs_result}")
    print("\n✅ BFS test passed!")


def test_dfs():
    """Test DFS traversal."""
    print("\n=== Testing DFS Traversal ===")
    
    G = nx.Graph()
    G.add_edge(0, 1)
    G.add_edge(0, 2)
    G.add_edge(1, 3)
    G.add_edge(2, 4)
    
    compiled = CompiledGraph(G)
    
    # DFS from node 0
    dfs_result = compiled.dfs(0)
    
    # Check all nodes visited
    assert set(dfs_result) == set(G.nodes()), "Not all nodes visited in DFS"
    
    # Check source is first
    assert dfs_result[0] == 0, "Source should be first in DFS order"
    
    print(f"  ✓ DFS order: {dfs_result}")
    print("\n✅ DFS test passed!")


def test_connected_components():
    """Test connected components against NetworkX."""
    print("\n=== Testing Connected Components ===")
    
    # Test 1: Single component
    G1 = nx.Graph()
    G1.add_edge('A', 'B')
    G1.add_edge('B', 'C')
    
    compiled1 = CompiledGraph(G1)
    components1 = compiled1.connected_components()
    
    assert len(components1) == 1, "Should have 1 component"
    assert components1[0] == {'A', 'B', 'C'}, "Component nodes mismatch"
    print(f"  ✓ Single component: {components1}")
    
    # Test 2: Multiple components
    G2 = nx.Graph()
    G2.add_edge('A', 'B')
    G2.add_edge('C', 'D')
    G2.add_node('E')  # Isolated
    
    compiled2 = CompiledGraph(G2)
    components2 = compiled2.connected_components()
    
    assert len(components2) == 3, f"Should have 3 components, got {len(components2)}"
    
    component_sets = [set(c) for c in components2]
    assert {'A', 'B'} in component_sets, "Missing A-B component"
    assert {'C', 'D'} in component_sets, "Missing C-D component"
    assert {'E'} in component_sets, "Missing isolated E component"
    
    print(f"  ✓ Multiple components: {len(components2)} components found")
    
    # Test 3: Large random graph
    G3 = nx.erdos_renyi_graph(100, 0.05, seed=42)
    compiled3 = CompiledGraph(G3)
    
    nx_components = list(nx.connected_components(G3))
    compiled_components = compiled3.connected_components()
    
    assert len(nx_components) == len(compiled_components), \
        f"Component count mismatch: NetworkX={len(nx_components)}, Compiled={len(compiled_components)}"
    
    print(f"  ✓ Large graph: {len(compiled_components)} components (matches NetworkX)")
    
    print("\n✅ All connected components tests passed!")


def test_large_graph():
    """Stress test with larger graph."""
    print("\n=== Testing Large Random Graph ===")
    
    # Generate sparse random graph
    random.seed(42)
    n = 1000
    G = nx.Graph()
    G.add_nodes_from(range(n))
    
    for _ in range(n * 4):  # ~4 edges per node
        u = random.randrange(n)
        v = random.randrange(n)
        if u != v:
            G.add_edge(u, v, weight=random.randint(1, 10))
    
    print(f"  Graph: {len(G.nodes())} nodes, {len(G.edges())} edges")
    
    compiled = CompiledGraph(G)
    
    # Test SSSP
    source = 0
    nx_result = nx.single_source_dijkstra_path_length(G, source)
    compiled_result = compiled.single_source_shortest_paths(source)
    
    assert nx_result == compiled_result, "SSSP mismatch on large graph"
    print(f"  ✓ SSSP: PASS")
    
    # Test bidirectional (sample pairs)
    for _ in range(10):
        src = random.randrange(n)
        tgt = random.randrange(n)
        
        try:
            nx_dist = nx.shortest_path_length(G, src, tgt, weight='weight')
            result = compiled.bidirectional_shortest_path(src, tgt)
            
            assert result is not None, f"Path should exist: {src} -> {tgt}"
            compiled_dist, _ = result
            
            assert abs(compiled_dist - nx_dist) < 1e-9, \
                f"Distance mismatch: {compiled_dist} vs {nx_dist}"
        except nx.NetworkXNoPath:
            # Disconnected - compiled should return None
            result = compiled.bidirectional_shortest_path(src, tgt)
            assert result is None, f"Should return None for disconnected pair {src} -> {tgt}"
    
    print(f"  ✓ Bidirectional (10 random pairs): PASS")
    
    # Test components
    nx_components = list(nx.connected_components(G))
    compiled_components = compiled.connected_components()
    
    assert len(nx_components) == len(compiled_components), "Component count mismatch"
    print(f"  ✓ Connected components: PASS")
    
    print("\n✅ Large graph tests passed!")


def run_all_tests():
    """Run complete test suite."""
    print("="*60)
    print("CompiledGraph Test Suite")
    print("="*60)
    
    test_single_source_shortest_paths()
    test_bidirectional_shortest_path()
    test_bfs()
    test_dfs()
    test_connected_components()
    test_large_graph()
    
    print("\n" + "="*60)
    print("🎉 ALL TESTS PASSED!")
    print("="*60)


if __name__ == "__main__":
    run_all_tests()