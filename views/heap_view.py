import math
import tkinter as tk
from views.base_view import BaseView
from models.heap import HeapModel

class HeapView(BaseView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.model = HeapModel(is_min=True)
        self.nodes = []

    def get_array_coords(self, idx):
        x = 50 + idx * 50 + 25
        y = self.height - 40
        return x, y

    def get_tree_coords(self, idx):
        if idx == 0:
            return self.width / 2, 40
        level = int(math.log2(idx + 1))
        parts = 2**(level + 1)
        pos = idx - (2**level - 1)
        x_mult = 1 + 2 * pos
        x = (self.width / parts) * x_mult
        y = 40 + level * 60
        return x, y

    def draw_base(self):
        pass

    def draw_items(self):
        if self.animating: return
        self.canvas.delete("item")
        self.canvas.delete("line")
        if self.width <= 1 or self.height <= 1:
            return
            
        r = 20
        for i, node in enumerate(self.nodes):
            ax, ay = self.get_array_coords(i)
            tx, ty = self.get_tree_coords(i)
            
            node['arr_x'] = node['arr_x_t'] = ax
            node['arr_y'] = node['arr_y_t'] = ay
            node['tr_x'] = node['tr_x_t'] = tx
            node['tr_y'] = node['tr_y_t'] = ty
            
            node['arr_rect'] = self.canvas.create_rectangle(ax-r, ay-r, ax+r, ay+r, fill="#8B5CF6", tags="item")
            node['arr_text'] = self.canvas.create_text(ax, ay, text=str(node['val']), fill="white", font=("Inter", 12, "bold"), tags="item")
            
            node['tr_circle'] = self.canvas.create_oval(tx-r, ty-r, tx+r, ty+r, fill="#7C3AED", tags="item")
            node['tr_text'] = self.canvas.create_text(tx, ty, text=str(node['val']), fill="white", font=("Inter", 12, "bold"), tags="item")
        
        self.draw_lines()

    def draw_lines(self):
        self.canvas.delete("line")
        for i in range(len(self.nodes)):
            left = 2 * i + 1
            right = 2 * i + 2
            parent = self.nodes[i]
            if left < len(self.nodes):
                child = self.nodes[left]
                self.canvas.create_line(parent['tr_x'], parent['tr_y'], child['tr_x'], child['tr_y'], fill="white", tags="line")
            if right < len(self.nodes):
                child = self.nodes[right]
                self.canvas.create_line(parent['tr_x'], parent['tr_y'], child['tr_x'], child['tr_y'], fill="white", tags="line")
        self.canvas.tag_lower("line")

    def insert(self, value):
        if self.animating or not value: return
        try:
            value = int(value)
        except ValueError:
            return
            
        self.animating = True
        swaps = self.model.insert(value)
        
        idx = len(self.nodes)
        ax, ay = self.get_array_coords(idx)
        tx, ty = self.get_tree_coords(idx)
        
        r = 20
        arr_rect = self.canvas.create_rectangle(ax-r, ay-r, ax+r, ay+r, fill="#8B5CF6", tags="item")
        arr_text = self.canvas.create_text(ax, ay, text=str(value), fill="white", font=("Inter", 12, "bold"), tags="item")
        
        tr_circle = self.canvas.create_oval(tx-r, ty-r, tx+r, ty+r, fill="#7C3AED", tags="item")
        tr_text = self.canvas.create_text(tx, ty, text=str(value), fill="white", font=("Inter", 12, "bold"), tags="item")
        
        node = {
            'val': value,
            'arr_rect': arr_rect, 'arr_text': arr_text,
            'tr_circle': tr_circle, 'tr_text': tr_text,
            'arr_x': ax, 'arr_y': ay, 'arr_x_t': ax, 'arr_y_t': ay,
            'tr_x': tx, 'tr_y': ty, 'tr_x_t': tx, 'tr_y_t': ty
        }
        self.nodes.append(node)
        self.draw_lines()
        
        self.set_explanation(f"HEAP INSERT: Added {value} at bottom. Now performing Heapify-Up to maintain heap property.")
        self.after(500, lambda: self.animate_swaps(swaps, None))

    def extract(self):
        if self.animating or len(self.nodes) == 0: return
        self.animating = True
        val, swaps = self.model.extract()
        
        if len(self.nodes) == 1:
            n = self.nodes.pop()
            self.canvas.delete(n['arr_rect'], n['arr_text'], n['tr_circle'], n['tr_text'])
            self.draw_lines()
            self.animating = False
            self.set_explanation(f"EXTRACT: Removed root {val}. Heap is now empty.")
            return
            
        old_root = self.nodes[0]
        self.canvas.delete(old_root['arr_rect'], old_root['arr_text'], old_root['tr_circle'], old_root['tr_text'])
        
        last_node = self.nodes.pop()
        self.nodes[0] = last_node
        
        last_node['arr_x_t'], last_node['arr_y_t'] = self.get_array_coords(0)
        last_node['tr_x_t'], last_node['tr_y_t'] = self.get_tree_coords(0)
        
        self.set_explanation(f"EXTRACT: Removed root {val}. Last element {last_node['val']} moves to root. Now Heapifying-Down.")
        self._move_to_target(last_node, lambda: self.animate_swaps(swaps, None))

    def _move_to_target(self, node, callback):
        speed = 10
        moving = False
        for p_cur, p_tar in [('arr_x', 'arr_x_t'), ('arr_y', 'arr_y_t'), ('tr_x', 'tr_x_t'), ('tr_y', 'tr_y_t')]:
            if abs(node[p_cur] - node[p_tar]) > speed:
                node[p_cur] += speed if node[p_cur] < node[p_tar] else -speed
                moving = True
            else:
                node[p_cur] = node[p_tar]
                
        r = 20
        self.canvas.coords(node['arr_rect'], node['arr_x']-r, node['arr_y']-r, node['arr_x']+r, node['arr_y']+r)
        self.canvas.coords(node['arr_text'], node['arr_x'], node['arr_y'])
        self.canvas.coords(node['tr_circle'], node['tr_x']-r, node['tr_y']-r, node['tr_x']+r, node['tr_y']+r)
        self.canvas.coords(node['tr_text'], node['tr_x'], node['tr_y'])
        self.draw_lines()
        
        if moving:
            self.after(20, lambda: self._move_to_target(node, callback))
        else:
            if callback: callback()

    def animate_swaps(self, swaps, callback):
        if not swaps:
            self.animating = False
            self.draw_items()
            if callback: callback()
            return
            
        i, j = swaps[0]
        swaps = swaps[1:]
        
        node_i = self.nodes[i]
        node_j = self.nodes[j]
        self.nodes[i], self.nodes[j] = self.nodes[j], self.nodes[i]
        
        node_i['arr_x_t'], node_i['arr_y_t'] = self.get_array_coords(j)
        node_i['tr_x_t'], node_i['tr_y_t'] = self.get_tree_coords(j)
        
        node_j['arr_x_t'], node_j['arr_y_t'] = self.get_array_coords(i)
        node_j['tr_x_t'], node_j['tr_y_t'] = self.get_tree_coords(i)
        
        self.set_explanation(f"HEAP SWAP: Swapping {node_i['val']} (index {i}) with {node_j['val']} (index {j}) to maintain heap ordering.")
        self._do_animate_step(node_i, node_j, swaps, callback)
        
    def _do_animate_step(self, node_i, node_j, swaps, callback):
        speed = 10
        moving = False
        for node in (node_i, node_j):
            for p_cur, p_tar in [('arr_x', 'arr_x_t'), ('arr_y', 'arr_y_t'), ('tr_x', 'tr_x_t'), ('tr_y', 'tr_y_t')]:
                if abs(node[p_cur] - node[p_tar]) > speed:
                    node[p_cur] += speed if node[p_cur] < node[p_tar] else -speed
                    moving = True
                else:
                    node[p_cur] = node[p_tar]
            
            r = 20
            self.canvas.coords(node['arr_rect'], node['arr_x']-r, node['arr_y']-r, node['arr_x']+r, node['arr_y']+r)
            self.canvas.coords(node['arr_text'], node['arr_x'], node['arr_y'])
            self.canvas.coords(node['tr_circle'], node['tr_x']-r, node['tr_y']-r, node['tr_x']+r, node['tr_y']+r)
            self.canvas.coords(node['tr_text'], node['tr_x'], node['tr_y'])

        self.draw_lines()
        
        if moving:
            self.after(20, lambda: self._do_animate_step(node_i, node_j, swaps, callback))
        else:
            self.animate_swaps(swaps, callback)

    def traverse(self, order="in"):
        if self.animating or not self.nodes: return
        self.animating = True
        if order == "in":
            indices = self.model.get_in_order()
            self.set_explanation("IN-ORDER Heap Traversal: Left Child → Root → Right Child recursively on the tree representation.")
        elif order == "pre":
            indices = self.model.get_pre_order()
            self.set_explanation("PRE-ORDER Heap Traversal: Root → Left Child → Right Child recursively.")
        else:
            indices = self.model.get_post_order()
            self.set_explanation("POST-ORDER Heap Traversal: Left Child → Right Child → Root recursively.")
        self.animate_traversal(indices)

    def animate_traversal(self, indices):
        if not indices:
            self.animating = False
            return
            
        idx = indices[0]
        node = self.nodes[idx]
        
        self.canvas.itemconfig(node['tr_circle'], fill="#FBBF24")
        self.canvas.itemconfig(node['arr_rect'], fill="#FBBF24")
        
        self.after(500, lambda: self._finish_highlight(node, indices[1:]))

    def _finish_highlight(self, node, remaining):
        self.canvas.itemconfig(node['tr_circle'], fill="#7C3AED")
        self.canvas.itemconfig(node['arr_rect'], fill="#8B5CF6")
        self.animate_traversal(remaining)

    def show_default_info(self):
        if self.app:
            self.app.update_info("O(log N)", "O(N)", ["class MinHeap:", "    def __init__(self):", "        self.heap = []", "    def insert(self, val)...", "    def extract_min(self)..."], None)
