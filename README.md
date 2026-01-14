# Python Graph Algorithm Optimization

This repository contains experiments and optimizations for graph algorithms in Python. The goal is to compare plain NetworkX implementations with optimized/compiled approaches (referred here as "CompiledGraph") and document performance differences.

## Benchmark: NetworkX vs CompiledGraph

Below is the benchmark image comparing average latencies (milliseconds) for three algorithms. Add the image file at `images/benchmark_networkx_vs_compiledgraph.png` (I've referenced it below). If you prefer, upload the image with that path in the repository so it displays here.

![Benchmark: NetworkX vs CompiledGraph](images/benchmark_networkx_vs_compiledgraph.png)

Summary table (values read from the plotted bars):

| Algorithm | NetworkX (ms) | CompiledGraph (ms) |
|---|---:|---:|
| SSSP (Dijkstra) | 55.6 | 15.5 |
| Bidirectional Search | 26.7 | 0.4 |
| Connected Components | 14.6 | 14.8 |

Interpretation

- CompiledGraph shows a large improvement for SSSP and Bidirectional Search in these benchmarks.
- Connected Components runs at about the same speed for both implementations in this test.

Reproduce the plot

You can reproduce the chart with the following sample script (requires matplotlib):

```python
import matplotlib.pyplot as plt
import numpy as np

algorithms = ["SSSP (Dijkstra)", "Bidirectional Search", "Connected Components"]
networkx = [55.6, 26.7, 14.6]
compiled = [15.5, 0.4, 14.8]

x = np.arange(len(algorithms))
width = 0.35

fig, ax = plt.subplots(figsize=(10, 5))
rects1 = ax.bar(x - width/2, networkx, width, label='NetworkX')
rects2 = ax.bar(x + width/2, compiled, width, label='CompiledGraph', color='#ff7f0e')

ax.set_ylabel('Average Latency (ms)')
ax.set_title('Benchmark: NetworkX vs CompiledGraph')
ax.set_xticks(x)
ax.set_xticklabels(algorithms)
ax.legend()
ax.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)

for rect in rects1 + rects2:
    height = rect.get_height()
    ax.annotate(f'{height:.1f}', xy=(rect.get_x() + rect.get_width() / 2, height),
                xytext=(0, 3), textcoords='offset points', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.savefig('images/benchmark_networkx_vs_compiledgraph.png', dpi=150)
plt.show()
```

Notes

- The numeric values shown in the table are read from the plotted image and rounded to one decimal place. If you have the original benchmark data, replace them for exact reproduction.
- If you'd like, I can also add the image file to the repository (create `images/benchmark_networkx_vs_compiledgraph.png`) if you provide the binary or allow me to upload it.

---

License: MIT
