class UnionFind:
    def __init__(self, vertices, defects, boundary_nodes=None):
        vertices = set(vertices)
        defects = set(defects)

        if boundary_nodes is None:
            boundary_nodes = set()
        boundary_nodes = set(boundary_nodes)

        vertices.update(boundary_nodes)

        # Boundary nodes are not treated as syndrome defects.
        defects = defects - boundary_nodes

        self.boundary_nodes = boundary_nodes
        self.parent = {v: v for v in vertices}
        self.rank = {v: 0 for v in vertices}

        # Parity is meaningful only for non-boundary-connected clusters.
        self.parity = {v: (1 if v in defects else 0) for v in vertices}

        # A cluster touches a boundary if it contains any boundary node.
        self.touches_boundary = {v: (v in boundary_nodes) for v in vertices}

    def find(self, v):
        if self.parent[v] != v:
            self.parent[v] = self.find(self.parent[v])
        return self.parent[v]

    def union(self, u, v):
        ru, rv = self.find(u), self.find(v)

        if ru == rv:
            return False

        # Union by rank.
        if self.rank[ru] < self.rank[rv]:
            ru, rv = rv, ru

        self.parent[rv] = ru

        if self.rank[ru] == self.rank[rv]:
            self.rank[ru] += 1

        # The merged cluster touches a boundary if either component does.
        self.touches_boundary[ru] = (
            self.touches_boundary[ru] or self.touches_boundary[rv]
        )

        # Boundary-connected clusters are treated as satisfied.
        # Otherwise, parities combine modulo 2.
        if self.touches_boundary[ru]:
            self.parity[ru] = 0
        else:
            self.parity[ru] ^= self.parity[rv]

        return True

    def get_clusters(self):
        # Group nodes by their current union-find root.
        clusters = {}

        for v in self.parent:
            root = self.find(v)
            clusters.setdefault(root, []).append(v)

        return clusters

    def is_odd_root(self, root):
        # Only odd, non-boundary-connected clusters remain active.
        return self.parity[root] == 1 and not self.touches_boundary[root]


def uf_cluster_growth(vertices, edges, defects, boundary_nodes=None):
    """
    Run Union-Find cluster growth on a decoding graph.

    Parameters
    ----------
    vertices:
        Detector nodes only.

    edges:
        List of weighted edges in the form (u, v, w).

    defects:
        Detector nodes marked as syndrome defects.

    boundary_nodes:
        Boundary nodes in the graph.

    Returns
    -------
    clusters:
        Dictionary mapping each root node to the nodes in its cluster.

    parity:
        Dictionary storing the parity of each union-find root.

    touches_boundary:
        Dictionary indicating whether each root touches a boundary node.
    """

    vertices = set(vertices)
    defects = set(defects)

    # Infer boundary nodes from edge endpoints outside the detector-node set.
    if boundary_nodes is None:
        boundary_nodes = set()

        for edge in edges:
            u, v = edge[0], edge[1]

            if u not in vertices:
                boundary_nodes.add(u)

            if v not in vertices:
                boundary_nodes.add(v)

    else:
        boundary_nodes = set(boundary_nodes)

    uf = UnionFind(
        vertices=vertices,
        defects=defects,
        boundary_nodes=boundary_nodes
    )

    # Store each undirected edge with a direction-independent key.
    edge_list = []
    growth = {}

    for u, v, w in edges:
        edge_key = frozenset((u, v))
        edge_list.append((u, v, w, edge_key))
        growth[edge_key] = 0

    def boundary_edges(cluster_nodes):
        """
        Return edges crossing from the cluster to nodes outside the cluster.
        """

        cluster_set = set(cluster_nodes)
        result = []

        for u, v, w, edge_key in edge_list:
            if (
                (u in cluster_set and v not in cluster_set)
                or
                (v in cluster_set and u not in cluster_set)
            ):
                result.append((u, v, w, edge_key))

        return result

    while True:
        clusters = uf.get_clusters()

        odd_roots = {
            root
            for root in clusters
            if uf.is_odd_root(root)
        }

        # Stop when no odd, non-boundary-connected cluster remains.
        if not odd_roots:
            break

        fully_grown_edges = set()
        changed = False

        # Grow active clusters.
        for root in odd_roots:
            cluster_nodes = clusters[root]

            for u, v, w, edge_key in boundary_edges(cluster_nodes):
                if growth[edge_key] < w:
                    growth[edge_key] += 1
                    changed = True

                    if growth[edge_key] == w:
                        fully_grown_edges.add((u, v))

        # Merge clusters across fully grown edges.
        for u, v in fully_grown_edges:
            if uf.union(u, v):
                changed = True

        # Terminate if no edge growth or merge occurred in this iteration.
        if not changed:
            break

    return uf.get_clusters(), uf.parity, uf.touches_boundary