# Union-Find Decoder Clustering

This repository contains a simplified implementation of the **clustering stage of a Union-Find decoder** for surface-code-inspired quantum error-correction experiments.

The main aim of this repository is to demonstrate how syndrome defects can be grouped into clusters using Union-Find growth and merging rules. Instead of directly using a full Stim-generated surface-code decoding graph, this repository uses a manually constructed dummy surface-code-like graph. This makes the clustering logic easier to understand, debug, visualize, and explain.

This implementation focuses only on the **cluster formation stage** of Union-Find decoding. It does not yet implement the final correction-chain extraction step.

---

## Repository Structure

```text
Union-Find-Decoder-Clustering-
│
├── main.ipynb
│
└── src/
    ├── create_graph.py
    ├── union_find.py
    └── uf_visualization.py

```
## Install the required packages using:
```text
pip install networkx matplotlib jupyter
```
