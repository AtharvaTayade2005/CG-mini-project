import tkinter as tk
from views.base_view import BaseView
from models.dp_greedy import DPGreedyModel

class DPGreedyView(BaseView):
    def __init__(self, master, mode="lcs", **kwargs):
        super().__init__(master, **kwargs)
        self.model = DPGreedyModel()
        self.mode = mode # 'frac', '01', 'lcs'
        self.generator = None
        self.delay = 1800 # Slow enough to read explanations

    def draw_base(self):
        self.canvas.delete("base")

    def draw_items(self):
        pass # Drawn via state animation mostly

    def draw_grid(self, state, title="DP Table"):
        self.canvas.delete("item")
        dp = state.get('dp', [])
        if not dp: return
        
        rows = len(dp)
        cols = len(dp[0])
        
        # cell sizes — make wider to avoid text overlap
        cell_w = min(55, (self.width - 150) // max(cols, 1))
        cell_h = min(40, (self.height - 150) // max(rows, 1))
        
        start_x = self.width / 2 - (cols * cell_w) / 2
        start_y = 95

        self.canvas.create_text(self.width/2, 55, text=title, fill="white", font=("Inter", 16, "bold"), tags="item")

        active_i = state.get('i', -1)
        active_j = state.get('w', state.get('j', -1))
        path = state.get('path', [])
        
        s1 = state.get('s1', "")
        s2 = state.get('s2', "")
        
        # Draw column headers for LCS
        if self.mode == "lcs" and s2:
            for j in range(len(s2)):
                self.canvas.create_text(start_x + (j+1)*cell_w + cell_w/2, start_y - 12, text=s2[j], fill="#F59E0B", font=("Inter", 11, "bold"), tags="item")
        
        # Draw column headers for 0/1 Knapsack (capacity values)
        if self.mode == "01":
            cap = state.get('capacity', cols - 1)
            for j in range(cols):
                self.canvas.create_text(start_x + j*cell_w + cell_w/2, start_y - 12, text=str(j), fill="#A0AEC0", font=("Inter", 9), tags="item")
        
        # Draw row headers
        if self.mode == "lcs" and s1:
            for i in range(len(s1)):
                self.canvas.create_text(start_x - 15, start_y + (i+1)*cell_h + cell_h/2, text=s1[i], fill="#F59E0B", font=("Inter", 11, "bold"), tags="item")
        elif self.mode == "01":
            weights = state.get('weights', [])
            values = state.get('values', [])
            for i in range(1, rows):
                label = f"W{weights[i-1]}"
                self.canvas.create_text(start_x - 22, start_y + i*cell_h + cell_h/2, text=label, fill="#A0AEC0", font=("Inter", 9), tags="item")
                
        for i in range(rows):
            for j in range(cols):
                x0 = start_x + j * cell_w
                y0 = start_y + i * cell_h
                x1 = x0 + cell_w
                y1 = y0 + cell_h
                
                bg = "#1E2336" # Default dark blueish
                text_col = "white"
                
                # Colors
                if i == active_i and j == active_j:
                    bg = "#EF4444" if state['type'] == 'calc' else "#10B981"
                elif (i, j) in path:
                    bg = "#3B82F6"
                    
                self.canvas.create_rectangle(x0, y0, x1, y1, fill=bg, outline="#2A2F45", tags="item")
                self.canvas.create_text((x0+x1)/2, (y0+y1)/2, text=str(dp[i][j]), fill=text_col, font=("Inter", 11), width=cell_w-4, tags="item")

    def draw_frac(self, state):
        self.canvas.delete("item")
        items = state.get('items', [])
        capacity = state.get('capacity', 0)
        rem = state.get('rem', capacity)
        taken = state.get('taken', [])
        current = state.get('current', -1)
        
        # Draw main capacity bar
        padding = 50
        bar_w = self.width - 2 * padding
        x0 = padding
        y0 = 110
        x1 = x0 + bar_w
        y1 = y0 + 40
        
        fill_ratio = (capacity - rem) / capacity if capacity > 0 else 0
        fill_x = x0 + bar_w * fill_ratio
        
        self.canvas.create_text(self.width/2, 70, text=f"Fractional Knapsack (Capacity: {capacity}, Remaining: {rem}, Value: {state.get('total_v', 0):.2f})", fill="white", font=("Inter", 15, "bold"), tags="item")
        
        # Outline
        self.canvas.create_rectangle(x0, y0, x1, y1, fill="#1E2336", outline="#3B82F6", width=2, tags="item")
        # Fill
        self.canvas.create_rectangle(x0, y0, fill_x, y1, fill="#10B981", outline="", tags="item")
        # Percentage text on bar
        if fill_ratio > 0:
            self.canvas.create_text(x0 + (fill_x - x0)/2, (y0+y1)/2, text=f"{fill_ratio*100:.0f}% full", fill="white", font=("Inter", 11, "bold"), tags="item")
        
        # Draw items as boxes below
        n = len(items)
        if n == 0: return
        box_w = min(120, bar_w / max(n, 1))
        box_gap = 12
        start_x = self.width/2 - (n * (box_w + box_gap))/2
        
        for i, it in enumerate(items): # it = (ratio, w, v, orig_idx)
            ratio, w, v, orig_idx = it
            bx0 = start_x + i * (box_w + box_gap)
            bx1 = bx0 + box_w
            by0 = 190
            by1 = by0 + 90
            
            bg = "#2A2F45"
            if orig_idx == current:
                bg = "#F59E0B"
                
            frac_taken = 0
            for t_idx, t_frac in taken:
                if t_idx == orig_idx: frac_taken = t_frac
                
            self.canvas.create_rectangle(bx0, by0, bx1, by1, fill=bg, outline="#121626", width=2, tags="item")
            
            # Fill fraction inner
            if frac_taken > 0:
                self.canvas.create_rectangle(bx0+1, by1 - 88*frac_taken, bx1-1, by1-1, fill="#3B82F6", outline="", tags="item")
                
            self.canvas.create_text((bx0+bx1)/2, by0 + 17, text=f"W:{w}", fill="white", font=("Inter", 10, "bold"), tags="item")
            self.canvas.create_text((bx0+bx1)/2, by0 + 34, text=f"V:{v}", fill="white", font=("Inter", 10), tags="item")
            self.canvas.create_text((bx0+bx1)/2, by0 + 51, text=f"Rat:{ratio:.1f}", fill="#A0AEC0", font=("Inter", 9), tags="item")
            self.canvas.create_text((bx0+bx1)/2, by0 + 72, text=f"Tk:{frac_taken*100:.0f}%", fill="#10B981" if frac_taken > 0 else "#555", font=("Inter", 9, "bold"), tags="item")


    def run_algo(self, algo_name, s1="", s2=""):
        if self.animating: return
        self.animating = True
        self.set_explanation(f"Starting {algo_name}...")
        
        # Default demo inputs
        if algo_name == "LCS":
            if not s1: s1 = "ABCBDAB"
            if not s2: s2 = "BDCAB"
            self.generator = self.model.lcs(s1, s2)
        elif algo_name == "01Knapsack":
            self.generator = self.model.zero_one_knapsack(50, [10, 20, 30], [60, 100, 120])
        elif algo_name == "FracKnapsack":
            self.generator = self.model.fractional_knapsack(50, [10, 20, 30], [60, 100, 120])
        
        self.animate_step()

    def animate_step(self):
        if not self.generator:
            self.animating = False
            return
            
        try:
            state = next(self.generator)
            
            # Draw the appropriate visualization
            if self.mode == "frac":
                self.draw_frac(state)
            else:
                title = "Longest Common Subsequence (LCS)" if self.mode == "lcs" else "0/1 Knapsack DP Table"
                self.draw_grid(state, title)
            
            # Display the step-by-step explanation text at the bottom
            msg = state.get('msg', '')
            if msg:
                self.set_explanation(msg)
                
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
            self.app.update_info("?", "?", ["Select an algorithm (Frac. Knapsack, 0/1 Knapsack, LCS)", "to load the visualization and code."], None)
