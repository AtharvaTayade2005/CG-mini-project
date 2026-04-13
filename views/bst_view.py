import tkinter as tk
from views.base_view import BaseView
from models.bst import BSTModel

class BSTView(BaseView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.model = BSTModel()
        self.nodes = {}

    def draw_base(self):
        pass

    def draw_items(self):
        if self.animating: return
        self.calculate_targets()
        r = 20
        self.canvas.delete("item")
        for val, node in self.nodes.items():
            node['x_cur'] = node['x_target']
            node['y_cur'] = node['y_target']
            x, y = node['x_cur'], node['y_cur']
            color = node.get('color', "#06B6D4") # Cyan default
            node['circle'] = self.canvas.create_oval(x-r, y-r, x+r, y+r, fill=color, tags="item")
            node['text'] = self.canvas.create_text(x, y, text=str(val), fill="white", font=("Inter", 12, "bold"), tags="item")
        self.redraw_lines()

    def get_edges(self):
        edges = []
        def traverse(n):
            if not n: return
            if n.left: edges.append((n.val, n.left.val))
            if n.right: edges.append((n.val, n.right.val))
            traverse(n.left)
            traverse(n.right)
        traverse(self.model.root)
        return edges

    def redraw_lines(self):
        self.canvas.delete("line")
        edges = self.get_edges()
        for p_val, c_val in edges:
            if p_val in self.nodes and c_val in self.nodes:
                p = self.nodes[p_val]
                c = self.nodes[c_val]
                self.canvas.create_line(p['x_cur'], p['y_cur'], c['x_cur'], c['y_cur'], fill="white", width=2, tags="line")
        self.canvas.tag_lower("line")

    def calculate_targets(self):
        inorder_nodes = []
        def traverse(node, depth):
            if not node: return
            traverse(node.left, depth + 1)
            inorder_nodes.append((node, depth))
            traverse(node.right, depth + 1)
            
        traverse(self.model.root, 0)
        
        if not inorder_nodes: return
        
        width_per_node = self.width / (len(inorder_nodes) + 1)
        r = 20
        
        for i, (n, depth) in enumerate(inorder_nodes):
            val = n.val
            x_tar = width_per_node * (i + 1)
            y_tar = 50 + depth * 70
            
            if val in self.nodes:
                self.nodes[val]['x_target'] = x_tar
                self.nodes[val]['y_target'] = y_tar
            else:
                x_start, y_start = self.width/2, -50
                circle = self.canvas.create_oval(x_start-r, y_start-r, x_start+r, y_start+r, fill="#06B6D4", tags="item")
                text = self.canvas.create_text(x_start, y_start, text=str(val), fill="white", font=("Inter", 12, "bold"), tags="item")
                self.nodes[val] = {
                    'val': val, 'x_cur': x_start, 'y_cur': y_start, 
                    'x_target': x_tar, 'y_target': y_tar, 
                    'circle': circle, 'text': text, 'color': "#06B6D4"
                }

    def insert(self, value):
        if self.animating or not value: return
        try: value = int(value)
        except ValueError: return
        if value in self.nodes: return # duplicate
            
        self.animating = True
        self.model.do_insert(value)
        self.calculate_targets()
        self.set_explanation(f"BST INSERT: Placing {value} by comparing left (smaller) or right (larger) at each node.")
        self.animate_tree()

    def delete(self, value):
        if self.animating or not value: return
        try: value = int(value)
        except ValueError: return
        if value not in self.nodes: return
        
        self.animating = True
        node = self.nodes.pop(value)
        node['y_target'] = self.height + 100
        
        self.model.do_delete(value)
        self.calculate_targets()
        self.set_explanation(f"BST DELETE: Removing node {value}. The tree restructures to maintain BST property.")
        self.animate_tree(extras=[node])
        
    def animate_tree(self, extras=None):
        if extras is None: extras = []
        shifting = False
        speed = 10
        r = 20
        
        all_animating_nodes = list(self.nodes.values()) + extras
        
        for node in all_animating_nodes:
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
            
        self.redraw_lines()
        
        if shifting:
            self.after(20, lambda: self.animate_tree(extras))
        else:
            for extra in extras:
                self.canvas.delete(extra['circle'])
                self.canvas.delete(extra['text'])
            self.animating = False

    def traverse(self, order="in"):
        if self.animating or not self.nodes: return
        self._reset_colors()
        self.animating = True
        if order == "in":
            vals = self.model.get_in_order()
            self.set_explanation("IN-ORDER traversal: Visit Left subtree, then Root, then Right subtree (gives sorted order).")
        elif order == "pre":
            vals = self.model.get_pre_order()
            self.set_explanation("PRE-ORDER traversal: Visit Root first, then Left subtree, then Right subtree.")
        else:
            vals = self.model.get_post_order()
            self.set_explanation("POST-ORDER traversal: Visit Left subtree, then Right subtree, then Root last.")
        self.animate_traversal(vals)

    def search(self, value):
        if self.animating or not value: return
        try: value = int(value)
        except: return
        
        path = self.model.get_search_path(value)
        if path:
            self._reset_colors()
            self.animating = True
            self.animate_search(path, target=value)
            
    def _reset_colors(self):
        for node in self.nodes.values():
            node['color'] = "#06B6D4"
            self.canvas.itemconfig(node['circle'], fill="#06B6D4")

    def animate_search(self, path, target):
        if not path:
            self.animating = False
            self.after(1000, self._reset_colors)
            return
            
        val = path.pop(0)
        node = self.nodes[val]
        
        if val == target:
            node['color'] = "#10B981" # Green if found
            self.set_explanation(f"FOUND! Node {val} matches target {target}. Search complete.")
        else:
            node['color'] = "#EF4444" # Red while searching
            self.set_explanation(f"Visiting node {val}. Target {target} is {'smaller, going LEFT.' if target < val else 'larger, going RIGHT.'}")
            
        self.canvas.itemconfig(node['circle'], fill=node['color'])
        self.after(1200, lambda: self.animate_search(path, target))

    def animate_traversal(self, vals):
        if not vals:
            self.animating = False
            return
            
        val = vals[0]
        node = self.nodes[val]
        self.canvas.itemconfig(node['circle'], fill="#FBBF24")
        self.set_explanation(f"Visiting node {val}.")
        self.after(800, lambda: self._finish_highlight(node, vals[1:]))

    def _finish_highlight(self, node, remaining):
        self.canvas.itemconfig(node['circle'], fill="#06B6D4")
        self.animate_traversal(remaining)

    def show_default_info(self):
        if self.app:
            self.app.update_info("O(log N)", "O(N)", ["class BST:", "    def insert(self, val)...", "    def delete(self, val)...", "    def search(self, val)...", "    def inorder(self)..."], None)
