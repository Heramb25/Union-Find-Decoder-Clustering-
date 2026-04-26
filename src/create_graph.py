def Create_Dummy_Surface_code_graph(n):
    V = set(i for i in range(1,4*n**2+1))
    pos = {}
    k = n*2
    j = 0
    for i in range(len(V)+1):
        c = (i-1)%(k)
        r = (i-1)//(k)
        if r% 2 == 0 and i%2 == 0:
            j += 1
            pos[j] = (c,r)
        if r% 2 == 1 and i%2 == 1:
            j += 1
            pos[j] = (c,r)
    
    Vertices = set(i for i in range(1,2*n**2+1))
    Edges = set()
    for i in pos.keys():
        if pos[i][1] % 2 == 0 and pos[i][0] != 2*n-1:
            if i+n-1 in Vertices:
                Edges.add((i,i+n))
            if i +n+1 in Vertices:
                Edges.add((i, i +n+1))
        if pos[i][1] % 2 == 0 and pos[i][0] == 2*n-1:
            if i+n-1 in Vertices:
                Edges.add((i,i+n))
            #if i +n+1 in Vertices:
            #    edges.add((i, i +n+1))
        if pos[i][1] % 2 == 1 and pos[i][0] != 0:
            if i+n in Vertices:
                Edges.add((i,i+n))
            if i +n-1 in Vertices:
                Edges.add((i, i +n-1))
        if pos[i][1] % 2 == 1 and pos[i][0] == 0:
            if i+n in Vertices:
                Edges.add((i,i+n))
            #if i +n-1 in Vertices:
            #    edges.add((i, i +n-1))
    boundary_nodes = set()
    for i in pos.keys():
        if pos[i][0] == 0 or pos[i][0] == 2*n - 1:
            boundary_nodes.add(i)
    data = {
        "All_nodes": Vertices,
        "detector_nodes": Vertices - boundary_nodes,
        "boundary_nodes": boundary_nodes,
        "edges": Edges,
        "coord_by_det": pos
    }
    return data