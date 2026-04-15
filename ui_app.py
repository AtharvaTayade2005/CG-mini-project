import customtkinter as ctk
from views.stack_view import StackView

class App(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Data Structure & Algorithm Visualizer")
        self.geometry("1200x800")
        self.minsize(900, 600)
        
        # Base colors for our dark premium theme
        self.bg_color = "#0B0F19"
        self.sidebar_color = "#121626"
        self.panel_color = "#1E2336"
        self.accent_color = "#3B82F6"
        self.accent_hover = "#2563EB"
        self.text_muted = "#A0AEC0"
        
        self.configure(fg_color=self.bg_color)

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # -- SIDEBAR --
        self.sidebar_frame = ctk.CTkFrame(self, width=240, corner_radius=0, fg_color=self.sidebar_color)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        self.sidebar_frame.grid_rowconfigure(8, weight=1)
        self.sidebar_frame.grid_propagate(False)

        # Logo / Title
        self.logo_label = ctk.CTkLabel(
            self.sidebar_frame, 
            text="DS Visualizer", 
            font=ctk.CTkFont(family="Inter", size=24, weight="bold"),
            text_color="#FFFFFF"
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(30, 30), sticky="w")
        
        self.sidebar_btns = {}
        
        self.btn_stack = self.create_sidebar_btn("Stack", "Stack", 1)
        self.btn_queue = self.create_sidebar_btn("Queue", "Queue", 2)
        self.btn_sll = self.create_sidebar_btn("Linked List", "SLL", 3)
        self.btn_heap = self.create_sidebar_btn("Binary Heap", "Heap", 4)
        self.btn_bst = self.create_sidebar_btn("BST", "BST", 5)
        self.btn_avl = self.create_sidebar_btn("AVL Tree", "AVL", 6)
        self.btn_graph = self.create_sidebar_btn("Graph", "Graph", 7)
        self.btn_sort = self.create_sidebar_btn("Sorting", "Sorting", 8)
        self.btn_search = self.create_sidebar_btn("Searching", "Searching", 9)
        self.btn_dp = self.create_sidebar_btn("DP & Greedy", "DP", 10)

        # -- MAIN CONTENT AREA --
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=25, pady=25)
        self.main_frame.grid_columnconfigure(0, weight=3) # Visualization weight
        self.main_frame.grid_columnconfigure(1, weight=1) # Sidebar weight
        self.main_frame.grid_rowconfigure(1, weight=1)

        # -- TOP CONTROL PANEL --
        self.control_panel = ctk.CTkFrame(self.main_frame, height=80, corner_radius=12, fg_color=self.panel_color)
        self.control_panel.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=(0, 20))
        self.control_panel.grid_propagate(False)

        self.input_entry = ctk.CTkEntry(
            self.control_panel, 
            placeholder_text="Enter value...", 
            width=180,
            height=40,
            corner_radius=8,
            font=ctk.CTkFont(family="Inter", size=14),
            border_color="#374151",
            fg_color="#111827"
        )
        self.input_entry.pack(side="left", padx=20, pady=20)

        # -- BULK INPUT BTN --
        self.btn_bulk = ctk.CTkButton(
            self.control_panel, text="📋 Bulk Input", width=100, height=40,
            command=self.open_bulk_input, 
            fg_color="#4F46E5", hover_color="#4338CA",
            font=ctk.CTkFont(family="Inter", size=13, weight="bold")
        )
        # Will be packed dynamically when view needs it

        self.action_buttons_frame = ctk.CTkFrame(self.control_panel, fg_color="transparent")
        self.action_buttons_frame.pack(side="left", fill="both", expand=True, padx=5, pady=0)

        # -- VISUALIZER VIEW CONTAINER --
        self.view_layout = ctk.CTkFrame(self.main_frame, fg_color="transparent")
        self.view_layout.grid(row=1, column=0, sticky="nsew", padx=(0, 15))
        self.view_layout.grid_rowconfigure(0, weight=1)
        self.view_layout.grid_columnconfigure(0, weight=1)

        self.view_container = ctk.CTkFrame(self.view_layout, corner_radius=12, fg_color=self.bg_color)
        self.view_container.grid(row=0, column=0, sticky="nsew", pady=(0, 15))
        self.view_container.grid_rowconfigure(0, weight=1)
        self.view_container.grid_columnconfigure(0, weight=1)
        # Adding a subtle border wrapper for canvas
        self.view_container.configure(border_width=1, border_color="#2A2F45")

        # -- PLAYBACK CONTROLS --
        self.playback_panel = ctk.CTkFrame(self.view_layout, height=60, corner_radius=12, fg_color=self.panel_color)
        self.playback_panel.grid(row=1, column=0, sticky="ew")
        self.playback_panel.grid_propagate(False)
        self.setup_playback_controls()

        # -- INFO SIDEBAR --
        self.info_sidebar = ctk.CTkFrame(self.main_frame, corner_radius=12, fg_color=self.panel_color)
        self.info_sidebar.grid(row=1, column=1, sticky="nsew")
        self.info_sidebar.grid_rowconfigure(3, weight=1)
        self.info_sidebar.grid_columnconfigure(0, weight=1)
        self.setup_info_sidebar()

        self.current_view = None
        self.current_view_name = None
        self.select_view("Stack")
        
    def create_sidebar_btn(self, text, code, row):
        btn = ctk.CTkButton(
            self.sidebar_frame, 
            text=f"  {text}", 
            corner_radius=8, 
            height=45,
            anchor="w",
            font=ctk.CTkFont(family="Inter", size=15, weight="bold"),
            fg_color="transparent", 
            text_color=self.text_muted,
            hover_color="#2A2F45",
            command=lambda: self.select_view(code)
        )
        btn.grid(row=row, column=0, sticky="ew", padx=15, pady=5)
        self.sidebar_btns[code] = btn
        return btn

    def create_action_btn(self, text, command):
        btn = ctk.CTkButton(
            self.action_buttons_frame, 
            text=text, 
            command=command,
            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
            fg_color=self.accent_color,
            hover_color=self.accent_hover,
            corner_radius=8,
            height=40
        )
        return btn

    def update_sidebar_active_state(self, name):
        # Reset all buttons
        for code, btn in self.sidebar_btns.items():
            btn.configure(fg_color="transparent", text_color=self.text_muted)
        
        # Highlight active button
        if name in self.sidebar_btns:
            self.sidebar_btns[name].configure(fg_color=self.accent_color, text_color="#FFFFFF")

    def clear_control_panel(self):
        for widget in self.action_buttons_frame.winfo_children():
            widget.destroy()

    def open_bulk_input(self):
        from views.bulk_input import BulkInputDialog
        dialog = BulkInputDialog(self)
        self.wait_window(dialog)
        val = dialog.get_result()
        if val:
            self.input_entry.delete(0, 'end')
            self.input_entry.insert(0, val)
            if hasattr(self.current_view, 'load_custom_data'):
                self.current_view.load_custom_data(val)

    def setup_playback_controls(self):
        self.btn_play_pause = ctk.CTkButton(self.playback_panel, text="⏸ Pause", width=90, command=self.toggle_play_pause,
                                            font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                                            fg_color="#10B981", hover_color="#059669")
        self.btn_play_pause.pack(side="left", padx=15, pady=15)

        self.btn_step = ctk.CTkButton(self.playback_panel, text="⏭ Step", width=90, command=self.step_forward,
                                      font=ctk.CTkFont(family="Inter", size=14, weight="bold"),
                                      fg_color="#F59E0B", hover_color="#D97706")
        self.btn_step.pack(side="left", padx=10, pady=15)
        
        self.speed_slider = ctk.CTkSlider(self.playback_panel, from_=0.1, to=2.0, command=self.change_speed, width=150)
        self.speed_slider.set(1.0)
        self.speed_slider.pack(side="right", padx=20, pady=20)
        
        lbl_speed = ctk.CTkLabel(self.playback_panel, text="Speed:", font=ctk.CTkFont(family="Inter", size=13))
        lbl_speed.pack(side="right", padx=5, pady=20)

    def setup_info_sidebar(self):
        self.lbl_comp_title = ctk.CTkLabel(self.info_sidebar, text="Complexity", font=ctk.CTkFont(family="Inter", size=16, weight="bold"), text_color="#A0AEC0")
        self.lbl_comp_title.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="w")
        
        self.comp_frame = ctk.CTkFrame(self.info_sidebar, fg_color="#111827", corner_radius=8)
        self.comp_frame.grid(row=1, column=0, padx=15, pady=5, sticky="ew")
        
        self.lbl_time_comp = ctk.CTkLabel(self.comp_frame, text="Time: O(1)", font=ctk.CTkFont(family="Inter", size=14))
        self.lbl_time_comp.pack(anchor="w", padx=15, pady=(10, 5))
        self.lbl_space_comp = ctk.CTkLabel(self.comp_frame, text="Space: O(1)", font=ctk.CTkFont(family="Inter", size=14))
        self.lbl_space_comp.pack(anchor="w", padx=15, pady=(0, 10))

        self.lbl_code_title = ctk.CTkLabel(self.info_sidebar, text="Pseudocode", font=ctk.CTkFont(family="Inter", size=16, weight="bold"), text_color="#A0AEC0")
        self.lbl_code_title.grid(row=2, column=0, padx=15, pady=(20, 5), sticky="w")
        
        self.code_textbox = ctk.CTkTextbox(self.info_sidebar, fg_color="#111827", text_color="#E5E7EB", font=ctk.CTkFont(family="Consolas", size=13), corner_radius=8, wrap="none")
        self.code_textbox.grid(row=3, column=0, padx=15, pady=(0, 15), sticky="nsew")

    def toggle_play_pause(self):
        if hasattr(self.current_view, 'toggle_pause'):
            # Tell view to pause, it should return its new state
            paused = self.current_view.toggle_pause()
            if paused:
                self.btn_play_pause.configure(text="▶ Play", fg_color=self.accent_color, hover_color=self.accent_hover)
            else:
                self.btn_play_pause.configure(text="⏸ Pause", fg_color="#10B981", hover_color="#059669")

    def step_forward(self):
        if hasattr(self.current_view, 'step_forward'):
            self.current_view.step_forward()

    def change_speed(self, value):
        if hasattr(self.current_view, 'set_speed'):
            self.current_view.set_speed(value)

    def update_info(self, time_c, space_c, code_lines, active_line=None):
        self.lbl_time_comp.configure(text=f"Time: {time_c}")
        self.lbl_space_comp.configure(text=f"Space: {space_c}")
        
        if not hasattr(self, '_current_pseudo') or self._current_pseudo != code_lines:
            self.code_textbox.configure(state="normal")
            self.code_textbox.delete("1.0", "end")
            self.code_textbox.insert("1.0", "\\n".join(code_lines))
            self.code_textbox.configure(state="disabled")
            self._current_pseudo = code_lines
            
        if active_line is not None and 0 <= active_line < len(code_lines):
            self.code_textbox.tag_remove("active", "1.0", "end")
            start_idx = f"{active_line + 1}.0"
            end_idx = f"{active_line + 1}.end"
            self.code_textbox.tag_add("active", start_idx, end_idx)
            self.code_textbox.tag_config("active", background="#F59E0B", foreground="#111827")
            self.code_textbox.see(start_idx)

    def select_view(self, name):
        if self.current_view_name == name:
            return # Already selected

        if self.current_view:
            self.current_view.destroy()
        
        self.current_view_name = name
        self.clear_control_panel()
        self.input_entry.delete(0, 'end')
        self.update_sidebar_active_state(name)
        
        # Determine if Bulk Input is needed
        if name == "Sorting":
            self.btn_bulk.pack(side="left", padx=(0, 10), pady=20, before=self.action_buttons_frame)
        else:
            self.btn_bulk.pack_forget()

        # Reset play button
        self.btn_play_pause.configure(text="⏸ Pause", fg_color="#10B981", hover_color="#059669")
        
        # Show default pseudocode template for the selected view
        if hasattr(self.current_view, 'show_default_info'):
            self.current_view.show_default_info()
        else:
            self.update_info("-", "-", ["Load an algorithm or perform an action to view code."], None)

        if name == "Stack":
            self.current_view = StackView(self.view_container)
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_push = self.create_action_btn("Push", lambda: self.current_view.push(self.input_entry.get()))
            btn_push.pack(side="left", padx=10, pady=20)
            
            btn_pop = self.create_action_btn("Pop", self.current_view.pop)
            btn_pop.configure(fg_color="#EF4444", hover_color="#DC2626") # Muted red for pop
            btn_pop.pack(side="left", padx=10, pady=20)
            
        elif name == "Queue":
            from views.queue_view import QueueView
            self.current_view = QueueView(self.view_container)
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_in = self.create_action_btn("Enqueue", lambda: self.current_view.enqueue(self.input_entry.get()))
            btn_in.pack(side="left", padx=10, pady=20)
            
            btn_out = self.create_action_btn("Dequeue", self.current_view.dequeue)
            btn_out.configure(fg_color="#EF4444", hover_color="#DC2626")
            btn_out.pack(side="left", padx=10, pady=20)
            
        elif name == "SLL":
            from views.linked_list_view import LinkedListView
            self.current_view = LinkedListView(self.view_container)
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_in_head = self.create_action_btn("Insert Head", lambda: self.current_view.insert_head(self.input_entry.get()))
            btn_in_head.pack(side="left", padx=8, pady=20)
            
            btn_in_tail = self.create_action_btn("Insert Tail", lambda: self.current_view.insert_tail(self.input_entry.get()))
            btn_in_tail.pack(side="left", padx=8, pady=20)
            
            btn_del_head = self.create_action_btn("Delete Head", self.current_view.delete_head)
            btn_del_head.configure(fg_color="#EF4444", hover_color="#DC2626")
            btn_del_head.pack(side="left", padx=8, pady=20)
            
            btn_del_tail = self.create_action_btn("Delete Tail", self.current_view.delete_tail)
            btn_del_tail.configure(fg_color="#EF4444", hover_color="#DC2626")
            btn_del_tail.pack(side="left", padx=8, pady=20)
            
        elif name == "Heap":
            from views.heap_view import HeapView
            self.current_view = HeapView(self.view_container)
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

            def change_heap_type(value):
                if not hasattr(self, 'current_view') or not isinstance(self.current_view, HeapView):
                    return
                is_min = (value == "Min Heap")
                self.current_view.set_heap_type(is_min)
                btn_ext.configure(text=f"Extract {'Min' if is_min else 'Max'}")

            seg_btn = ctk.CTkSegmentedButton(self.action_buttons_frame, values=["Min Heap", "Max Heap"], command=change_heap_type, selected_color=self.accent_color, selected_hover_color=self.accent_hover)
            seg_btn.pack(side="left", padx=10, pady=20)
            seg_btn.set("Min Heap")
            
            btn_insert = self.create_action_btn("Insert", lambda: self.current_view.insert(self.input_entry.get()))
            btn_insert.pack(side="left", padx=5, pady=20)
            
            btn_ext = self.create_action_btn("Extract Min", self.current_view.extract)
            btn_ext.configure(fg_color="#EF4444", hover_color="#DC2626")
            btn_ext.pack(side="left", padx=5, pady=20)
            
            btn_tr_in = self.create_action_btn("In-order", lambda: self.current_view.traverse("in"))
            btn_tr_in.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_in.pack(side="left", padx=5, pady=20)
            
            btn_tr_pre = self.create_action_btn("Pre-order", lambda: self.current_view.traverse("pre"))
            btn_tr_pre.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_pre.pack(side="left", padx=5, pady=20)
            
            btn_tr_post = self.create_action_btn("Post-order", lambda: self.current_view.traverse("post"))
            btn_tr_post.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_post.pack(side="left", padx=5, pady=20)
            
        elif name == "AVL":
            from views.avl_tree_view import AVLTreeView
            self.current_view = AVLTreeView(self.view_container)
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_insert = self.create_action_btn("Insert", lambda: self.current_view.insert(self.input_entry.get()))
            btn_insert.pack(side="left", padx=5, pady=20)
            
            btn_del = self.create_action_btn("Delete", lambda: self.current_view.delete(self.input_entry.get()))
            btn_del.configure(fg_color="#EF4444", hover_color="#DC2626")
            btn_del.pack(side="left", padx=5, pady=20)
            
            btn_src = self.create_action_btn("Search", lambda: self.current_view.search(self.input_entry.get()))
            btn_src.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_src.pack(side="left", padx=5, pady=20)
            
            btn_tr_in = self.create_action_btn("In-order", lambda: self.current_view.traverse("in"))
            btn_tr_in.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_in.pack(side="left", padx=5, pady=20)
            
            btn_tr_pre = self.create_action_btn("Pre-order", lambda: self.current_view.traverse("pre"))
            btn_tr_pre.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_pre.pack(side="left", padx=5, pady=20)
            
            btn_tr_post = self.create_action_btn("Post-order", lambda: self.current_view.traverse("post"))
            btn_tr_post.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_post.pack(side="left", padx=5, pady=20)
            
        elif name == "BST":
            from views.bst_view import BSTView
            self.current_view = BSTView(self.view_container)
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_insert = self.create_action_btn("Insert", lambda: self.current_view.insert(self.input_entry.get()))
            btn_insert.pack(side="left", padx=5, pady=20)
            
            btn_del = self.create_action_btn("Delete", lambda: self.current_view.delete(self.input_entry.get()))
            btn_del.configure(fg_color="#EF4444", hover_color="#DC2626")
            btn_del.pack(side="left", padx=5, pady=20)
            
            btn_src = self.create_action_btn("Search", lambda: self.current_view.search(self.input_entry.get()))
            btn_src.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_src.pack(side="left", padx=5, pady=20)
            
            btn_tr_in = self.create_action_btn("In-order", lambda: self.current_view.traverse("in"))
            btn_tr_in.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_in.pack(side="left", padx=5, pady=20)
            
            btn_tr_pre = self.create_action_btn("Pre-order", lambda: self.current_view.traverse("pre"))
            btn_tr_pre.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_pre.pack(side="left", padx=5, pady=20)
            
            btn_tr_post = self.create_action_btn("Post-order", lambda: self.current_view.traverse("post"))
            btn_tr_post.configure(fg_color="#10B981", hover_color="#059669")
            btn_tr_post.pack(side="left", padx=5, pady=20)

        elif name == "Graph":
            from views.graph_view import GraphView
            self.current_view = GraphView(self.view_container)
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_add_v = self.create_action_btn("+ V", lambda: self.current_view.add_vertex(self.input_entry.get()))
            btn_add_v.pack(side="left", padx=2, pady=20)
            
            btn_add_e_u = self.create_action_btn("+ E (u,v,w)", lambda: self.current_view.add_edge(self.input_entry.get(), False))
            btn_add_e_u.configure(fg_color="#6366F1", hover_color="#4F46E5")
            btn_add_e_u.pack(side="left", padx=2, pady=20)
            
            btn_bfs = self.create_action_btn("BFS", lambda: self.current_view.traverse(self.input_entry.get(), "BFS"))
            btn_bfs.pack(side="left", padx=2, pady=20)

            btn_dfs = self.create_action_btn("DFS", lambda: self.current_view.traverse(self.input_entry.get(), "DFS"))
            btn_dfs.pack(side="left", padx=2, pady=20)
            
            btn_dij = self.create_action_btn("Dijkstra", lambda: self.current_view.run_algo("Dijkstra", self.input_entry.get()))
            btn_dij.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_dij.pack(side="left", padx=2, pady=20)
            
            btn_bel = self.create_action_btn("Bellman", lambda: self.current_view.run_algo("Bellman", self.input_entry.get()))
            btn_bel.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_bel.pack(side="left", padx=2, pady=20)
            
            btn_prim = self.create_action_btn("Prim's", lambda: self.current_view.run_algo("Prim"))
            btn_prim.configure(fg_color="#10B981", hover_color="#059669")
            btn_prim.pack(side="left", padx=2, pady=20)
            
            btn_krus = self.create_action_btn("Kruskal's", lambda: self.current_view.run_algo("Kruskal"))
            btn_krus.configure(fg_color="#10B981", hover_color="#059669")
            btn_krus.pack(side="left", padx=2, pady=20)
            
            btn_src = self.create_action_btn("Search", lambda: self.current_view.search(self.input_entry.get()))
            btn_src.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_src.pack(side="left", padx=3, pady=20)
            
        elif name == "Sorting":
            from views.array_view import ArrayView
            self.current_view = ArrayView(self.view_container, mode="sort")
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_gen = self.create_action_btn("New Array", self.current_view.generate_new)
            btn_gen.pack(side="left", padx=5, pady=20)
            
            btn_bub = self.create_action_btn("Bubble Sort", lambda: self.current_view.run_algo("Bubble"))
            btn_bub.configure(fg_color="#10B981", hover_color="#059669")
            btn_bub.pack(side="left", padx=5, pady=20)
            
            btn_ins = self.create_action_btn("Insertion Sort", lambda: self.current_view.run_algo("Insertion"))
            btn_ins.configure(fg_color="#10B981", hover_color="#059669")
            btn_ins.pack(side="left", padx=5, pady=20)
            
            btn_qs = self.create_action_btn("Quick Sort", lambda: self.current_view.run_algo("Quick"))
            btn_qs.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_qs.pack(side="left", padx=5, pady=20)
            
            btn_ms = self.create_action_btn("Merge Sort", lambda: self.current_view.run_algo("Merge"))
            btn_ms.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_ms.pack(side="left", padx=5, pady=20)

        elif name == "Searching":
            from views.array_view import ArrayView
            self.current_view = ArrayView(self.view_container, mode="search")
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_gen = self.create_action_btn("New Array", self.current_view.generate_new)
            btn_gen.pack(side="left", padx=5, pady=20)
            
            btn_lin = self.create_action_btn("Linear Search", lambda: self.current_view.run_algo("Linear Search", self.input_entry.get()))
            btn_lin.pack(side="left", padx=5, pady=20)
            
            btn_bin = self.create_action_btn("Binary Search", lambda: self.current_view.run_algo("Binary Search", self.input_entry.get()))
            btn_bin.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_bin.pack(side="left", padx=5, pady=20)
            
        elif name == "DP":
            from views.dp_greedy_view import DPGreedyView
            self.current_view = DPGreedyView(self.view_container, mode="lcs")
            self.current_view.app = self
            self.current_view.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
            
            btn_frac = self.create_action_btn("Frac. Knapsack", lambda: [setattr(self.current_view, 'mode', 'frac'), self.current_view.run_algo("FracKnapsack")])
            btn_frac.pack(side="left", padx=5, pady=20)
            
            btn_01 = self.create_action_btn("0/1 Knapsack", lambda: [setattr(self.current_view, 'mode', '01'), self.current_view.run_algo("01Knapsack")])
            btn_01.configure(fg_color="#8B5CF6", hover_color="#7C3AED")
            btn_01.pack(side="left", padx=5, pady=20)
            
            btn_lcs = self.create_action_btn("LCS", lambda: [setattr(self.current_view, 'mode', 'lcs'), self.current_view.run_algo("LCS")])
            btn_lcs.configure(fg_color="#10B981", hover_color="#059669")
            btn_lcs.pack(side="left", padx=5, pady=20)

        else:
            label = ctk.CTkLabel(self.view_container, text=f"{name} View Placeholder", font=ctk.CTkFont(family="Inter", size=20))
            label.grid(row=0, column=0)
            self.current_view = label
