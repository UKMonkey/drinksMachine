import tkinter as tk
from glass_size_store import GlassSizeStore


class GlassSizeDialog:

    def __init__(self, parent, on_size_selected):
        self.parent = parent
        self.on_size_selected = on_size_selected
        self.timer_id = None

        self.dialog = tk.Toplevel(parent)
        self.dialog.attributes("-fullscreen", True)
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.configure(bg="#f0f0f0")

        # Title Label
        title_label = tk.Label(
            self.dialog,
            text="Select Glass Size",
            font=("Arial", 28, "bold"),
            bg="#f0f0f0",
            pady=20,
        )
        title_label.pack(side=tk.TOP, fill=tk.X)

        # Cancel / Back Button at the bottom
        btn_back = tk.Button(
            self.dialog,
            text="Cancel",
            font=("Arial", 20, "bold"),
            bg="#f8d7da",
            command=self.cancel_and_close,
            height=2,
        )
        btn_back.pack(side=tk.BOTTOM, fill=tk.X, padx=20, pady=20)

        # Scrollable container frame for touch devices
        container = tk.Frame(self.dialog, bg="#f0f0f0")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.config(width=40)

        self.scrollable_frame = tk.Frame(canvas, bg="#ffffff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        canvas.bind("<ButtonPress-1>", lambda event: canvas.scan_mark(event.x, event.y))
        canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

        self.dialog.bind("<Any-ButtonPress>", self.reset_timeout)
        self.dialog.bind("<Any-KeyPress>", self.reset_timeout)

        self.populate_sizes()
        self.reset_timeout()

    def reset_timeout(self, event=None):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)
        self.timer_id = self.dialog.after(60000, self.auto_cancel)

    def auto_cancel(self):
        print("GlassSizeDialog: Timed out due to inactivity, auto-canceling.")
        self.dialog.destroy()

    def cancel_and_close(self):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)
        self.dialog.destroy()

    def populate_sizes(self):
        sizes = GlassSizeStore.get_glass_sizes()

        if not sizes:
            lbl = tk.Label(
                self.scrollable_frame,
                text="No glass sizes found in configuration.",
                font=("Arial", 18),
                bg="#ffffff",
                fg="#666666",
            )
            lbl.pack(pady=40, padx=20)
            return

        for size_info in sizes:
            btn = tk.Button(
                self.scrollable_frame,
                text=size_info.get("name", "Unknown Glass"),
                font=("Arial", 24),
                bg="#e0e0e0",
                activebackground="#d0d0d0",
                anchor="w",
                padx=30,
                pady=20,
                command=lambda info=size_info: self.select_size(info),
            )
            btn.pack(fill=tk.X, padx=10, pady=8)

    def select_size(self, size_info):
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)
        print(f"Glass size selected: {size_info['name']}")
        if self.on_size_selected:
            self.on_size_selected(size_info)
        self.dialog.destroy()