import json
import statistics
import tkinter as tk
from tkinter import ttk, messagebox, StringVar
from pathlib import Path


class OmegaTerminalApp:
    """Main application class for the Omega Terminal-inspired student data system."""

    def __init__(self, root):
        """Initialize the root window, theme settings, data model, and UI structure."""
        self.root = root
        self.root.title("")
        self.root.geometry("1200x720")
        self.root.configure(bg="#020202")
        self.root.resizable(False, False)

        # Data storage location and current in-memory dataset
        self.database_path = Path(__file__).with_name("database.json")
        self.student_data = []

        # Login input variables
        self.username_var = StringVar()
        self.password_var = StringVar()

        # Student form variables
        self.form_name = StringVar()
        self.form_class = StringVar()
        self.form_score = StringVar()
        self.form_status = StringVar()

        # Current page tracker
        self.current_page = None

        # Load persisted data and prepare the UI
        self.load_database()
        self.create_styles()
        self.create_login_screen()

    # ----------------------------------------------------------------------
    # Database Logic
    # ----------------------------------------------------------------------
    def load_database(self):
        """Load student records from a JSON file; initialize file when missing."""
        if not self.database_path.exists():
            default_data = [
                {"Name": "Lara Adams", "Class": "12A", "Score": 89, "Status": "Pass"},
                {"Name": "Rian Hart", "Class": "11C", "Score": 74, "Status": "Pass"},
                {"Name": "Mia Chen", "Class": "10B", "Score": 95, "Status": "Pass"},
            ]
            self.student_data = default_data
            self.save_database()
            return

        try:
            with self.database_path.open("r", encoding="utf-8") as file:
                self.student_data = json.load(file)
        except (json.JSONDecodeError, IOError):
            self.student_data = []
            self.save_database()

    def save_database(self):
        """Write the current list of student records back to the JSON database file."""
        with self.database_path.open("w", encoding="utf-8") as file:
            json.dump(self.student_data, file, indent=4)

    def add_student_record(self, record):
        """Append a new student record and persist it."""
        self.student_data.append(record)
        self.save_database()
        self.refresh_student_table()
        self.refresh_statistics()

    def update_student_record(self, index, updated_record):
        """Update the change."""
        self.student_data[index] = updated_record
        self.save_database()
        self.refresh_student_table()
        self.refresh_statistics()

    def delete_student_record(self, index):
        """Delete the change."""
        del self.student_data[index]
        self.save_database()
        self.refresh_student_table()
        self.refresh_statistics()

    # ----------------------------------------------------------------------
    # Styling and UI Utilities
    # ----------------------------------------------------------------------
    def create_styles(self):
        """Define ttk styling and widget theme settings for a neon/dark aesthetic."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        style.configure("TFrame", background="#020202")
        style.configure("TLabel", background="#020202", foreground="#00ff41", font=("Consolas", 11))
        style.configure("Header.TLabel", font=("Consolas", 18, "bold"), foreground="#00ff41")
        style.configure("Section.TLabel", font=("Consolas", 14, "bold"), foreground="#00ff41")
        style.configure("TButton", background="#020202", foreground="#00ff41", font=("Consolas", 11), relief="flat")
        style.map("TButton", background=[("active", "#111111")], foreground=[("active", "#00ff41")])
        style.configure("Treeview", background="#101010", fieldbackground="#101010", foreground="#00ff41", rowheight=26, bordercolor="#111111", borderwidth=1)
        style.configure("Treeview.Heading", background="#111111", foreground="#00ff41", font=("Consolas", 11, "bold"))
        style.map("Treeview", background=[("selected", "#004400")], foreground=[("selected", "#ffffff")])

    def clear_root(self):
        """Remove all widgets from the root window to prepare a new page."""
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_neon_label(self, parent, text, style="TLabel", **kwargs):
        """Helper to create consistent neon-themed labels."""
        return ttk.Label(parent, text=text, style=style, **kwargs)

    def create_sidebar_button(self, parent, text, command):
        """Helper to create sidebar navigation buttons with consistent appearance."""
        button = ttk.Button(parent, text=text, command=command)
        button.configure(width=24)
        return button

    # ----------------------------------------------------------------------
    # Authentication and Login Screen
    # ----------------------------------------------------------------------
    def create_login_screen(self):
        """Render the login screen before allowing access to the application."""
        self.clear_root()

        login_frame = ttk.Frame(self.root, padding=(30, 30, 30, 30), style="TFrame")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.create_neon_label(login_frame, "ACCESS", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 24))
        self.create_neon_label(login_frame, "Username:").grid(row=1, column=0, sticky="w", padx=8, pady=6)
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var, font=("Consolas", 12), width=28)
        username_entry.grid(row=1, column=1, pady=6)

        self.create_neon_label(login_frame, "Password:").grid(row=2, column=0, sticky="w", padx=8, pady=6)
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, show="*", font=("Consolas", 12), width=28)
        password_entry.grid(row=2, column=1, pady=6)

        auth_hint = ttk.Label(login_frame, text="Isi dulu baru Enter", font=("Consolas", 9), foreground="#00ff41", background="#020202")
        auth_hint.grid(row=3, column=0, columnspan=2, pady=(14, 24))

        login_button = ttk.Button(login_frame, text="ENTER", command=self.verify_login)
        login_button.grid(row=4, column=0, columnspan=2, pady=8)

        username_entry.focus()

    def verify_login(self):
        """Validate login credentials and load the main interface if authenticated."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if username == "tes" and password == "1234":
            self.create_main_interface()
            return

        messagebox.showerror("ACCESS DENIED", "Invalid username or password. Please try again.")

    # ----------------------------------------------------------------------
    # Main Interface Construction
    # ----------------------------------------------------------------------
    def create_main_interface(self):
        """Build the main application frame with sidebar and default dashboard view."""
        self.clear_root()

        root_container = ttk.Frame(self.root, style="TFrame")
        root_container.pack(fill="both", expand=True)

        sidebar_frame = ttk.Frame(root_container, width=250, padding=(16, 16, 16, 16), style="TFrame")
        sidebar_frame.pack(side="left", fill="y")

        content_frame = ttk.Frame(root_container, padding=(18, 18, 18, 18), style="TFrame")
        content_frame.pack(side="right", fill="both", expand=True)

        self.sidebar_frame = sidebar_frame
        self.content_frame = content_frame

        self.create_neon_label(sidebar_frame, "", style="Header.TLabel").pack(pady=(0, 24))
        self.create_neon_label(sidebar_frame, "", style="Section.TLabel").pack(anchor="w", pady=(0, 12))

        self.create_sidebar_button(sidebar_frame, "Overview", self.show_dashboard).pack(fill="x", pady=8)
        self.create_sidebar_button(sidebar_frame, "Records", self.show_student_database).pack(fill="x", pady=8)
        self.create_sidebar_button(sidebar_frame, "Statistics Analysis", self.show_statistics_analysis).pack(fill="x", pady=8)
        ttk.Separator(sidebar_frame, orient="horizontal").pack(fill="x", pady=24)
        self.create_neon_label(sidebar_frame, "", font=("Consolas", 9), style="TLabel").pack(anchor="w", pady=(12, 0))

        self.show_dashboard()

    # ----------------------------------------------------------------------
    # Overview Page
    # ----------------------------------------------------------------------
    def show_dashboard(self):
        """Render the dashboard summary page with system information and data highlights."""
        self.clear_content_area()
        self.current_page = "Overview"

        header = self.create_neon_label(self.content_frame, "Overview", style="Header.TLabel")
        header.pack(anchor="w", pady=(0, 14))

        subtitle = self.create_neon_label(self.content_frame, "", style="TLabel")
        subtitle.pack(anchor="w", pady=(0, 26))

        stats_frame = ttk.Frame(self.content_frame, padding=(12, 12, 12, 12), style="TFrame")
        stats_frame.pack(fill="x", pady=(0, 16))

        total = len(self.student_data)
        average = self.calculate_average()
        high = self.calculate_highest()
        low = self.calculate_lowest()

        for label, value in [
            ("Total Records", total),
            ("Rata Rata Score", f"{average:.2f}" if average is not None else "N/A"),
            ("Tinggi Score", high if high is not None else "N/A"),
            ("Rendah Score", low if low is not None else "N/A"),
        ]:
            card = ttk.Frame(stats_frame, padding=(16, 16, 16, 16), style="TFrame")
            card.pack(side="left", expand=True, fill="x", padx=8)
            self.create_neon_label(card, label, style="Section.TLabel").pack(anchor="w")
            self.create_neon_label(card, str(value), style="TLabel").pack(anchor="w", pady=(10, 0))

        audit_frame = ttk.Frame(self.content_frame, padding=(16, 16, 16, 16), style="TFrame")
        audit_frame.pack(fill="both", expand=True)
        self.create_neon_label(audit_frame, "Database", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        self.create_student_table(audit_frame)

    # ----------------------------------------------------------------------
    # Records Page
    # ----------------------------------------------------------------------
    def show_student_database(self):
        """Render the student database management page with add/update/delete controls."""
        self.clear_content_area()
        self.current_page = "Records"

        header = self.create_neon_label(self.content_frame, "Records", style="Header.TLabel")
        header.pack(anchor="w", pady=(0, 14))

        student_frame = ttk.Frame(self.content_frame, style="TFrame")
        student_frame.pack(fill="both", expand=True)

        form_frame = ttk.Frame(student_frame, padding=(12, 12, 12, 12), style="TFrame")
        form_frame.pack(side="left", fill="y", padx=(0, 16), pady=(0, 16))

        self.create_neon_label(form_frame, "Record Editor", style="Section.TLabel").pack(anchor="w", pady=(0, 12))
        self.create_neon_label(form_frame, "Name:").pack(anchor="w", pady=4)
        ttk.Entry(form_frame, textvariable=self.form_name, font=("Consolas", 11), width=30).pack(anchor="w", pady=4)
        self.create_neon_label(form_frame, "Class:").pack(anchor="w", pady=4)
        ttk.Entry(form_frame, textvariable=self.form_class, font=("Consolas", 11), width=30).pack(anchor="w", pady=4)
        self.create_neon_label(form_frame, "Score:").pack(anchor="w", pady=4)
        ttk.Entry(form_frame, textvariable=self.form_score, font=("Consolas", 11), width=30).pack(anchor="w", pady=4)
        self.create_neon_label(form_frame, "Status:").pack(anchor="w", pady=4)
        ttk.Entry(form_frame, textvariable=self.form_status, font=("Consolas", 11), width=30).pack(anchor="w", pady=4)

        button_area = ttk.Frame(form_frame, style="TFrame")
        button_area.pack(fill="x", pady=(18, 0))
        ttk.Button(button_area, text="Add Record", command=self.add_record_from_form).pack(side="left", padx=(0, 8))
        ttk.Button(button_area, text="Update Selected", command=self.update_selected_record).pack(side="left", padx=(0, 8))
        ttk.Button(button_area, text="Remove Selected", command=self.delete_selected_record).pack(side="left")

        table_frame = ttk.Frame(student_frame, padding=(0, 0, 0, 0), style="TFrame")
        table_frame.pack(side="right", fill="both", expand=True, pady=(0, 16))

        self.create_neon_label(table_frame, "Recor Murid", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        self.create_student_table(table_frame)

    def create_student_table(self, parent):
        """Create or refresh a Treeview widget displaying student records."""
        if hasattr(self, "student_table") and self.student_table.winfo_exists():
            self.student_table.destroy()

        columns = ("Name", "Class", "Score", "Status")
        self.student_table = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse", height=12)
        self.student_table.pack(fill="both", expand=True)

        for column in columns:
            self.student_table.heading(column, text=column)
            self.student_table.column(column, anchor="center", width=160)

        self.refresh_student_table()
        self.student_table.bind("<ButtonRelease-1>", self.bind_table_selection)

    def refresh_student_table(self):
        """Update the Treeview rows to reflect the latest dataset."""
        if not hasattr(self, "student_table"):
            return

        self.student_table.delete(*self.student_table.get_children())
        for record in self.student_data:
            self.student_table.insert("", "end", values=(record["Name"], record["Class"], record["Score"], record["Status"]))

    def bind_table_selection(self, event):
        """Populate form fields with the selected student record for editing."""
        selected = self.student_table.focus()
        if not selected:
            return

        values = self.student_table.item(selected, "values")
        self.form_name.set(values[0])
        self.form_class.set(values[1])
        self.form_score.set(values[2])
        self.form_status.set(values[3])

    def add_record_from_form(self):
        """Validate the student input form and add a new record."""
        name = self.form_name.get().strip()
        class_name = self.form_class.get().strip()
        score_text = self.form_score.get().strip()
        status = self.form_status.get().strip()

        if not name or not class_name or not score_text or not status:
            messagebox.showwarning("Incomplete Data", "All fields are required to add a new record.")
            return

        try:
            score = float(score_text)
        except ValueError:
            messagebox.showwarning("Invalid Score", "Score must be a number.")
            return

        record = {"Name": name, "Class": class_name, "Score": score, "Status": status}
        self.add_student_record(record)
        self.clear_form_fields()

    def update_selected_record(self):
        """Update the currently selected record with values from the form."""
        selected = self.student_table.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Select a record in the table to update it.")
            return

        index = self.student_table.index(selected)
        name = self.form_name.get().strip()
        class_name = self.form_class.get().strip()
        score_text = self.form_score.get().strip()
        status = self.form_status.get().strip()

        if not name or not class_name or not score_text or not status:
            messagebox.showwarning("Incomplete Data", "All fields are required to update the record.")
            return

        try:
            score = float(score_text)
        except ValueError:
            messagebox.showwarning("Invalid Score", "Score must be a number.")
            return

        updated_record = {"Name": name, "Class": class_name, "Score": score, "Status": status}
        self.update_student_record(index, updated_record)
        self.clear_form_fields()

    def delete_selected_record(self):
        """Delete the user-selected record from the dataset."""
        selected = self.student_table.focus()
        if not selected:
            messagebox.showwarning("No Selection", "Select a record in the table before deleting.")
            return

        index = self.student_table.index(selected)
        confirm = messagebox.askyesno("Confirm Delete", "Delete the selected record from the database?")
        if confirm:
            self.delete_student_record(index)
            self.clear_form_fields()

    def clear_form_fields(self):
        """Reset all student entry form fields."""
        self.form_name.set("")
        self.form_class.set("")
        self.form_score.set("")
        self.form_status.set("")

    # ----------------------------------------------------------------------
    # Analytics Page
    # ----------------------------------------------------------------------
    def show_statistics_analysis(self):
        """Render the statistics page with dynamic calculations from the student dataset."""
        self.clear_content_area()
        self.current_page = "Analytics"

        header = self.create_neon_label(self.content_frame, "Analytics", style="Header.TLabel")
        header.pack(anchor="w", pady=(0, 14))

        description = self.create_neon_label(self.content_frame, "", style="TLabel")
        description.pack(anchor="w", pady=(0, 24))

        stats_frame = ttk.Frame(self.content_frame, style="TFrame")
        stats_frame.pack(fill="x", pady=(0, 14))

        stats = self.calculate_statistics()
        for label, value in stats.items():
            card = ttk.Frame(stats_frame, padding=(16, 16, 16, 16), style="TFrame")
            card.pack(side="left", expand=True, fill="x", padx=8)
            self.create_neon_label(card, label, style="Section.TLabel").pack(anchor="w")
            self.create_neon_label(card, value, style="TLabel").pack(anchor="w", pady=(10, 0))

        chart_frame = ttk.Frame(self.content_frame, padding=(14, 14, 14, 14), style="TFrame")
        chart_frame.pack(fill="both", expand=True, pady=(18, 0))
        self.create_neon_label(chart_frame, "Score Distribution", style="Section.TLabel").pack(anchor="w", pady=(0, 10))

        self.create_statistics_table(chart_frame)

    def calculate_average(self):
        """Compute the average score from the current dataset."""
        scores = [record["Score"] for record in self.student_data if isinstance(record.get("Score"), (int, float))]
        return statistics.mean(scores) if scores else None

    def calculate_median(self):
        """Compute the median score from the current dataset."""
        scores = [record["Score"] for record in self.student_data if isinstance(record.get("Score"), (int, float))]
        return statistics.median(scores) if scores else None

    def calculate_highest(self):
        """Determine the highest score in the current dataset."""
        scores = [record["Score"] for record in self.student_data if isinstance(record.get("Score"), (int, float))]
        return max(scores) if scores else None

    def calculate_lowest(self):
        """Determine the lowest score in the current dataset."""
        scores = [record["Score"] for record in self.student_data if isinstance(record.get("Score"), (int, float))]
        return min(scores) if scores else None

    def calculate_statistics(self):
        """Collect summary statistics for the statistics page."""
        average = self.calculate_average()
        median = self.calculate_median()
        highest = self.calculate_highest()
        lowest = self.calculate_lowest()
        total = len(self.student_data)

        return {
            "Total Students": str(total),
            "Average Score": f"{average:.2f}" if average is not None else "N/A",
            "Median Score": f"{median:.2f}" if median is not None else "N/A",
            "Highest Score": str(highest) if highest is not None else "N/A",
            "Lowest Score": str(lowest) if lowest is not None else "N/A",
        }

    def create_statistics_table(self, parent):
        """Create a read-only score distribution table for quick analysis."""
        columns = ("Student", "Score", "Status")
        table = ttk.Treeview(parent, columns=columns, show="headings", selectmode="none", height=12)
        table.pack(fill="both", expand=True)

        for column in columns:
            table.heading(column, text=column)
            table.column(column, anchor="center", width=200)

        for record in self.student_data:
            table.insert("", "end", values=(record["Name"], record["Score"], record["Status"]))

    # ----------------------------------------------------------------------
    # Internal UI Helpers
    # ----------------------------------------------------------------------
    def clear_content_area(self):
        """Clear only the right-side content area while preserving the sidebar."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def refresh_statistics(self):
        """Refresh statistics widgets when underlying data changes."""
        if self.current_page == "statistics":
            self.show_statistics_analysis()
        elif self.current_page == "dashboard":
            self.show_dashboard()


if __name__ == "__main__":
    root = tk.Tk()
    app = OmegaTerminalApp(root)
    root.mainloop()
