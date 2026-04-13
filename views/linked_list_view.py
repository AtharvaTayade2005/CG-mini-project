import tkinter as tk
from views.base_view import BaseView
from models.linked_list import LinkedListModel

class LinkedListView(BaseView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.model = LinkedListModel()
        self.nodes = []

    def draw_base(self):
        pass

    def draw_items(self):
        if self.animating: return
        self.canvas.delete("item")
        self.canvas.delete("line")
        if self.width <= 1 or self.height <= 1:
            return
            
        y_center = self.height / 2
        start_x = 50
        gap = 40
        rect_width = 80
        rect_height = 40
        
        for i, node in enumerate(self.nodes):
            x_pos = start_x + i * (rect_width + gap)
            node['x_cur'] = x_pos
            node['x_target'] = x_pos
            node['y_cur'] = y_center
            node['y_target'] = y_center
            
            node['rect_id'] = self.canvas.create_rectangle(
                x_pos, y_center - rect_height/2, 
                x_pos + rect_width, y_center + rect_height/2, 
                fill="#10B981", tags="item"
            )
            node['text_id'] = self.canvas.create_text(
                x_pos + rect_width/2, y_center, 
                text=str(node['val']), fill="white", font=("Inter", 12, "bold"), tags="item"
            )
        self.redraw_lines()

    def redraw_lines(self):
        self.canvas.delete("line")
        rect_width = 80
        for i in range(len(self.nodes) - 1):
            curr = self.nodes[i]
            nxt = self.nodes[i+1]
            self.canvas.create_line(
                curr['x_cur'] + rect_width, curr['y_cur'], 
                nxt['x_cur'], nxt['y_cur'], 
                arrow=tk.LAST, fill="white", width=2, tags="line"
            )

    def insert_tail(self, value):
        if self.animating or not value: return
        self.animating = True
        self.model.insert_tail(value)
        
        y_center = self.height / 2
        rect_width = 80
        rect_height = 40
        gap = 40
        start_x = 50
        
        x_target = start_x + len(self.nodes) * (rect_width + gap)
        y_start = -50
        
        rect_id = self.canvas.create_rectangle(
            x_target, y_start - rect_height/2, 
            x_target + rect_width, y_start + rect_height/2, 
            fill="#10B981", tags="item"
        )
        text_id = self.canvas.create_text(
            x_target + rect_width/2, y_start, 
            text=str(value), fill="white", font=("Inter", 12, "bold"), tags="item"
        )
        
        new_node = {
            'val': value,
            'rect_id': rect_id,
            'text_id': text_id,
            'x_cur': x_target,
            'x_target': x_target,
            'y_cur': y_start,
            'y_target': y_center
        }
        self.nodes.append(new_node)
        self.set_explanation(f"INSERT TAIL: Appending '{value}' at the end. The previous tail's 'next' pointer now links to this new node.")
        
        if self.app:
            self.app.update_info("O(N)", "O(1)", 
                ["def insert_tail(head, val):", "    new_node = Node(val)", "    if not head: return new_node", "    curr = head", "    while curr.next: curr = curr.next", "    curr.next = new_node"], 5)

        self.animate_insert(new_node)

    def insert_head(self, value):
        if self.animating or not value: return
        self.animating = True
        self.model.insert_head(value)
        
        y_center = self.height / 2
        rect_width = 80
        gap = 40
        start_x = 50
        
        for i, node in enumerate(self.nodes):
            node['x_target'] = start_x + (i + 1) * (rect_width + gap)
            
        x_target = start_x
        y_start = -50
        
        rect_id = self.canvas.create_rectangle(
            x_target, y_start - 20, 
            x_target + rect_width, y_start + 20, 
            fill="#10B981", tags="item"
        )
        text_id = self.canvas.create_text(
            x_target + rect_width/2, y_start, 
            text=str(value), fill="white", font=("Inter", 12, "bold"), tags="item"
        )
        
        new_node = {
            'val': value,
            'rect_id': rect_id,
            'text_id': text_id,
            'x_cur': x_target,
            'x_target': x_target,
            'y_cur': y_start,
            'y_target': y_center
        }
        self.nodes.insert(0, new_node)
        self.set_explanation(f"INSERT HEAD: Adding '{value}' at the front. The new node's 'next' pointer links to the old head.")
        
        if self.app:
            self.app.update_info("O(1)", "O(1)", 
                ["def insert_head(head, val):", "    new_node = Node(val)", "    new_node.next = head", "    head = new_node", "    return head"], 3)

        self.animate_shift_then_insert(new_node)

    def animate_insert(self, item):
        speed = 20
        rect_width = 80
        rect_height = 40
        
        if item['y_cur'] < item['y_target']:
            item['y_cur'] = min(item['y_cur'] + speed, item['y_target'])
            self.canvas.coords(
                item['rect_id'], 
                item['x_cur'], item['y_cur'] - rect_height/2, 
                item['x_cur'] + rect_width, item['y_cur'] + rect_height/2
            )
            self.canvas.coords(item['text_id'], item['x_cur'] + rect_width/2, item['y_cur'])
            
            self.redraw_lines()
            self.after(20, lambda: self.animate_insert(item))
        else:
            self.animating = False
            self.redraw_lines()

    def animate_shift_then_insert(self, insert_item):
        shifting = False
        speed = 15
        rect_width = 80
        rect_height = 40
        
        for node in self.nodes:
            if node == insert_item: continue
            if node['x_cur'] < node['x_target']:
                node['x_cur'] = min(node['x_cur'] + speed, node['x_target'])
                self.canvas.coords(
                    node['rect_id'], 
                    node['x_cur'], node['y_cur'] - rect_height/2, 
                    node['x_cur'] + rect_width, node['y_cur'] + rect_height/2
                )
                self.canvas.coords(node['text_id'], node['x_cur'] + rect_width/2, node['y_cur'])
                shifting = True

        self.redraw_lines()
        
        if shifting:
            self.after(20, lambda: self.animate_shift_then_insert(insert_item))
        else:
            self.animate_insert(insert_item)

    def delete_head(self):
        if self.animating or len(self.nodes) == 0: return
        self.animating = True
        self.model.delete_head()
        
        node = self.nodes.pop(0)
        node['y_target'] = self.height + 100
        self.set_explanation(f"DELETE HEAD: Removing '{node['val']}'. The head pointer now shifts to the next node.")
        
        if self.app:
            self.app.update_info("O(1)", "O(1)", 
                ["def delete_head(head):", "    if not head: return None", "    return head.next"], 2)

        self.animate_delete_then_shift(node)
        
    def delete_tail(self):
        if self.animating or len(self.nodes) == 0: return
        self.animating = True
        self.model.delete_tail()
        
        node = self.nodes.pop()
        node['y_target'] = self.height + 100
        self.set_explanation(f"DELETE TAIL: Removing last node '{node['val']}'. The previous node's 'next' pointer becomes NULL.")
        
        if self.app:
            self.app.update_info("O(N)", "O(1)", 
                ["def delete_tail(head):", "    if not head or not head.next: return None", "    curr = head", "    while curr.next.next: curr = curr.next", "    curr.next = None", "    return head"], 4)

        self.animate_delete(node)

    def animate_delete(self, node):
        speed = 20
        rect_width = 80
        rect_height = 40
        if node['y_cur'] < node['y_target']:
            node['y_cur'] += speed
            self.canvas.coords(
                node['rect_id'], 
                node['x_cur'], node['y_cur'] - rect_height/2, 
                node['x_cur'] + rect_width, node['y_cur'] + rect_height/2
            )
            self.canvas.coords(node['text_id'], node['x_cur'] + rect_width/2, node['y_cur'])
            self.redraw_lines()
            self.after(20, lambda: self.animate_delete(node))
        else:
            self.canvas.delete(node['rect_id'])
            self.canvas.delete(node['text_id'])
            self.animating = False

    def animate_delete_then_shift(self, node):
        speed = 20
        rect_width = 80
        rect_height = 40
        if node['y_cur'] < node['y_target']:
            node['y_cur'] += speed
            self.canvas.coords(
                node['rect_id'], 
                node['x_cur'], node['y_cur'] - rect_height/2, 
                node['x_cur'] + rect_width, node['y_cur'] + rect_height/2
            )
            self.canvas.coords(node['text_id'], node['x_cur'] + rect_width/2, node['y_cur'])
            self.redraw_lines()
            self.after(20, lambda: self.animate_delete_then_shift(node))
        else:
            self.canvas.delete(node['rect_id'])
            self.canvas.delete(node['text_id'])
            
            start_x = 50
            gap = 40
            for i, n in enumerate(self.nodes):
                n['x_target'] = start_x + i * (rect_width + gap)
                
            self.animate_shift()
            
    def animate_shift(self):
        shifting = False
        speed = 15
        rect_width = 80
        rect_height = 40
        
        for node in self.nodes:
            if node['x_cur'] > node['x_target']:
                node['x_cur'] = max(node['x_cur'] - speed, node['x_target'])
                self.canvas.coords(
                    node['rect_id'], 
                    node['x_cur'], node['y_cur'] - rect_height/2, 
                    node['x_cur'] + rect_width, node['y_cur'] + rect_height/2
                )
                self.canvas.coords(node['text_id'], node['x_cur'] + rect_width/2, node['y_cur'])
                shifting = True

        self.redraw_lines()
        
        if shifting:
            self.after(20, self.animate_shift)
        else:
            self.animating = False

    def show_default_info(self):
        if self.app:
            self.app.update_info("O(1) / O(N)", "O(N)", ["class LinkedListNode:", "    def __init__(self, val):", "        self.val = val", "        self.next = None", "", "class LinkedList:", "    def insert_head(self)...", "    def insert_tail(self)..."], None)
