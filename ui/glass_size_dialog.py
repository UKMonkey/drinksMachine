import tkinter as tk


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

        # Create a scrollable container frame for touch devices
        container = tk.Frame(self.dialog, bg="#f0f0f0")
        container.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        canvas = tk.Canvas(container, bg="#ffffff", highlightthickness=0)
        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.config(width=40)  # Extra wide for easy finger touch scrolling

        self.scrollable_frame = tk.Frame(canvas, bg="#ffffff")

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Enable touch drag-to-scroll on the canvas
        canvas.bind("<ButtonPress-1>", lambda event: canvas.scan_mark(event.x, event.y))
        canvas.bind("<B1-Motion>", lambda event: canvas.scan_dragto(event.x, event.y, gain=1))

        # Reset timeout on any user interaction across the dialog window
        self.dialog.bind("<Any-ButtonPress>", self.reset_timeout)
        self.dialog.bind("<Any-KeyPress>", self.reset_timeout)

        # Populate hard-coded sizes
        self.populate_sizes()

        # Start the initial 60-second timeout countdown (60000 ms)
        self.reset_timeout()

    def reset_timeout(self, event=None):
        """Resets the 60-second auto-cancel inactivity timer."""
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)

        # 60,000 milliseconds = 60 seconds
        self.timer_id = self.dialog.after(60000, self.auto_cancel)

    def auto_cancel(self):
        """Called automatically when the 60-second timeout expires."""
        print("GlassSizeDialog: Timed out due to inactivity, auto-canceling.")
        self.dialog.destroy()

    def cancel_and_close(self):
        """Manual cancel via button click."""
        if self.timer_id:
            self.dialog.after_cancel(self.timer_id)
        self.dialog.destroy()

    def populate_sizes(self):
        sizes = [
            {"name": "Standard Glass (250ml)", "multiplier": 1.0},
            {"name": "Large Glass (400ml)", "multiplier": 1.6},
        ]

        for size_info in sizes:
            btn = tk.Button(
                self.scrollable_frame,
                text=size_info["name"],
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