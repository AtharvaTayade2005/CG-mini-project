import tkinter as tk
from views.base_view import BaseView
from models.array_algo import ArrayModel

class ArrayView(BaseView):
    def __init__(self, master, mode="sort", **kwargs):
        super().__init__(master, **kwargs)
        self.model = ArrayModel(15)
        self.mode = mode # 'sort' or 'search'
        self.generator = None
        self.delay = 1500 # Slowed down for learning

    def draw_base(self):
        self.canvas.delete("base")
        if self.width <= 1 or self.height <= 1:
            return

    def generate_new(self):
        if self.animating: return
        self.model.generate_new()
        self.draw_state({'arr': self.model.arr})
        self.set_explanation("Generated a new random array.")

    def load_custom_data(self, val):
        if self.animating: return
        self.model.set_arr(val)
        self.draw_state({'arr': self.model.arr})
        self.set_explanation("Loaded custom array data.")

    def draw_items(self):
        if self.animating: return
        self.draw_state({'arr': self.model.arr})

    def draw_state(self, state):
        self.canvas.delete("item")
        if self.width <= 1 or self.height <= 1:
            return

        arr = state.get('arr', [])
        if not arr: return

        n = len(arr)
        if n == 0: return

        max_val = max(arr) if max(arr) > 0 else 1
        
        # Colors
        default_color = "#3B82F6" # Blue
        compare_color = "#EF4444" # Red
        swap_color = "#FBBF24"    # Yellow
        sorted_color = "#10B981"  # Emerald Green
        pivot_color = "#8B5CF6"   # Purple
        
        compare_idx = state.get('compare', [])
        swap_idx = state.get('swap', [])
        sorted_idx = state.get('sorted', [])
        merged_idx = state.get('merged', [])
        pivot = state.get('pivot', -1)
        found_idx = state.get('found', -1)
        
        left_idx = state.get('left', -1)
        right_idx = state.get('right', -1)
        mid_idx = state.get('mid', -1)

        if self.mode == "sort":
            # Draw Histogram Bars
            padding = 40
            avail_width = self.width - 2 * padding
            bar_width = avail_width / n
            max_height = self.height - 120

            for i, val in enumerate(arr):
                x0 = padding + i * bar_width
                y0 = self.height - 60
                x1 = x0 + bar_width - 2 # 2px gap
                bar_h = (val / max_val) * max_height
                y1 = y0 - bar_h

                color = default_color
                if i in sorted_idx or i in merged_idx: color = sorted_color
                if i == pivot: color = pivot_color
                if i in compare_idx: color = compare_color
                if i in swap_idx: color = swap_color
                if i == found_idx: color = sorted_color

                self.canvas.create_rectangle(x0, y1, x1, y0, fill=color, outline="", tags="item")
                self.canvas.create_text((x0+x1)/2, y1 - 10, text=str(val), fill="white", font=("Inter", 10), tags="item")

        elif self.mode == "search":
            # Draw Horizontal Blocks
            padding = 50
            avail_width = self.width - 2 * padding
            box_width = min(avail_width / n, 60)
            start_x = self.width / 2 - (n * box_width) / 2
            y_center = self.height / 2 - 20
            
            for i, val in enumerate(arr):
                x0 = start_x + i * box_width
                y0 = y_center - 25
                x1 = x0 + box_width - 4
                y1 = y_center + 25

                color = default_color
                if i in compare_idx: color = compare_color
                if i == mid_idx: color = swap_color # Yellow mid
                if i == found_idx: color = sorted_color

                self.canvas.create_rectangle(x0, y0, x1, y1, fill=color, outline="#1E2336", width=2, tags="item")
                self.canvas.create_text((x0+x1)/2, y_center, text=str(val), fill="white", font=("Inter", 12, "bold"), tags="item")

                # Pointer labels
                label_y = y1 + 15
                if i == left_idx:
                    self.canvas.create_text((x0+x1)/2, label_y, text="L", fill="#EF4444", font=("Inter", 12, "bold"), tags="item")
                if i == right_idx:
                    self.canvas.create_text((x0+x1)/2, label_y + 15, text="R", fill="#EF4444", font=("Inter", 12, "bold"), tags="item")
                if i == mid_idx:
                    self.canvas.create_text((x0+x1)/2, y0 - 15, text="M", fill="#FBBF24", font=("Inter", 12, "bold"), tags="item")

    def run_algo(self, algo_name, target=None):
        if self.animating: return
        self.animating = True
        
        self.set_explanation(f"Initializing {algo_name}...")
        
        if algo_name == "Bubble": self.generator = self.model.bubble_sort()
        elif algo_name == "Insertion": self.generator = self.model.insertion_sort()
        elif algo_name == "Quick": self.generator = self.model.quick_sort()
        elif algo_name == "Merge": self.generator = self.model.merge_sort()
        elif algo_name == "Linear Search": self.generator = self.model.linear_search(int(target) if target else -1)
        elif algo_name == "Binary Search": self.generator = self.model.binary_search(int(target) if target else -1)

        self.animate_step()

    def animate_step(self):
        if not self.generator:
            self.animating = False
            return
            
        if getattr(self, 'is_paused', False) and not getattr(self, 'step_requested', False):
            self.after(100, self.animate_step)
            return
            
        self.step_requested = False
        
        try:
            state = next(self.generator)
            self.draw_state(state)
            if 'msg' in state:
                self.set_explanation(state['msg'])
            
            if self.app and 'code' in state:
                time_c = state.get('time_c', "O(?)")
                space_c = state.get('space_c', "O(?)")
                code = state.get('code', [])
                line = state.get('line', -1)
                self.app.update_info(time_c, space_c, code, line)

            actual_delay = int(self.delay / getattr(self, 'playback_speed', 1.0))
            self.after(actual_delay, self.animate_step)
        except StopIteration:
            self.animating = False
            self.generator = None

    def show_default_info(self):
        if self.app:
            mode_text = "Sorting Algorithm" if self.mode == "sort" else "Search Algorithm"
            self.app.update_info("?", "?", [f"Select a {mode_text} below", "to display its live code tracing."], None)
