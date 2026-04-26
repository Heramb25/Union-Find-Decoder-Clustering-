import networkx as nx
import matplotlib.pyplot as plt


def make_nx_from_data(data):
    """
    Convert graph-data dictionary into a NetworkX graph.

    Expected data format:
        data = {
            "All_nodes": Vertices,
            "detector_nodes": Vertices - boundary_nodes,
            "boundary_nodes": boundary_nodes,
            "edges": Edges,
            "coord_by_det": pos
        }
    """

    all_nodes = set(data["All_nodes"])
    detector_nodes = set(data["detector_nodes"])
    boundary_nodes = set(data["boundary_nodes"])
    edges = data["edges"]
    pos = data["coord_by_det"]

    detector_nodes = detector_nodes - boundary_nodes

    graph = nx.Graph()
    graph.add_nodes_from(all_nodes)

    for edge in edges:
        u, v = edge[0], edge[1]
        graph.add_edge(u, v)

    return graph, pos, detector_nodes, boundary_nodes


def visualize_uf_run(uf_graph, defects, clusters):
    """
    Visualize the initial syndrome-defect graph and final Union-Find clusters.

    Parameters
    ----------
    uf_graph:
        Graph-data dictionary returned by the graph-building function.

    defects:
        Set/list of defect detector nodes.

    clusters:
        Output from UnionFind.get_clusters().
        Format: {root: [nodes_in_cluster]}

    Boundary nodes are always drawn as fixed light-gray squares.
    """

    graph, pos, det_nodes, bnd_nodes = make_nx_from_data(uf_graph)

    det_nodes = set(det_nodes)
    bnd_nodes = set(bnd_nodes)

    defects = set(defects)
    defects = defects - bnd_nodes
    defects = defects & det_nodes

    filtered_clusters = {}

    for root, nodes in clusters.items():
        det_cluster_nodes = [node for node in nodes if node in det_nodes]

        if len(det_cluster_nodes) > 1:
            filtered_clusters[root] = det_cluster_nodes

    node_to_cluster = {}

    for root, nodes in filtered_clusters.items():
        for node in nodes:
            node_to_cluster[node] = root

    cmap = plt.get_cmap("tab20")

    cluster_color = {
        root: cmap(index % 20)
        for index, root in enumerate(filtered_clusters.keys())
    }

    det_labels = {node: str(node) for node in det_nodes}
    bnd_labels = {node: f"B{node}" for node in bnd_nodes}

    fig, axes = plt.subplots(1, 2, figsize=(15, 7))

    # Initial graph
    ax = axes[0]
    ax.set_title("Union Find - Initial graph")

    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        width=1.5,
        edge_color="gray"
    )

    normal_nodes = [node for node in det_nodes if node not in defects]
    defect_nodes = [node for node in det_nodes if node in defects]

    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        nodelist=normal_nodes,
        node_size=500,
        node_color="white",
        edgecolors="black"
    )

    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        nodelist=defect_nodes,
        node_size=550,
        node_color="red",
        edgecolors="black"
    )

    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        nodelist=list(bnd_nodes),
        node_size=320,
        node_shape="s",
        node_color="lightgray",
        edgecolors="black"
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        labels=det_labels,
        ax=ax,
        font_size=9,
        font_weight="bold"
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        labels=bnd_labels,
        ax=ax,
        font_size=8,
        font_weight="bold"
    )

    ax.axis("equal")
    ax.axis("off")

    # Final clusters
    ax = axes[1]
    ax.set_title("Union Find - Final clusters")

    nx.draw_networkx_edges(
        graph,
        pos,
        ax=ax,
        width=1.5,
        edge_color="gray"
    )

    neutral_nodes = [
        node for node in det_nodes
        if node not in node_to_cluster
    ]

    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        nodelist=neutral_nodes,
        node_size=500,
        node_color="white",
        edgecolors="black"
    )

    for root, nodes in filtered_clusters.items():
        nx.draw_networkx_nodes(
            graph,
            pos,
            ax=ax,
            nodelist=nodes,
            node_size=550,
            node_color=[cluster_color[root]],
            edgecolors="black"
        )

    nx.draw_networkx_nodes(
        graph,
        pos,
        ax=ax,
        nodelist=list(bnd_nodes),
        node_size=320,
        node_shape="s",
        node_color="lightgray",
        edgecolors="black"
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        labels=det_labels,
        ax=ax,
        font_size=9,
        font_weight="bold"
    )

    nx.draw_networkx_labels(
        graph,
        pos,
        labels=bnd_labels,
        ax=ax,
        font_size=8,
        font_weight="bold"
    )

    ax.axis("equal")
    ax.axis("off")

    plt.tight_layout()
    plt.show()