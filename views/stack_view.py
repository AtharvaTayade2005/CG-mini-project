import tkinter as tk
from views.base_view import BaseView
from models.stack import StackModel

class StackView(BaseView):
    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.model = StackModel()
        self.rects = []

    def draw_base(self):
        self.canvas.delete("base")
        if self.width <= 1 or self.height <= 1:
            return
            
        x_center = self.width / 2
        rect_width = 120
        # Draw the "bucket" of the stack
        self.canvas.create_line(x_center - rect_width/2, self.height - 45, x_center + rect_width/2, self.height - 45, fill="white", width=4, tags="base")
        self.canvas.create_line(x_center - rect_width/2, self.height - 45, x_center - rect_width/2, 50, fill="white", width=4, tags="base")
        self.canvas.create_line(x_center + rect_width/2, self.height - 45, x_center + rect_width/2, 50, fill="white", width=4, tags="base")

    def draw_items(self):
        if self.animating:
            return
        self.canvas.delete("item")
        if self.width <= 1 or self.height <= 1:
            return
            
        x_center = self.width / 2
        rect_width = 100
        rect_height = 40
        
        for i, item in enumerate(self.rects):
            y_target = self.height - 50 - i * (rect_height + 5)
            # update tracking
            item['y_cur'] = y_target
            item['y_target'] = y_target
            item['rect_id'] = self.canvas.create_rectangle(
                x_center - rect_width/2, y_target - rect_height, 
                x_center + rect_width/2, y_target, 
                fill="#3B82F6", tags="item"
            )
            item['text_id'] = self.canvas.create_text(
                x_center, y_target - rect_height/2, text=str(item['val']), fill="white", font=("Inter", 14, "bold"), tags="item"
            )

    def push(self, value):
        if self.animating: return
        if not value: return # Ignore empty
        
        self.animating = True
        self.model.push(value)
        
        x_center = self.width / 2
        rect_width = 100
        rect_height = 40
        y_start = 10
        
        rect_id = self.canvas.create_rectangle(
            x_center - rect_width/2, y_start - rect_height, 
            x_center + rect_width/2, y_start, 
            fill="#3B82F6", tags="item"
        )
        text_id = self.canvas.create_text(
            x_center, y_start - rect_height/2, text=str(value), fill="white", font=("Inter", 14, "bold"), tags="item"
        )
        
        y_target = self.height - 50 - (len(self.rects)) * (rect_height + 5)
        
        new_item = {
            'val': value, 
            'rect_id': rect_id, 
            'text_id': text_id, 
            'y_cur': y_start, 
            'y_target': y_target
        }
        self.rects.append(new_item)
        
        self.set_explanation(f"PUSH: Placing '{value}' on top of the stack. Stack follows LIFO (Last In, First Out).")
        self.animate_push(new_item)

    def animate_push(self, item):
        speed = 8
        rect_height = 40
        x_center = self.width / 2
        rect_width = 100

        if item['y_cur'] < item['y_target']:
            item['y_cur'] = min(item['y_cur'] + speed, item['y_target'])
            
            self.canvas.coords(
                item['rect_id'], 
                x_center - rect_width/2, item['y_cur'] - rect_height, 
                x_center + rect_width/2, item['y_cur']
            )
            self.canvas.coords(item['text_id'], x_center, item['y_cur'] - rect_height/2)
            
            self.after(20, lambda: self.animate_push(item))
        else:
            self.animating = False
            self.set_explanation(f"PUSH complete. '{item['val']}' is now the top of the stack. Size: {len(self.rects)}.")

    def pop(self):
        if self.animating or len(self.rects) == 0: return
        
        self.animating = True
        self.model.pop()
        
        item = self.rects.pop()
        item['y_target'] = 10 # Animate back to top
        
        self.set_explanation(f"POP: Removing top element '{item['val']}' from the stack (LIFO).")
        self.animate_pop(item)

    def animate_pop(self, item):
        speed = 8
        rect_height = 40
        x_center = self.width / 2
        rect_width = 100

        if item['y_cur'] > item['y_target']:
            item['y_cur'] = max(item['y_cur'] - speed, item['y_target'])
            
            self.canvas.coords(
                item['rect_id'], 
                x_center - rect_width/2, item['y_cur'] - rect_height, 
                x_center + rect_width/2, item['y_cur']
            )
            self.canvas.coords(item['text_id'], x_center, item['y_cur'] - rect_height/2)
            
            self.after(20, lambda: self.animate_pop(item))
        else:
            self.canvas.delete(item['rect_id'])
            self.canvas.delete(item['text_id'])
            self.animating = False
            top_val = self.rects[-1]['val'] if self.rects else 'None'
            self.set_explanation(f"POP complete. New top element: {top_val}. Size: {len(self.rects)}.")
