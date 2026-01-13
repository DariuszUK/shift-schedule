"""
Dialog windows for countdown management and history
"""
import tkinter as tk
from tkinter import ttk, messagebox, colorchooser
from datetime import datetime
from typing import Optional, Callable
from models import Countdown, HistoryEntry


class CountdownDialog:
    """Dialog for adding/editing countdowns"""
    
    def __init__(self, parent, countdown: Optional[Countdown] = None, on_save: Optional[Callable] = None):
        self.countdown = countdown
        self.on_save = on_save
        self.result = None
        
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("Edytuj odliczenie" if countdown else "Dodaj odliczenie")
        self.window.geometry("500x600")
        self.window.resizable(False, False)
        
        self.create_widgets()
        self.load_data()
        
        # Make window modal
        if parent:
            self.window.transient(parent)
            self.window.grab_set()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        row = 0
        
        # Name
        ttk.Label(main_frame, text="Nazwa:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.name_var, width=40).grid(row=row, column=1, pady=5)
        row += 1
        
        # Type
        ttk.Label(main_frame, text="Typ odliczenia:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar(value="TO")
        type_frame = ttk.Frame(main_frame)
        type_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        ttk.Radiobutton(type_frame, text="DO (countdown to)", variable=self.type_var, 
                       value="TO", command=self.on_type_change).pack(side=tk.LEFT)
        ttk.Radiobutton(type_frame, text="OD (countdown from)", variable=self.type_var, 
                       value="FROM", command=self.on_type_change).pack(side=tk.LEFT, padx=10)
        row += 1
        
        # Start datetime (for FROM type)
        ttk.Label(main_frame, text="Data/czas rozpoczęcia:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.start_datetime_var = tk.StringVar()
        self.start_entry = ttk.Entry(main_frame, textvariable=self.start_datetime_var, width=40)
        self.start_entry.grid(row=row, column=1, pady=5)
        ttk.Label(main_frame, text="(Format: YYYY-MM-DD HH:MM:SS)", font=("", 8)).grid(row=row+1, column=1, sticky=tk.W)
        row += 2
        
        # End datetime (for TO type)
        ttk.Label(main_frame, text="Data/czas zakończenia:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.end_datetime_var = tk.StringVar()
        self.end_entry = ttk.Entry(main_frame, textvariable=self.end_datetime_var, width=40)
        self.end_entry.grid(row=row, column=1, pady=5)
        ttk.Label(main_frame, text="(Format: YYYY-MM-DD HH:MM:SS)", font=("", 8)).grid(row=row+1, column=1, sticky=tk.W)
        row += 2
        
        # Enabled
        self.enabled_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Aktywne", variable=self.enabled_var).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Show
        self.show_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Widoczne", variable=self.show_var).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Color
        ttk.Label(main_frame, text="Kolor wyświetlania:").grid(row=row, column=0, sticky=tk.W, pady=5)
        color_frame = ttk.Frame(main_frame)
        color_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.color_var = tk.StringVar(value="#00ffff")
        ttk.Entry(color_frame, textvariable=self.color_var, width=15).pack(side=tk.LEFT)
        self.color_preview = tk.Canvas(color_frame, width=30, height=20, bg=self.color_var.get())
        self.color_preview.pack(side=tk.LEFT, padx=5)
        ttk.Button(color_frame, text="Wybierz...", command=self.choose_color).pack(side=tk.LEFT)
        row += 1
        
        # Alert section
        ttk.Separator(main_frame, orient=tk.HORIZONTAL).grid(row=row, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)
        row += 1
        
        ttk.Label(main_frame, text="ALERTY", font=("", 10, "bold")).grid(row=row, column=0, columnspan=2, pady=5)
        row += 1
        
        # Alert enabled
        self.alert_enabled_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(main_frame, text="Włącz alerty", variable=self.alert_enabled_var).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Alert minutes
        ttk.Label(main_frame, text="Alert (minuty przed):").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.alert_minutes_var = tk.IntVar(value=60)
        ttk.Spinbox(main_frame, from_=1, to=10080, textvariable=self.alert_minutes_var, width=10).grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Alert mode
        ttk.Label(main_frame, text="Tryb alertu:").grid(row=row, column=0, sticky=tk.W, pady=5)
        self.alert_mode_var = tk.StringVar(value="pulse")
        ttk.Combobox(main_frame, textvariable=self.alert_mode_var, 
                    values=["pulse", "blink", "static"], width=15, state="readonly").grid(row=row, column=1, sticky=tk.W, pady=5)
        row += 1
        
        # Alert color
        ttk.Label(main_frame, text="Kolor alertu:").grid(row=row, column=0, sticky=tk.W, pady=5)
        alert_color_frame = ttk.Frame(main_frame)
        alert_color_frame.grid(row=row, column=1, sticky=tk.W, pady=5)
        self.alert_color_var = tk.StringVar(value="#ff0000")
        ttk.Entry(alert_color_frame, textvariable=self.alert_color_var, width=15).pack(side=tk.LEFT)
        self.alert_color_preview = tk.Canvas(alert_color_frame, width=30, height=20, bg=self.alert_color_var.get())
        self.alert_color_preview.pack(side=tk.LEFT, padx=5)
        ttk.Button(alert_color_frame, text="Wybierz...", command=self.choose_alert_color).pack(side=tk.LEFT)
        row += 1
        
        # Buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=row, column=0, columnspan=2, pady=20)
        ttk.Button(button_frame, text="Zapisz", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Anuluj", command=self.cancel).pack(side=tk.LEFT, padx=5)
        
        self.on_type_change()
    
    def on_type_change(self):
        """Handle type change"""
        if self.type_var.get() == "TO":
            self.start_entry.config(state="disabled")
            self.end_entry.config(state="normal")
        else:
            self.start_entry.config(state="normal")
            self.end_entry.config(state="disabled")
    
    def choose_color(self):
        """Choose display color"""
        color = colorchooser.askcolor(self.color_var.get())
        if color[1]:
            self.color_var.set(color[1])
            self.color_preview.config(bg=color[1])
    
    def choose_alert_color(self):
        """Choose alert color"""
        color = colorchooser.askcolor(self.alert_color_var.get())
        if color[1]:
            self.alert_color_var.set(color[1])
            self.alert_color_preview.config(bg=color[1])
    
    def load_data(self):
        """Load countdown data into form"""
        if self.countdown:
            self.name_var.set(self.countdown.name)
            self.type_var.set(self.countdown.type)
            self.start_datetime_var.set(self.countdown.start_datetime or "")
            self.end_datetime_var.set(self.countdown.end_datetime or "")
            self.enabled_var.set(self.countdown.enabled)
            self.show_var.set(self.countdown.show)
            self.color_var.set(self.countdown.color)
            self.color_preview.config(bg=self.countdown.color)
            self.alert_enabled_var.set(self.countdown.alert_enabled)
            self.alert_minutes_var.set(self.countdown.alert_minutes)
            self.alert_mode_var.set(self.countdown.alert_mode)
            self.alert_color_var.set(self.countdown.alert_color)
            self.alert_color_preview.config(bg=self.countdown.alert_color)
            self.on_type_change()
    
    def save(self):
        """Save countdown"""
        name = self.name_var.get().strip()
        if not name:
            messagebox.showerror("Błąd", "Nazwa nie może być pusta")
            return
        
        countdown_type = self.type_var.get()
        start_dt = self.start_datetime_var.get().strip()
        end_dt = self.end_datetime_var.get().strip()
        
        # Validate datetime
        if countdown_type == "FROM" and not start_dt:
            messagebox.showerror("Błąd", "Data/czas rozpoczęcia jest wymagana dla typu OD")
            return
        if countdown_type == "TO" and not end_dt:
            messagebox.showerror("Błąd", "Data/czas zakończenia jest wymagana dla typu DO")
            return
        
        # Validate datetime format
        try:
            if countdown_type == "FROM" and start_dt:
                datetime.strptime(start_dt, "%Y-%m-%d %H:%M:%S")
            if countdown_type == "TO" and end_dt:
                datetime.strptime(end_dt, "%Y-%m-%d %H:%M:%S")
        except ValueError:
            messagebox.showerror("Błąd", "Nieprawidłowy format daty/czasu. Użyj: YYYY-MM-DD HH:MM:SS")
            return
        
        # Create or update countdown
        if self.countdown:
            countdown_id = self.countdown.id
        else:
            countdown_id = None
        
        self.result = Countdown(
            id=countdown_id,
            name=name,
            type=countdown_type,
            start_datetime=start_dt if countdown_type == "FROM" else None,
            end_datetime=end_dt if countdown_type == "TO" else None,
            enabled=self.enabled_var.get(),
            show=self.show_var.get(),
            color=self.color_var.get(),
            alert_enabled=self.alert_enabled_var.get(),
            alert_minutes=self.alert_minutes_var.get(),
            alert_mode=self.alert_mode_var.get(),
            alert_color=self.alert_color_var.get()
        )
        
        if self.on_save:
            self.on_save(self.result)
        
        self.window.destroy()
    
    def cancel(self):
        """Cancel dialog"""
        self.result = None
        self.window.destroy()


class HistoryDialog:
    """Dialog for viewing countdown history"""
    
    def __init__(self, parent, history_entries: list, on_clear: Optional[Callable] = None):
        self.history_entries = history_entries
        self.on_clear = on_clear
        
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("📋 Historia odliczeń")
        self.window.geometry("800x500")
        
        self.create_widgets()
        self.load_history()
        
        # Make window modal
        if parent:
            self.window.transient(parent)
            self.window.grab_set()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Filter/sort frame
        filter_frame = ttk.Frame(main_frame)
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Label(filter_frame, text="Sortuj według:").pack(side=tk.LEFT, padx=5)
        self.sort_var = tk.StringVar(value="ended_at")
        ttk.Combobox(filter_frame, textvariable=self.sort_var, 
                    values=["ended_at", "started_at", "name", "duration_seconds"], 
                    width=15, state="readonly").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(filter_frame, text="Odśwież", command=self.load_history).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Wyczyść historię", command=self.clear_history).pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        columns = ("name", "type", "started", "ended", "duration", "notes")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("name", text="Nazwa")
        self.tree.heading("type", text="Typ")
        self.tree.heading("started", text="Rozpoczęto")
        self.tree.heading("ended", text="Zakończono")
        self.tree.heading("duration", text="Czas trwania")
        self.tree.heading("notes", text="Notatki")
        
        self.tree.column("name", width=150)
        self.tree.column("type", width=60)
        self.tree.column("started", width=150)
        self.tree.column("ended", width=150)
        self.tree.column("duration", width=120)
        self.tree.column("notes", width=200)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Close button
        ttk.Button(main_frame, text="Zamknij", command=self.window.destroy).pack(pady=(10, 0))
    
    def load_history(self):
        """Load history entries into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Sort entries
        sort_by = self.sort_var.get()
        sorted_entries = sorted(self.history_entries, key=lambda h: getattr(h, sort_by), reverse=True)
        
        # Add entries
        for entry in sorted_entries:
            duration = self.format_duration(entry.duration_seconds)
            self.tree.insert("", tk.END, values=(
                entry.name,
                entry.type,
                entry.started_at,
                entry.ended_at,
                duration,
                entry.notes
            ))
    
    def format_duration(self, seconds):
        """Format duration in seconds to human-readable format"""
        days = seconds // 86400
        hours = (seconds % 86400) // 3600
        minutes = (seconds % 3600) // 60
        secs = seconds % 60
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0:
            parts.append(f"{hours}h")
        if minutes > 0:
            parts.append(f"{minutes}m")
        if secs > 0 or not parts:
            parts.append(f"{secs}s")
        
        return " ".join(parts)
    
    def clear_history(self):
        """Clear all history"""
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz wyczyścić całą historię?"):
            if self.on_clear:
                self.on_clear()
            # Clear treeview
            for item in self.tree.get_children():
                self.tree.delete(item)


class ManageCountdownsDialog:
    """Dialog for managing all countdowns"""
    
    def __init__(self, parent, storage, on_refresh: Optional[Callable] = None):
        self.storage = storage
        self.on_refresh = on_refresh
        
        self.window = tk.Toplevel(parent) if parent else tk.Tk()
        self.window.title("⏱️ Zarządzaj odliczeniami")
        self.window.geometry("700x500")
        
        self.create_widgets()
        self.load_countdowns()
        
        # Make window modal
        if parent:
            self.window.transient(parent)
            self.window.grab_set()
    
    def create_widgets(self):
        """Create dialog widgets"""
        # Main frame
        main_frame = ttk.Frame(self.window, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Buttons frame
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(button_frame, text="➕ Dodaj nowe", command=self.add_countdown).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="✏️ Edytuj", command=self.edit_countdown).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🗑️ Usuń", command=self.delete_countdown).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="🔄 Odśwież", command=self.load_countdowns).pack(side=tk.RIGHT, padx=5)
        
        # Treeview
        tree_frame = ttk.Frame(main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tree_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Create treeview
        columns = ("name", "type", "datetime", "enabled", "show", "alert")
        self.tree = ttk.Treeview(tree_frame, columns=columns, show="headings", yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.tree.yview)
        
        self.tree.heading("name", text="Nazwa")
        self.tree.heading("type", text="Typ")
        self.tree.heading("datetime", text="Data/Czas")
        self.tree.heading("enabled", text="Aktywne")
        self.tree.heading("show", text="Widoczne")
        self.tree.heading("alert", text="Alert")
        
        self.tree.column("name", width=150)
        self.tree.column("type", width=60)
        self.tree.column("datetime", width=180)
        self.tree.column("enabled", width=80)
        self.tree.column("show", width=80)
        self.tree.column("alert", width=80)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Bind double-click to edit
        self.tree.bind("<Double-1>", lambda e: self.edit_countdown())
        
        # Close button
        ttk.Button(main_frame, text="Zamknij", command=self.window.destroy).pack(pady=(10, 0))
    
    def load_countdowns(self):
        """Load countdowns into treeview"""
        # Clear existing items
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        # Add countdowns
        for countdown in self.storage.countdowns:
            datetime_str = countdown.end_datetime if countdown.type == "TO" else countdown.start_datetime
            self.tree.insert("", tk.END, values=(
                countdown.name,
                countdown.type,
                datetime_str or "",
                "Tak" if countdown.enabled else "Nie",
                "Tak" if countdown.show else "Nie",
                "Tak" if countdown.alert_enabled else "Nie"
            ), tags=(countdown.id,))
    
    def add_countdown(self):
        """Add new countdown"""
        dialog = CountdownDialog(self.window, countdown=None, on_save=self.on_countdown_save)
        self.window.wait_window(dialog.window)
    
    def edit_countdown(self):
        """Edit selected countdown"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uwaga", "Wybierz odliczenie do edycji")
            return
        
        item = selection[0]
        countdown_id = self.tree.item(item)["tags"][0]
        countdown = self.storage.get_countdown(countdown_id)
        
        if countdown:
            dialog = CountdownDialog(self.window, countdown=countdown, on_save=self.on_countdown_update)
            self.window.wait_window(dialog.window)
    
    def delete_countdown(self):
        """Delete selected countdown"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Uwaga", "Wybierz odliczenie do usunięcia")
            return
        
        if messagebox.askyesno("Potwierdzenie", "Czy na pewno chcesz usunąć to odliczenie?"):
            item = selection[0]
            countdown_id = self.tree.item(item)["tags"][0]
            self.storage.delete_countdown(countdown_id)
            self.load_countdowns()
            
            if self.on_refresh:
                self.on_refresh()
    
    def on_countdown_save(self, countdown: Countdown):
        """Handle countdown save"""
        self.storage.add_countdown(countdown)
        self.load_countdowns()
        
        if self.on_refresh:
            self.on_refresh()
    
    def on_countdown_update(self, countdown: Countdown):
        """Handle countdown update"""
        self.storage.update_countdown(countdown.id, countdown)
        self.load_countdowns()
        
        if self.on_refresh:
            self.on_refresh()
