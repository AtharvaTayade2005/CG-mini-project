import tkinter as tk
from views.base_view import BaseView
from models.queue import QueueModel

class QueueView(BaseView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.model = QueueModel()
        self.rects = [] # stores {'val', 'rect_id', 'text_id', 'x_cur', 'x_target'}

    def draw_base(self):
        self.canvas.delete("base")
        if self.width <= 1 or self.height <= 1:
            return
            
        y_center = self.height / 2
        lane_height = 80
        self.canvas.create_line(50, y_center - lane_height/2, self.width - 50, y_center - lane_height/2, fill="white", width=4, tags="base")
        self.canvas.create_line(50, y_center + lane_height/2, self.width - 50, y_center + lane_height/2, fill="white", width=4, tags="base")

    def draw_items(self):
        if self.animating: return
        self.canvas.delete("item")
        if self.width <= 1 or self.height <= 1:
            return
            
        y_center = self.height / 2
        rect_width = 80
        rect_height = 60
        gap = 10
        start_x = self.width - 60 - rect_width
        
        for i, item in enumerate(self.rects):
            x_target = start_x - i * (rect_width + gap)
            item['x_cur'] = x_target
            item['x_target'] = x_target
            
            item['rect_id'] = self.canvas.create_rectangle(
                x_target, y_center - rect_height/2, 
                x_target + rect_width, y_center + rect_height/2, 
                fill="#F59E0B", tags="item"
            )
            item['text_id'] = self.canvas.create_text(
                x_target + rect_width/2, y_center, 
                text=str(item['val']), fill="white", font=("Inter", 14, "bold"), tags="item"
            )

    def enqueue(self, value):
        if self.animating: return
        if not value: return
        
        self.animating = True
        self.model.enqueue(value)
        
        y_center = self.height / 2
        rect_width = 80
        rect_height = 60
        gap = 10
        
        x_start = -100 # enter from left side
        x_target = self.width - 60 - rect_width - len(self.rects) * (rect_width + gap)
        
        rect_id = self.canvas.create_rectangle(
            x_start, y_center - rect_height/2, 
            x_start + rect_width, y_center + rect_height/2, 
            fill="#F59E0B", tags="item"
        )
        text_id = self.canvas.create_text(
            x_start + rect_width/2, y_center, 
            text=str(value), fill="white", font=("Inter", 14, "bold"), tags="item"
        )
        
        new_item = {
            'val': value,
            'rect_id': rect_id,
            'text_id': text_id,
            'x_cur': x_start,
            'x_target': x_target
        }
        self.rects.append(new_item)
        self.set_explanation(f"ENQUEUE: Adding '{value}' to the rear of the queue. Queue follows FIFO (First In, First Out).")
        
        if self.app:
            self.app.update_info("O(1)", "O(N)", 
                ["def enqueue(queue, item):", "    queue.append(item)"], 1)

        self.animate_enqueue(new_item)

    def animate_enqueue(self, item):
        speed = 10
        rect_width = 80
        rect_height = 60
        y_center = self.height / 2
        
        if item['x_cur'] < item['x_target']:
            item['x_cur'] = min(item['x_cur'] + speed, item['x_target'])
            self.canvas.coords(
                item['rect_id'], 
                item['x_cur'], y_center - rect_height/2, 
                item['x_cur'] + rect_width, y_center + rect_height/2
            )
            self.canvas.coords(item['text_id'], item['x_cur'] + rect_width/2, y_center)
            
            self.after(20, lambda: self.animate_enqueue(item))
        else:
            self.animating = False
            self.set_explanation(f"ENQUEUE complete. '{item['val']}' is now in the queue. Size: {len(self.rects)}.")

    def dequeue(self):
        if self.animating or len(self.rects) == 0: return
        
        self.animating = True
        self.model.dequeue()
        
        popped_item = self.rects.pop(0)
        popped_item['x_target'] = self.width + 100 # leave left to right
        
        self.set_explanation(f"DEQUEUE: Removing front element '{popped_item['val']}' from the queue (FIFO — it was first in).")
        
        if self.app:
            self.app.update_info("O(N)", "O(1)", 
                ["def dequeue(queue):", "    if not queue.is_empty():", "        return queue.pop(0)"], 2)

        self.animate_dequeue(popped_item)

    def animate_dequeue(self, item):
        speed = 10
        rect_width = 80
        rect_height = 60
        y_center = self.height / 2
        
        if item['x_cur'] < item['x_target']:
            item['x_cur'] += speed
            self.canvas.coords(
                item['rect_id'], 
                item['x_cur'], y_center - rect_height/2, 
                item['x_cur'] + rect_width, y_center + rect_height/2
            )
            self.canvas.coords(item['text_id'], item['x_cur'] + rect_width/2, y_center)
            self.after(20, lambda: self.animate_dequeue(item))
        else:
            self.canvas.delete(item['rect_id'])
            self.canvas.delete(item['text_id'])
            
            self.shift_all_items()

    def shift_all_items(self):
        gap = 10
        rect_width = 80
        start_x = self.width - 60 - rect_width
        for i, item in enumerate(self.rects):
            item['x_target'] = start_x - i * (rect_width + gap)
            
        self.animate_shift()

    def animate_shift(self):
        shifting = False
        speed = 10
        rect_width = 80
        rect_height = 60
        y_center = self.height / 2
        
        for item in self.rects:
            if item['x_cur'] < item['x_target']:
                item['x_cur'] = min(item['x_cur'] + speed, item['x_target'])
                self.canvas.coords(
                    item['rect_id'], 
                    item['x_cur'], y_center - rect_height/2, 
                    item['x_cur'] + rect_width, y_center + rect_height/2
                )
                self.canvas.coords(item['text_id'], item['x_cur'] + rect_width/2, y_center)
                shifting = True
                
        if shifting:
            self.after(20, self.animate_shift)
        else:
            self.animating = False
            front = self.rects[0]['val'] if self.rects else 'None'
            self.set_explanation(f"DEQUEUE complete. Remaining elements shifted forward. Front is now: {front}. Size: {len(self.rects)}.")

    def show_default_info(self):
        if self.app:
            self.app.update_info("O(1)", "O(N)", ["class Queue:", "    def __init__(self):", "        self.items = []", "    def enqueue(self, item)...", "    def dequeue(self)..."], None)
