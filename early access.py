import json
import statistics
import tkinter as tk
from tkinter import ttk, messagebox, StringVar, Canvas, Toplevel
from pathlib import Path
from datetime import datetime
from collections import defaultdict
import os

# Try to import optional libraries for advanced features
try:
    from PIL import Image, ImageDraw, ImageFont
    PILLOW_AVAILABLE = True
except ImportError:
    PILLOW_AVAILABLE = False

try:
    import matplotlib.pyplot as plt
    import matplotlib
    matplotlib.use('TkAgg')
    from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, PageBreak
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    REPORTLAB_AVAILABLE = True
except ImportError:
    REPORTLAB_AVAILABLE = False


class ProTestingApp:
    """Main application class for the Pro by TESTING student data system."""

    def __init__(self, root):
        """Initialize the root window, theme settings, data model, and UI structure."""
        self.root = root
        self.root.title("early access- TESTING")
        self.root.geometry("1400x800")
        self.root.configure(bg="#0a0a0a")
        self.root.resizable(True, True)

        # Data storage locations and current in-memory dataset
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

        # Search variable
        self.search_var = StringVar()
        self.search_var.trace("w", self.on_search_change)

        # Current page tracker
        self.current_page = None
        
        # Notification system
        self.notification_label = None
        self.notification_after_id = None
        
        # Pass/Fail threshold
        self.pass_threshold = 75

        # Load persisted data and prepare the UI
        self.load_database()
        self.create_styles()
        self.create_login_screen()

    # ----------------------------------------------------------------------
    # Database and Activity Log Logic
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

    def load_activity_log(self):
        """Load activity log from JSON file."""
        if not self.activity_log_path.exists():
            self.activity_log = []
            return

        try:
            with self.activity_log_path.open("r", encoding="utf-8") as file:
                self.activity_log = json.load(file)
        except (json.JSONDecodeError, IOError):
            self.activity_log = []

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
        self.show_notification(f"✓ Student '{record['Name']}' added successfully!")

    def update_student_record(self, index, updated_record):
        """Update the record."""
        old_name = self.student_data[index].get("Name", "Unknown")
        self.student_data[index] = updated_record
        self.save_database()
        self.refresh_student_table()
        self.refresh_statistics()
        self.show_notification(f"✓ Student '{updated_record['Name']}' updated successfully!")

    def delete_student_record(self, index):
        """Delete the record."""
        deleted_name = self.student_data[index].get("Name", "Unknown")
        del self.student_data[index]
        self.save_database()
        self.refresh_student_table()
        self.refresh_statistics()
        self.show_notification(f"✓ Student '{deleted_name}' deleted successfully!")

    # ----------------------------------------------------------------------
    # Styling and UI Utilities
    # ----------------------------------------------------------------------
    def create_styles(self):
        """Define ttk styling for futuristic Onyx Black with Phosphor Green theme."""
        style = ttk.Style(self.root)
        style.theme_use("clam")

        # Color scheme
        onyx_black = "#0a0a0a"
        dark_bg = "#0f0f0f"
        phosphor_green = "#00ff41"
        bright_green = "#00ff80"
        accent_gray = "#1a1a1a"
        border_gray = "#2a2a2a"

        # Frame styles
        style.configure("TFrame", background=onyx_black)
        style.configure("Card.TFrame", background=accent_gray, relief="flat", borderwidth=1)
        
        # Label styles with glow effects
        style.configure("TLabel", background=onyx_black, foreground=phosphor_green, font=("Courier New", 10))
        style.configure("Header.TLabel", 
                       font=("Courier New", 20, "bold"), 
                       foreground=bright_green,
                       background=onyx_black)
        style.configure("Glow.Header.TLabel",
                       font=("Courier New", 20, "bold"),
                       foreground=bright_green,
                       background=onyx_black)
        style.configure("Section.TLabel", 
                       font=("Courier New", 13, "bold"), 
                       foreground=bright_green,
                       background=accent_gray)
        style.configure("Stat.TLabel",
                       font=("Courier New", 11),
                       foreground=phosphor_green,
                       background=accent_gray)
        
        # Button styles with rounded appearance
        style.configure("TButton",
                       background=accent_gray,
                       foreground=phosphor_green,
                       font=("Courier New", 10),
                       relief="solid",
                       borderwidth=1,
                       focuscolor="none",
                       padding=8)
        style.map("TButton",
                 background=[("active", border_gray), ("pressed", phosphor_green)],
                 foreground=[("active", bright_green), ("pressed", onyx_black)])
        
        # Entry styles
        style.configure("TEntry",
                       font=("Courier New", 10),
                       fieldbackground=dark_bg,
                       foreground=phosphor_green,
                       borderwidth=1,
                       relief="solid")
        
        # Treeview styles
        style.configure("Treeview",
                       background=dark_bg,
                       fieldbackground=dark_bg,
                       foreground=phosphor_green,
                       rowheight=28,
                       bordercolor=border_gray,
                       borderwidth=1,
                       font=("Courier New", 9))
        style.configure("Treeview.Heading",
                       background=accent_gray,
                       foreground=bright_green,
                       font=("Courier New", 10, "bold"),
                       borderwidth=1)
        style.map("Treeview",
                 background=[("selected", "#1a4d1a")],
                 foreground=[("selected", "#ffffff")])
        
        # Separator styles
        style.configure("TSeparator", background=border_gray)

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
        button.configure(width=28)
        return button

    def create_glow_label(self, parent, text):
        """Create a label with glow effect using Canvas."""
        canvas = Canvas(parent, width=300, height=50, bg="#0a0a0a", highlightthickness=0)
        canvas.pack(pady=10)
        
        # Draw glow effect (multiple overlaid text with transparency)
        for i in range(5, 0, -1):
            alpha = int(255 * (0.2 / i))
            canvas.create_text(150, 25, text=text, font=("Courier New", 20, "bold"),
                             fill="#00ff41", activefill="#00ff80")
        
        canvas.create_text(150, 25, text=text, font=("Courier New", 20, "bold"),
                          fill="#00ff80", activefill="#00ff41")
        return canvas

    def show_notification(self, message, duration=3000):
        """Display a notification in the bottom right corner."""
        if self.notification_after_id:
            self.root.after_cancel(self.notification_after_id)
        
        if not self.notification_label or not self.notification_label.winfo_exists():
            self.notification_label = tk.Label(
                self.root,
                text=message,
                bg="#1a4d1a",
                fg="#00ff41",
                font=("Courier New", 10),
                padx=15,
                pady=10,
                relief="solid",
                borderwidth=1
            )
            self.notification_label.place(relx=0.98, rely=0.98, anchor="se")
        else:
            self.notification_label.config(text=message)
        
        self.notification_after_id = self.root.after(duration, self.hide_notification)

    def hide_notification(self):
        """Hide the notification label."""
        if self.notification_label and self.notification_label.winfo_exists():
            self.notification_label.place_forget()

    def validate_score_input(self, entry_widget, var):
        """Highlight entry red if invalid score format."""
        try:
            float(var.get())
            entry_widget.configure(style="TEntry")
            return True
        except ValueError:
            if var.get().strip():  # Only highlight if there's text
                entry_widget.configure(style="Invalid.TEntry")
            return False

    def on_search_change(self, *args):
        """Handle search text changes for live filtering."""
        if self.current_page == "Records":
            self.refresh_student_table_with_filter()

    # ----------------------------------------------------------------------
    # Authentication and Login Screen
    # ----------------------------------------------------------------------
    def create_login_screen(self):
        """Render the login screen before allowing access to the application."""
        self.clear_root()

        # Add invalid entry style for error highlighting
        style = ttk.Style(self.root)
        style.configure("Invalid.TEntry",
                       font=("Courier New", 10),
                       fieldbackground="#330000",
                       foreground="#ff4444",
                       borderwidth=2,
                       relief="solid")

        login_frame = ttk.Frame(self.root, padding=(40, 40, 40, 40))
        login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.create_neon_label(login_frame, "▶ early access ◀", style="Header.TLabel").grid(row=0, column=0, columnspan=2, pady=(0, 30))
        
        self.create_neon_label(login_frame, "Username:").grid(row=1, column=0, sticky="w", padx=10, pady=8)
        username_entry = ttk.Entry(login_frame, textvariable=self.username_var, font=("Courier New", 12), width=32)
        username_entry.grid(row=1, column=1, pady=8, padx=10)

        self.create_neon_label(login_frame, "Password:").grid(row=2, column=0, sticky="w", padx=10, pady=8)
        password_entry = ttk.Entry(login_frame, textvariable=self.password_var, show="•", font=("Courier New", 12), width=32)
        password_entry.grid(row=2, column=1, pady=8, padx=10)

        auth_hint = ttk.Label(login_frame, text="» Default: tes / 1234", font=("Courier New", 9), foreground="#00ff41", background="#0a0a0a")
        auth_hint.grid(row=3, column=0, columnspan=2, pady=(20, 30))

        login_button = ttk.Button(login_frame, text="[ ENTER SYSTEM ]", command=self.verify_login)
        login_button.grid(row=4, column=0, columnspan=2, pady=10)

        username_entry.focus()

    def verify_login(self):
        """Validate login credentials and load the main interface if authenticated."""
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        if username == "tes" and password == "1234":
            self.create_main_interface()
            return

        messagebox.showerror("ACCESS DENIED", "Invalid username or password.\nPlease try again.")

    # ----------------------------------------------------------------------
    # Main Interface Construction
    # ----------------------------------------------------------------------
    def create_main_interface(self):
        """Build the main application frame with sidebar and default dashboard view."""
        self.clear_root()

        root_container = ttk.Frame(self.root)
        root_container.pack(fill="both", expand=True)

        sidebar_frame = ttk.Frame(root_container, width=280, padding=(16, 16, 16, 16))
        sidebar_frame.pack(side="left", fill="y")
        sidebar_frame.pack_propagate(False)

        content_frame = ttk.Frame(root_container, padding=(20, 20, 20, 20))
        content_frame.pack(side="right", fill="both", expand=True)

        self.sidebar_frame = sidebar_frame
        self.content_frame = content_frame

        self.create_neon_label(sidebar_frame, "◆early access◆", style="Header.TLabel").pack(pady=(0, 30), anchor="w")
        self.create_neon_label(sidebar_frame, "► NAVIGATION", style="Section.TLabel").pack(anchor="w", pady=(0, 16))

        self.create_sidebar_button(sidebar_frame, "📊 Overview", self.show_dashboard).pack(fill="x", pady=10)
        self.create_sidebar_button(sidebar_frame, "📝 Master Data", self.show_student_database).pack(fill="x", pady=10)
        self.create_sidebar_button(sidebar_frame, "📈 Analytics", self.show_statistics_analysis).pack(fill="x", pady=10)
        self.create_sidebar_button(sidebar_frame, "💾 Export Report", self.show_export_dialog).pack(fill="x", pady=10)
        
        ttk.Separator(sidebar_frame, orient="horizontal").pack(fill="x", pady=20)
        self.create_neon_label(sidebar_frame, "► STATUS", style="Section.TLabel").pack(anchor="w", pady=(0, 10))
        self.create_neon_label(sidebar_frame, f"Records: {len(self.student_data)}", style="TLabel").pack(anchor="w", pady=4)

        self.show_dashboard()

    # ----------------------------------------------------------------------
    # Overview Page (Dashboard)
    # ----------------------------------------------------------------------
    def show_dashboard(self):
        """Render the dashboard summary page with prominent visual cards and icons."""
        self.clear_content_area()
        self.current_page = "Overview"

        # Create scrollable frame for large content
        main_container = ttk.Frame(self.content_frame)
        main_container.pack(fill="both", expand=True)

        header = self.create_neon_label(main_container, "▶ DASHBOARD OVERVIEW ◀", style="Header.TLabel")
        header.pack(anchor="w", pady=(0, 20))

        subtitle = self.create_neon_label(main_container, "Real-time student performance metrics", style="TLabel")
        subtitle.pack(anchor="w", pady=(0, 30))

        # Statistics Cards with Icons
        stats_frame = ttk.Frame(main_container)
        stats_frame.pack(fill="x", pady=(0, 30))

        total = len(self.student_data)
        average = self.calculate_average()
        high = self.calculate_highest()
        low = self.calculate_lowest()
        passed = sum(1 for r in self.student_data if r.get("Score", 0) >= self.pass_threshold)

        stat_data = [
            ("👥 Total Students", str(total)),
            ("📊 Average Score", f"{average:.2f}" if average is not None else "N/A"),
            ("🏆 Highest Score", str(high) if high is not None else "N/A"),
            ("📉 Lowest Score", str(low) if low is not None else "N/A"),
            ("✅ Pass Rate", f"{(passed/total*100):.1f}%" if total > 0 else "0%"),
        ]

        for i, (label, value) in enumerate(stat_data):
            card = ttk.Frame(stats_frame, style="Card.TFrame", padding=(20, 20, 20, 20))
            card.pack(side="left", expand=True, fill="both", padx=10)
            
            label_widget = self.create_neon_label(card, label, style="Section.TLabel")
            label_widget.pack(anchor="w", pady=(0, 15))
            
            value_widget = self.create_neon_label(card, value, style="Stat.TLabel")
            value_widget.pack(anchor="w", font=("Courier New", 18, "bold"), foreground="#00ff80")

        # Student Table Section
        table_frame = ttk.Frame(main_container, padding=(0, 0, 0, 0))
        table_frame.pack(fill="both", expand=True, pady=(20, 0))

        self.create_neon_label(table_frame, "📋 Student Records Database", style="Section.TLabel").pack(anchor="w", pady=(0, 15))
        self.create_student_table(table_frame)

    # ----------------------------------------------------------------------
    # Records Page (Master Data)
    # ----------------------------------------------------------------------
    def show_student_database(self):
        """Render the student database management page with form beside table."""
        self.clear_content_area()
        self.current_page = "Records"

        header = self.create_neon_label(self.content_frame, "▶ MASTER DATA EDITOR ◀", style="Header.TLabel")
        header.pack(anchor="w", pady=(0, 20))

        # Add search bar
        search_frame = ttk.Frame(self.content_frame)
        search_frame.pack(fill="x", pady=(0, 20))
        
        self.create_neon_label(search_frame, "🔍 Search Student:", style="TLabel").pack(side="left", padx=(0, 10))
        search_entry = ttk.Entry(search_frame, textvariable=self.search_var, font=("Courier New", 11), width=40)
        search_entry.pack(side="left", fill="x", expand=True)

        # Main container for form and table side-by-side
        main_layout = ttk.Frame(self.content_frame)
        main_layout.pack(fill="both", expand=True, pady=(0, 0))

        # Form on the left
        form_frame = ttk.Frame(main_layout, padding=(16, 16, 16, 16), width=400)
        form_frame.pack(side="left", fill="both", padx=(0, 20))
        form_frame.pack_propagate(False)

        self.create_neon_label(form_frame, "✏️ Student Record Data", style="Section.TLabel").pack(anchor="w", pady=(0, 20))
        
        # Name field
        self.create_neon_label(form_frame, "Name:", style="TLabel").pack(anchor="w", pady=(10, 4))
        ttk.Entry(form_frame, textvariable=self.form_name, font=("Courier New", 11), width=35).pack(anchor="w", pady=(0, 12))
        
        # Class field
        self.create_neon_label(form_frame, "Class:", style="TLabel").pack(anchor="w", pady=(10, 4))
        ttk.Entry(form_frame, textvariable=self.form_class, font=("Courier New", 11), width=35).pack(anchor="w", pady=(0, 12))
        
        # Score field with validation
        self.create_neon_label(form_frame, "Score (0-100):", style="TLabel").pack(anchor="w", pady=(10, 4))
        score_entry = ttk.Entry(form_frame, textvariable=self.form_score, font=("Courier New", 11), width=35)
        score_entry.pack(anchor="w", pady=(0, 12))
        self.form_score.trace("w", lambda *args: self.validate_score_input(score_entry, self.form_score))
        
        # Status field (read-only, auto-calculated)
        self.create_neon_label(form_frame, "Status (Auto):", style="TLabel").pack(anchor="w", pady=(10, 4))
        status_entry = ttk.Entry(form_frame, textvariable=self.form_status, font=("Courier New", 11), width=35, state="readonly")
        status_entry.pack(anchor="w", pady=(0, 20))

        # Form buttons
        button_area = ttk.Frame(form_frame)
        button_area.pack(fill="x", pady=(20, 0))
        ttk.Button(button_area, text="[ + ADD ]", command=self.add_record_from_form).pack(side="left", padx=5)
        ttk.Button(button_area, text="[ ✏ UPDATE ]", command=self.update_selected_record).pack(side="left", padx=5)
        ttk.Button(button_area, text="[ ✕ DELETE ]", command=self.delete_selected_record).pack(side="left", padx=5)

        # Table on the right
        table_frame = ttk.Frame(main_layout, padding=(16, 0, 0, 0))
        table_frame.pack(side="right", fill="both", expand=True)

        self.create_neon_label(table_frame, "📊 Student List", style="Section.TLabel").pack(anchor="w", pady=(0, 15))
        self.create_student_table(table_frame)

    def create_student_table(self, parent):
        """Create or refresh a Treeview widget displaying student records."""
        if hasattr(self, "student_table") and self.student_table.winfo_exists():
            self.student_table.destroy()

        columns = ("Name", "Class", "Score", "Status")
        self.student_table = ttk.Treeview(parent, columns=columns, show="headings", selectmode="browse", height=14)
        self.student_table.pack(fill="both", expand=True)

        for column in columns:
            self.student_table.heading(column, text=column)
            self.student_table.column(column, anchor="center", width=140)

        self.refresh_student_table()
        self.student_table.bind("<ButtonRelease-1>", self.bind_table_selection)

    def refresh_student_table(self):
        """Update the Treeview rows to reflect the latest dataset."""
        if not hasattr(self, "student_table"):
            return

        self.student_table.delete(*self.student_table.get_children())
        for record in self.student_data:
            self.student_table.insert("", "end", values=(record["Name"], record["Class"], record["Score"], record["Status"]))

    def refresh_student_table_with_filter(self):
        """Update the table with search filter applied."""
        if not hasattr(self, "student_table"):
            return

        self.student_table.delete(*self.student_table.get_children())
        search_term = self.search_var.get().lower()

        for record in self.student_data:
            if search_term in record["Name"].lower() or search_term in record["Class"].lower():
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
        # Status is auto-calculated based on score, so we don't set it from table
        try:
            score = float(values[2])
            status = "Pass" if score >= self.pass_threshold else "Fail"
            self.form_status.set(status)
        except (ValueError, IndexError):
            self.form_status.set("Unknown")

    def add_record_from_form(self):
        """Validate the student input form and add a new record."""
        name = self.form_name.get().strip()
        class_name = self.form_class.get().strip()
        score_text = self.form_score.get().strip()

        if not name or not class_name or not score_text:
            messagebox.showwarning("Incomplete Data", "Name, class, and score are required to add a new record.")
            return

        try:
            score = float(score_text)
            if not (0 <= score <= 100):
                messagebox.showwarning("Invalid Score", "Score must be between 0 and 100.")
                return
        except ValueError:
            messagebox.showwarning("Invalid Score", "Score must be a valid number.")
            return

        # Auto-determine status based on score
        status = "Pass" if score >= self.pass_threshold else "Fail"

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

        if not name or not class_name or not score_text:
            messagebox.showwarning("Incomplete Data", "Name, class, and score are required to update the record.")
            return

        try:
            score = float(score_text)
            if not (0 <= score <= 100):
                messagebox.showwarning("Invalid Score", "Score must be between 0 and 100.")
                return
        except ValueError:
            messagebox.showwarning("Invalid Score", "Score must be a valid number.")
            return

        # Auto-determine status based on score
        status = "Pass" if score >= self.pass_threshold else "Fail"

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
        self.search_var.set("")

    # ----------------------------------------------------------------------
    # Analytics Page
    # ----------------------------------------------------------------------
    def show_statistics_analysis(self):
        """Render the statistics page with dynamic calculations and bar chart."""
        self.clear_content_area()
        self.current_page = "Analytics"

        header = self.create_neon_label(self.content_frame, "▶ ANALYTICS DASHBOARD ◀", style="Header.TLabel")
        header.pack(anchor="w", pady=(0, 20))

        stats_frame = ttk.Frame(self.content_frame)
        stats_frame.pack(fill="x", pady=(0, 20))

        stats = self.calculate_statistics()
        for label, value in stats.items():
            card = ttk.Frame(stats_frame, style="Card.TFrame", padding=(16, 16, 16, 16))
            card.pack(side="left", expand=True, fill="x", padx=10)
            self.create_neon_label(card, label, style="Section.TLabel").pack(anchor="w")
            self.create_neon_label(card, value, style="Stat.TLabel").pack(anchor="w", pady=(10, 0), font=("Courier New", 14, "bold"), foreground="#00ff80")

        # Pass/Fail Distribution Chart
        chart_frame = ttk.Frame(self.content_frame, style="Card.TFrame", padding=(16, 16, 16, 16))
        chart_frame.pack(fill="both", expand=True, pady=(20, 0))

        self.create_neon_label(chart_frame, "📊 Pass/Fail Distribution", style="Section.TLabel").pack(anchor="w", pady=(0, 20))
        
        self.create_pass_fail_chart(chart_frame)

    def create_pass_fail_chart(self, parent):
        """Create a bar chart showing pass/fail statistics."""
        if not MATPLOTLIB_AVAILABLE:
            label = ttk.Label(parent, text="[Chart visualization requires matplotlib]\nMatplotlib not installed. Data shown below:",
                            foreground="#ff6666", background="#0a0a0a", font=("Courier New", 10))
            label.pack(pady=20)
            self.create_statistics_table(parent)
            return

        passed = sum(1 for r in self.student_data if r.get("Score", 0) >= self.pass_threshold)
        failed = len(self.student_data) - passed

        fig, ax = plt.subplots(figsize=(10, 5), facecolor="#0f0f0f", edgecolor="#00ff41")
        ax.set_facecolor("#0a0a0a")

        categories = ["PASSED", "FAILED"]
        values = [passed, failed]
        colors = ["#00ff41", "#ff4444"]

        bars = ax.bar(categories, values, color=colors, edgecolor="#00ff80", linewidth=2, width=0.6)
        
        ax.set_ylabel("Number of Students", color="#00ff41", fontsize=11, fontweight="bold")
        ax.set_title(f"Pass/Fail Analysis (Threshold: {self.pass_threshold})", color="#00ff80", fontsize=13, fontweight="bold", pad=20)
        ax.tick_params(colors="#00ff41", labelsize=10)
        ax.spines["bottom"].set_color("#00ff41")
        ax.spines["left"].set_color("#00ff41")
        ax.spines["top"].set_visible(False)
        ax.spines["right"].set_visible(False)
        
        # Add value labels on bars
        for bar, value in zip(bars, values):
            height = bar.get_height()
            ax.text(bar.get_x() + bar.get_width()/2., height,
                   f"{int(value)}", ha="center", va="bottom", color="#00ff41", fontweight="bold", fontsize=12)

        canvas = FigureCanvasTkAgg(fig, master=parent)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True, pady=(0, 20))

    def create_statistics_table(self, parent):
        """Create a read-only score distribution table for quick analysis."""
        columns = ("Name", "Score", "Status")
        table = ttk.Treeview(parent, columns=columns, show="headings", selectmode="none", height=12)
        table.pack(fill="both", expand=True)

        for column in columns:
            table.heading(column, text=column)
            table.column(column, anchor="center", width=200)

        for record in self.student_data:
            table.insert("", "end", values=(record["Name"], record["Score"], record["Status"]))

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
            "👥 Total Students": str(total),
            "📊 Average Score": f"{average:.2f}" if average is not None else "N/A",
            "📈 Median Score": f"{median:.2f}" if median is not None else "N/A",
            "🏆 Highest Score": str(highest) if highest is not None else "N/A",
            "📉 Lowest Score": str(lowest) if lowest is not None else "N/A",
        }

    # ----------------------------------------------------------------------
    # Export Functionality
    # ----------------------------------------------------------------------
    def show_export_dialog(self):
        """Show export options dialog."""
        export_window = Toplevel(self.root)
        export_window.title("Export Report")
        export_window.geometry("400x300")
        export_window.configure(bg="#0a0a0a")

        ttk.Label(export_window, text="▶ EXPORT OPTIONS ◀", style="Header.TLabel").pack(pady=20)

        ttk.Button(export_window, text="[ 📄 Export as PDF ]", command=self.export_to_pdf).pack(fill="x", padx=20, pady=10)
        ttk.Button(export_window, text="[ 📊 Export as JSON ]", command=self.export_to_json).pack(fill="x", padx=20, pady=10)

        ttk.Button(export_window, text="[ ✕ Close ]", command=export_window.destroy).pack(fill="x", padx=20, pady=10)

    def export_to_pdf(self):
        """Export student records to PDF file."""
        if not REPORTLAB_AVAILABLE:
            messagebox.showerror("Export Error", "ReportLab library not installed.\nInstall it with: pip install reportlab")
            return

        try:
            filename = f"student_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = self.database_path.parent / filename

            doc = SimpleDocTemplate(str(filepath), pagesize=letter)
            elements = []

            # Title
            styles = getSampleStyleSheet()
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=24,
                textColor=colors.HexColor("#00ff41"),
                spaceAfter=30,
                alignment=1
            )
            elements.append(Paragraph("STUDENT GRADE REPORT", title_style))

            # Summary section
            summary_style = ParagraphStyle(
                'CustomNormal',
                parent=styles['Normal'],
                fontSize=11,
                textColor=colors.HexColor("#00ff41"),
                spaceAfter=12
            )
            avg = self.calculate_average()
            summary_text = f"""
            <b>Report Generated:</b> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}<br/>
            <b>Total Students:</b> {len(self.student_data)}<br/>
            <b>Average Score:</b> {avg:.2f if avg else 'N/A'}<br/>
            <b>Highest Score:</b> {self.calculate_highest() or 'N/A'}<br/>
            <b>Lowest Score:</b> {self.calculate_lowest() or 'N/A'}
            """
            elements.append(Paragraph(summary_text, summary_style))
            elements.append(Spacer(1, 20))

            # Data table
            data = [["Name", "Class", "Score", "Status"]]
            for record in self.student_data:
                data.append([
                    record["Name"],
                    record["Class"],
                    str(record["Score"]),
                    record["Status"]
                ])

            table = Table(data)
            table.setStyle(TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1a1a1a")),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.HexColor("#00ff41")),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Courier-Bold"),
                ("FONTSIZE", (0, 0), (-1, 0), 12),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.HexColor("#0f0f0f")),
                ("TEXTCOLOR", (0, 1), (-1, -1), colors.HexColor("#00ff41")),
                ("FONTNAME", (0, 1), (-1, -1), "Courier"),
                ("FONTSIZE", (0, 1), (-1, -1), 10),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.HexColor("#0f0f0f"), colors.HexColor("#1a1a1a")]),
                ("GRID", (0, 0), (-1, -1), 1, colors.HexColor("#333333")),
            ]))
            elements.append(table)

            doc.build(elements)
            messagebox.showinfo("Export Success", f"Report exported successfully!\n\nFile: {filename}")
            self.show_notification(f"✓ PDF exported: {filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export PDF:\n{str(e)}")

    def export_to_json(self):
        """Export student records to JSON file."""
        try:
            filename = f"student_data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
            filepath = self.database_path.parent / filename

            export_data = {
                "export_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "total_records": len(self.student_data),
                "students": self.student_data,
                "statistics": {
                    "average": self.calculate_average(),
                    "median": self.calculate_median(),
                    "highest": self.calculate_highest(),
                    "lowest": self.calculate_lowest(),
                }
            }

            with filepath.open("w", encoding="utf-8") as f:
                json.dump(export_data, f, indent=4)

            messagebox.showinfo("Export Success", f"Data exported successfully!\n\nFile: {filename}")
            self.show_notification(f"✓ JSON exported: {filename}")

        except Exception as e:
            messagebox.showerror("Export Error", f"Failed to export JSON:\n{str(e)}")

    # ----------------------------------------------------------------------
    # Internal UI Helpers
    # ----------------------------------------------------------------------
    def clear_content_area(self):
        """Clear only the right-side content area while preserving the sidebar."""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def refresh_statistics(self):
        """Refresh statistics widgets when underlying data changes."""
        if self.current_page == "Analytics":
            self.show_statistics_analysis()
        elif self.current_page == "Overview":
            self.show_dashboard()


if __name__ == "__main__":
    root = tk.Tk()
    app = ProTestingApp(root)
    root.mainloop()
