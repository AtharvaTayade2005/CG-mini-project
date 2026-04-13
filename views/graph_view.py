import math
import tkinter as tk
from views.base_view import BaseView
from models.graph import GraphModel

class GraphView(BaseView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.model = GraphModel()
        self.nodes = {} 
        self.edges = []
        self.generator = None
        self.delay = 2000 # Increased delay for readability

    def calculate_targets(self):
        n = len(self.nodes)
        if n == 0: return
        cx = self.width / 2
        cy = self.height / 2 - 30
        radius = min(self.width, self.height) * 0.35
        
        for i, val in enumerate(self.nodes.keys()):
            angle = i * (2 * math.pi / n)
            self.nodes[val]['x_target'] = cx + radius * math.cos(angle)
            self.nodes[val]['y_target'] = cy + radius * math.sin(angle)

    def draw_items(self):
        if self.animating and not self.generator: return
        self.calculate_targets()
        r = 20
        self.canvas.delete("item")
        
        for val, node in self.nodes.items():
            if not self.animating:
                node['x_cur'] = node['x_target']
                node['y_cur'] = node['y_target']
            x, y = node['x_cur'], node['y_cur']
            
            color = "#6366F1"
            if 'temp_color' in node: color = node['temp_color']
            
            node['circle'] = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, tags="item")
            node['text'] = self.canvas.create_text(x, y, text=str(val), fill="white", font=("Inter", 12, "bold"), tags="item")
            
            if 'dist_label' in node:
                self.canvas.create_text(x, y-25, text=node['dist_label'], fill="#FBBF24", font=("Inter", 10, "bold"), tags="item")
            
        self.redraw_edges()

    def redraw_edges(self, hl_edges=None, check_edge=None):
        hl_edges = hl_edges or []
        self.canvas.delete("edge")
        for u, v, w, directed in self.edges:
            if u in self.nodes and v in self.nodes:
                nu = self.nodes[u]
                nv = self.nodes[v]
                arr = tk.LAST if directed else tk.NONE
                
                ecolor = "white"
                ewid = 2
                
                if (u, v) in hl_edges or (v, u) in hl_edges:
                    ecolor = "#10B981"
                    ewid = 4
                elif check_edge and (check_edge == (u,v) or check_edge == (v,u)):
                    ecolor = "#EF4444"
                    ewid = 4

                self.canvas.create_line(nu['x_cur'], nu['y_cur'], nv['x_cur'], nv['y_cur'], fill=ecolor, width=ewid, arrow=arr, tags="edge")
                
                mx, my = (nu['x_cur'] + nv['x_cur'])/2, (nu['y_cur'] + nv['y_cur'])/2
                self.canvas.create_text(mx, my-12, text=str(w), fill="#10B981", font=("Inter", 12, "bold"), tags="edge")
        self.canvas.tag_lower("edge")

    def animate_graph(self):
        shifting = False
        speed = 5
        r = 20
        
        for node in self.nodes.values():
            for p_cur, p_tar in [('x_cur', 'x_target'), ('y_cur', 'y_target')]:
                diff = node[p_tar] - node[p_cur]
                if abs(diff) > speed:
                    node[p_cur] += speed if diff > 0 else -speed
                    shifting = True
                else:
                    node[p_cur] = node[p_tar]
                
            x, y = node['x_cur'], node['y_cur']
            self.canvas.coords(node['circle'], x-r, y-r, x+r, y+r)
            self.canvas.coords(node['text'], x, y)
            if 'dist_label' in node:
                self.canvas.delete("item")
                self.draw_items() 
            
        self.redraw_edges()
        if shifting:
            self.after(20, self.animate_graph)
        else:
            self.animating = False

    def add_vertex(self, val):
        if self.animating or not val: return
        self.animating = True
        self.model.add_vertex(val)
        
        if val not in self.nodes:
            r = 20
            cx, cy = self.width/2, self.height/2
            circle = self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#6366F1", tags="item")
            text = self.canvas.create_text(cx, cy, text=str(val), fill="white", font=("Inter", 12, "bold"), tags="item")
            self.nodes[val] = {'val': val, 'x_cur': cx, 'y_cur': cy, 'circle': circle, 'text': text}
            
        self.calculate_targets()
        self.animate_graph()
        self.set_explanation(f"Added new vertex '{val}'.")

    def add_edge(self, input_val, directed=False):
        if self.animating or not input_val: return
        parts = [p.strip() for p in input_val.replace(',', ' ').split() if p.strip()]
        if len(parts) >= 2:
            u, v = parts[0], parts[1]
            w = int(parts[2]) if len(parts) > 2 else 1
            self.model.add_edge(u, v, directed, w)
            if u not in self.nodes: self.add_vertex_instant(u)
            if v not in self.nodes: self.add_vertex_instant(v)
            if not any(eu == u and ev == v for eu,ev,ew,ed in self.edges):
                self.edges.append((u, v, w, directed))
            self.draw_items()
            self.set_explanation(f"Added edge from '{u}' to '{v}' with weight {w}.")

    def add_vertex_instant(self, val):
        self.model.add_vertex(val)
        r = 20
        cx, cy = self.width/2, self.height/2
        circle = self.canvas.create_oval(cx-r, cy-r, cx+r, cy+r, fill="#6366F1", tags="item")
        text = self.canvas.create_text(cx, cy, text=str(val), fill="white", font=("Inter", 12, "bold"), tags="item")
        self.nodes[val] = {'val': val, 'x_cur': cx, 'y_cur': cy, 'circle': circle, 'text': text}

    def reset_styles(self):
        self.canvas.delete("info_text")
        for node in self.nodes.values():
            if 'temp_color' in node: del node['temp_color']
            if 'dist_label' in node: del node['dist_label']
        self.set_explanation("")
        self.draw_items()

    def run_algo(self, algo_name, start_val=None):
        if self.animating: return
        self.reset_styles()
        self.animating = True
        
        if algo_name == "Dijkstra": self.generator = self.model.dijkstra(start_val)
        elif algo_name == "Bellman": self.generator = self.model.bellman_ford(start_val)
        elif algo_name == "Prim": self.generator = self.model.prim_mst()
        elif algo_name == "Kruskal": self.generator = self.model.kruskal_mst()
        
        self.animate_step()

    def animate_step(self):
        if not self.generator:
            self.animating = False
            self.draw_items()
            return
            
        try:
            state = next(self.generator)
            self.reset_styles()
            
            visited = state.get('visited', set())
            dist = state.get('dist', {})
            current = state.get('current')
            mst_edges = state.get('mst_edges', [])
            check_edge = state.get('edge')
            updated = state.get('updated')
            msg = state.get('msg', "")
            
            for v in visited:
                if v in self.nodes: self.nodes[v]['temp_color'] = "#8B5CF6"
            if current and current in self.nodes:
                self.nodes[current]['temp_color'] = "#F59E0B"
            if updated and updated in self.nodes:
                self.nodes[updated]['temp_color'] = "#10B981"
                
            for v, d in dist.items():
                if v in self.nodes:
                    self.nodes[v]['dist_label'] = f"d={d}" if d != float('inf') else "d=∞"
                    
            if msg:
                self.set_explanation(msg)
                
            self.draw_items()
            self.redraw_edges(hl_edges=mst_edges, check_edge=check_edge)
            
            self.after(self.delay, self.animate_step)
            
        except StopIteration:
            self.animating = False
            self.generator = None

    def traverse(self, start_val, mode="BFS"):
        if self.animating or not start_val or start_val not in self.nodes: return
        self.reset_styles()
        self.animating = True
        if mode == "BFS": steps = self.model.get_bfs_steps(start_val)
        else: steps = self.model.get_dfs_steps(start_val)
        
        self.animate_traversal(steps)

    def animate_traversal(self, steps):
        if not steps:
            self.animating = False
            for node in self.nodes.values():
                self.canvas.itemconfig(node['circle'], fill="#6366F1")
            self.canvas.delete("info_text")
            self.set_explanation("Traversal Loop Completed.")
            return
            
        visited_node, q_list, edge, msg = steps[0]
        
        if visited_node:
            node = self.nodes[visited_node]
            node['temp_color'] = "#F59E0B"
            self.draw_items()
            
        self.redraw_edges(check_edge=edge)
        self.set_explanation(msg)
            
        self.canvas.delete("info_text")
        q_str = "Collection Tracker: [" + ", ".join(q_list) + "]"
        self.canvas.create_text(20, 20, anchor=tk.W, text=q_str, fill="white", font=("Inter", 14), tags="info_text")
        
        self.after(2000, lambda: self.animate_traversal(steps[1:]))

    def search(self, val):
        if self.animating or not val: return
        if val not in self.nodes: return
        self.reset_styles()
        self.animating = True
        
        start_val = list(self.nodes.keys())[0]
        steps = self.model.get_bfs_steps(start_val)
        
        search_steps = []
        for step in steps:
            search_steps.append(step)
            if step[0] == val: break
            
        self.animate_search(search_steps, val)

    def animate_search(self, steps, target_val):
        if not steps:
            self.animating = False
            for node in self.nodes.values():
                self.canvas.itemconfig(node['circle'], fill="#6366F1")
            self.canvas.delete("info_text")
            self.set_explanation(f"Finished BFS search targeting '{target_val}'.")
            return
            
        visited_node, q_list, edge, msg = steps[0]
        if visited_node:
            node = self.nodes[visited_node]
            fill_color = "#10B981" if visited_node == target_val else "#EC4899"
            node['temp_color'] = fill_color
            self.draw_items()
            
        self.redraw_edges(check_edge=edge)
        self.set_explanation(msg)
            
        self.canvas.delete("info_text")
        q_str = "Search BFS Q: [" + ", ".join(q_list) + "]"
        self.canvas.create_text(20, 20, anchor=tk.W, text=q_str, fill="white", font=("Inter", 14), tags="info_text")
        
        self.after(2000, lambda: self.animate_search(steps[1:], target_val))

    def show_default_info(self):
        if self.app:
            self.app.update_info("O(V + E)", "O(V)", ["class Graph:", "    def add_vertex(self, v)...", "    def add_edge(self, u, v)...", "    def bfs_traverse(self)...", "    def dijkstra(self)..."], None)
