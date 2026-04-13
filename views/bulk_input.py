import customtkinter as ctk

class BulkInputDialog(ctk.CTkToplevel):
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Bulk Input")
        self.geometry("400x300")
        self.resizable(False, False)
        
        # Center the dialog
        self.update_idletasks()
        if master:
            x = master.winfo_rootx() + (master.winfo_width() // 2) - (400 // 2)
            y = master.winfo_rooty() + (master.winfo_height() // 2) - (300 // 2)
            self.geometry(f"+{x}+{y}")
        
        self.transient(master)
        self.grab_set()

        self.result = None

        self.configure(fg_color="#1E2336")

        lbl = ctk.CTkLabel(self, text="Paste comma or space-separated values:", 
                           font=ctk.CTkFont(family="Inter", size=14, weight="bold"), text_color="#A0AEC0")
        lbl.pack(pady=(20, 10))

        self.textbox = ctk.CTkTextbox(self, fg_color="#111827", border_color="#374151", border_width=1,
                                      font=ctk.CTkFont(family="Inter", size=14), corner_radius=8, height=150)
        self.textbox.pack(fill="x", padx=20, pady=10)
        self.textbox.focus()

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=20, pady=10)

        btn_cancel = ctk.CTkButton(btn_frame, text="Cancel", command=self.destroy, fg_color="#374151", hover_color="#4B5563")
        btn_cancel.pack(side="left", expand=True, padx=5)

        btn_ok = ctk.CTkButton(btn_frame, text="Load Data", command=self.submit, fg_color="#4F46E5", hover_color="#4338CA")
        btn_ok.pack(side="right", expand=True, padx=5)

    def submit(self):
        self.result = self.textbox.get("1.0", "end").strip()
        self.destroy()

    def get_result(self):
        return self.result
