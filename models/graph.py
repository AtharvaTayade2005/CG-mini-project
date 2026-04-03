class GraphModel:
    def __init__(self):
        self.adj = {}
        self.edges_list = [] # (u, v, weight, directed)

    def add_vertex(self, v):
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u, v, directed=False, weight=1):
        self.add_vertex(u)
        self.add_vertex(v)
        
        # Check if already exists to avoid duplicates
        if not any(nbr == v for nbr, w, d in self.adj[u]):
            self.adj[u].append((v, weight, directed))
            self.edges_list.append((u, v, weight, directed))
            
        if not directed:
            if not any(nbr == u for nbr, w, d in self.adj[v]):
                self.adj[v].append((u, weight, directed))

    # --- EXISTING TRAVERSALS ---
    def get_bfs_steps(self, start):
        if start not in self.adj: return []
        visited = set([start])
        queue = [start]
        steps = []
        while queue:
            node = queue.pop(0)
            steps.append((node, list(queue), None, f"Dequeued node {node} from Queue."))
            for nbr, w, d in self.adj[node]:
                if nbr not in visited:
                    visited.add(nbr)
                    queue.append(nbr)
                    steps.append((None, list(queue), (node, nbr), f"Discovered neighbor {nbr}. Added to Queue."))
        return steps

    def get_dfs_steps(self, start):
        if start not in self.adj: return []
        visited = set()
        stack = [start]
        steps = []
        while stack:
            node = stack.pop()
            if node not in visited:
                visited.add(node)
                steps.append((node, list(stack), None, f"Popped node {node} from Stack. Marking visited."))
                for nbr, w, d in reversed(self.adj[node]):
                    if nbr not in visited:
                        stack.append(nbr)
                        steps.append((None, list(stack), (node, nbr), f"Found unvisited neighbor {nbr}. Pushing to Stack."))
        return steps

    # --- ADVANCED ALGORITHMS GENERATORS ---
    def dijkstra(self, start):
        import math
        dist = {v: math.inf for v in self.adj}
        if start not in dist: return
        dist[start] = 0
        visited = set()
        
        yield {'visited': set(), 'dist': dist.copy(), 'current': start, 'msg': f"Starting Dijkstra from {start}. All other distances set to infinity."}
        
        for _ in range(len(self.adj)):
            u = None
            min_d = math.inf
            for v in self.adj:
                if v not in visited and dist[v] <= min_d:
                    min_d = dist[v]
                    u = v
            if u is None: break
            visited.add(u)
            yield {'visited': visited.copy(), 'dist': dist.copy(), 'current': u, 'msg': f"Selected unvisited node {u} with minimum distance {dist[u]}."}
            
            for v, w, d in self.adj[u]:
                if v not in visited:
                    yield {'visited': visited.copy(), 'dist': dist.copy(), 'current': u, 'edge': (u, v), 'msg': f"Checking edge from {u} to {v} (weight: {w})."}
                    if dist[u] + w < dist[v]:
                        old_d = dist[v]
                        dist[v] = dist[u] + w
                        yield {'visited': visited.copy(), 'dist': dist.copy(), 'current': v, 'edge': (u, v), 'updated': v, 'msg': f"Found shorter path! Relaxing {v}: {old_d} -> {dist[v]}."}

        yield {'visited': visited.copy(), 'dist': dist.copy(), 'msg': "Dijkstra's Algorithm completed. Shortest paths finalized!"}

    def bellman_ford(self, start):
        import math
        dist = {v: math.inf for v in self.adj}
        if start not in dist: return
        dist[start] = 0
        
        edges = []
        for u in self.adj:
            for v, w, d in self.adj[u]:
                edges.append((u, v, w))

        yield {'dist': dist.copy(), 'edges': edges, 'msg': f"Starting Bellman-Ford from {start}. Initializing all other distances to infinity."}
        
        for i in range(len(self.adj) - 1):
            yield {'dist': dist.copy(), 'iteration': i+1, 'msg': f"--- Starting Bellman-Ford Iteration {i+1} ---"}
            for u, v, w in edges:
                yield {'dist': dist.copy(), 'edge': (u, v), 'iteration': i+1, 'msg': f"Checking edge {u} -> {v} (weight {w})."}
                if dist[u] != math.inf and dist[u] + w < dist[v]:
                    old_d = dist[v]
                    dist[v] = dist[u] + w
                    yield {'dist': dist.copy(), 'edge': (u, v), 'updated': v, 'iteration': i+1, 'msg': f"Relaxed node {v}: distance updated from {old_d} to {dist[v]}."}

        yield {'dist': dist.copy(), 'msg': "Bellman-Ford Algorithm completed. All nodes naturally settled."}

    def prim_mst(self):
        import math
        if not self.adj: return
        
        start = list(self.adj.keys())[0]
        visited = set([start])
        mst_edges = []
        
        yield {'visited': visited.copy(), 'mst_edges': mst_edges.copy(), 'current': start, 'msg': f"Starting Prim's MST from arbitrary node {start}."}
        
        while len(visited) < len(self.adj):
            min_e = None
            min_w = math.inf
            
            for u in visited:
                for v, w, d in self.adj[u]:
                    if v not in visited:
                        yield {'visited': visited.copy(), 'mst_edges': mst_edges.copy(), 'edge': (u, v), 'check': True, 'msg': f"Evaluating edge {u} -> {v} (weight {w}) connecting to unvisited region."}
                        if w < min_w:
                            min_w = w
                            min_e = (u, v)
                            
            if not min_e: break
            visited.add(min_e[1])
            mst_edges.append(min_e)
            yield {'visited': visited.copy(), 'mst_edges': mst_edges.copy(), 'edge': min_e, 'added': True, 'msg': f"Selected minimum crossing edge {min_e[0]} -> {min_e[1]}. Added to MST!"}

        yield {'visited': visited.copy(), 'mst_edges': mst_edges.copy(), 'msg': "Prim's Algorithm completed! Minimum Spanning Tree is fully connected."}

    def kruskal_mst(self):
        parent = {v: v for v in self.adj}
        def find(i):
            if parent[i] == i:
                return i
            parent[i] = find(parent[i])
            return parent[i]
            
        def union(i, j):
            root_i = find(i)
            root_j = find(j)
            if root_i != root_j:
                parent[root_i] = root_j
                return True
            return False

        edges = []
        seen = set()
        for u, v, w, d in self.edges_list:
            if d: continue 
            if (u, v) not in seen and (v, u) not in seen:
                edges.append((w, u, v))
                seen.add((u, v))
                
        yield {'edges': edges, 'mst_edges': [], 'msg': "Starting Kruskal's MST. Gathering all undirected edges."}
        edges.sort()
        yield {'edges': edges, 'mst_edges': [], 'sorted': True, 'msg': "Sorted all edges by ascending weight. We will evaluate them one by one."}
        
        mst_edges = []
        for w, u, v in edges:
            yield {'mst_edges': mst_edges.copy(), 'edge': (u, v), 'check': True, 'msg': f"Checking edge {u} - {v} (weight {w}). Will it cause a cycle?"}
            if union(u, v):
                mst_edges.append((u, v))
                yield {'mst_edges': mst_edges.copy(), 'edge': (u, v), 'added': True, 'msg': f"No cycle! Added edge {u} - {v} to the MST."}
            else:
                yield {'mst_edges': mst_edges.copy(), 'edge': (u, v), 'check': True, 'msg': f"Cycle detected! Ignoring edge {u} - {v}."}

        yield {'mst_edges': mst_edges.copy(), 'msg': "Kruskal's Algorithm completed! Minimum Spanning Tree is assembled."}
