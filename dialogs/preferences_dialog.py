"""Preferences and settings dialog"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from ui_components import ModernTheme

class PreferencesDialog:
    def __init__(self, parent, app):
        self.app = app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Preferences")
        self.dialog.geometry("600x700")
        self.dialog.configure(bg=ModernTheme.DARK['bg'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_ui()
    
    def create_ui(self):
        # Header
        header = tk.Frame(self.dialog, bg=ModernTheme.DARK['surface'],
                         highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="⚙️ Preferences",
                font=('Segoe UI', 18, 'bold'),
                bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        # Scrollable content
        canvas = tk.Canvas(self.dialog, bg=ModernTheme.DARK['bg'],
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(self.dialog, orient=tk.VERTICAL,
                                command=canvas.yview)
        
        content = tk.Frame(canvas, bg=ModernTheme.DARK['bg'])
        
        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=20, pady=20)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=20)
        
        # Connection settings
        self.create_section(content, "🔌 Connection")
        
        self.remember_creds = tk.BooleanVar(value=self.app.prefs.get('remember_credentials', False))
        tk.Checkbutton(content, text="Remember server credentials",
                      variable=self.remember_creds,
                      bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                      selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 10)).pack(anchor='w', padx=20, pady=5)
        
        self.auto_connect = tk.BooleanVar(value=self.app.prefs.get('auto_connect', False))
        tk.Checkbutton(content, text="Auto-connect to last server on startup",
                      variable=self.auto_connect,
                      bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                      selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 10)).pack(anchor='w', padx=20, pady=5)
        
        # UI settings
        self.create_section(content, "🎨 Interface")
        
        self.auto_fetch = tk.BooleanVar(value=self.app.prefs.get('auto_fetch', True))
        tk.Checkbutton(content, text="Auto-fetch data when switching tabs",
                      variable=self.auto_fetch,
                      bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                      selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 10)).pack(anchor='w', padx=20, pady=5)
        
        self.auto_refresh = tk.BooleanVar(value=self.app.prefs.get('auto_refresh', False))
        tk.Checkbutton(content, text="Auto-refresh logs",
                      variable=self.auto_refresh,
                      bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                      selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 10)).pack(anchor='w', padx=20, pady=5)
        
        refresh_frame = tk.Frame(content, bg=ModernTheme.DARK['bg'])
        refresh_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(refresh_frame, text="Refresh interval (seconds):",
                bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        self.refresh_interval = tk.Spinbox(refresh_frame, from_=1, to=60,
                                          bg=ModernTheme.DARK['surface_light'],
                                          fg=ModernTheme.DARK['text'],
                                          font=('Segoe UI', 10), width=10)
        self.refresh_interval.delete(0, tk.END)
        self.refresh_interval.insert(0, self.app.prefs.get('refresh_interval', 5))
        self.refresh_interval.pack(side=tk.LEFT, padx=10)
        
        console_frame = tk.Frame(content, bg=ModernTheme.DARK['bg'])
        console_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(console_frame, text="Console lines:",
                bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        self.console_lines = tk.Spinbox(console_frame, from_=50, to=500,
                                       increment=50,
                                       bg=ModernTheme.DARK['surface_light'],
                                       fg=ModernTheme.DARK['text'],
                                       font=('Segoe UI', 10), width=10)
        self.console_lines.delete(0, tk.END)
        self.console_lines.insert(0, self.app.prefs.get('console_lines', 100))
        self.console_lines.pack(side=tk.LEFT, padx=10)
        
        # Server settings
        self.create_section(content, "🎮 Server")
        
        memory_frame = tk.Frame(content, bg=ModernTheme.DARK['bg'])
        memory_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(memory_frame, text="Default memory allocation:",
                bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                font=('Segoe UI', 10)).pack(side=tk.LEFT)
        
        self.default_memory = ttk.Combobox(memory_frame,
                                          values=['2G', '4G', '6G', '8G', '12G', '16G'],
                                          state='readonly', width=10)
        self.default_memory.set(self.app.prefs.get('default_memory', '4G'))
        self.default_memory.pack(side=tk.LEFT, padx=10)
        
        # Paths
        self.create_section(content, "📁 Paths")
        
        mods_frame = tk.Frame(content, bg=ModernTheme.DARK['bg'])
        mods_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(mods_frame, text="Local mods folder:",
                bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                font=('Segoe UI', 10)).pack(anchor='w')
        
        path_frame = tk.Frame(mods_frame, bg=ModernTheme.DARK['bg'])
        path_frame.pack(fill=tk.X, pady=5)
        
        self.mods_path = tk.Entry(path_frame, bg=ModernTheme.DARK['surface_light'],
                                 fg=ModernTheme.DARK['text'], font=('Segoe UI', 9))
        self.mods_path.insert(0, self.app.prefs.get('local_mods_path', ''))
        self.mods_path.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        tk.Button(path_frame, text="Browse", command=self.browse_mods,
                 bg=ModernTheme.DARK['accent'], fg='white',
                 font=('Segoe UI', 9), relief='flat',
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        backup_frame = tk.Frame(content, bg=ModernTheme.DARK['bg'])
        backup_frame.pack(fill=tk.X, padx=20, pady=5)
        
        tk.Label(backup_frame, text="Backup folder:",
                bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                font=('Segoe UI', 10)).pack(anchor='w')
        
        backup_path_frame = tk.Frame(backup_frame, bg=ModernTheme.DARK['bg'])
        backup_path_frame.pack(fill=tk.X, pady=5)
        
        self.backup_path = tk.Entry(backup_path_frame, bg=ModernTheme.DARK['surface_light'],
                                   fg=ModernTheme.DARK['text'], font=('Segoe UI', 9))
        self.backup_path.insert(0, self.app.prefs.get('backup_path', ''))
        self.backup_path.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=5)
        
        tk.Button(backup_path_frame, text="Browse", command=self.browse_backup,
                 bg=ModernTheme.DARK['accent'], fg='white',
                 font=('Segoe UI', 9), relief='flat',
                 padx=15, pady=5, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Data management
        self.create_section(content, "🗑️ Data Management")
        
        data_frame = tk.Frame(content, bg=ModernTheme.DARK['bg'])
        data_frame.pack(fill=tk.X, padx=20, pady=10)
        
        tk.Button(data_frame, text="Clear Saved Credentials",
                 command=self.clear_credentials,
                 bg=ModernTheme.DARK['error'], fg='white',
                 font=('Segoe UI', 10), relief='flat',
                 padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(data_frame, text="Reset All Preferences",
                 command=self.reset_preferences,
                 bg=ModernTheme.DARK['error'], fg='white',
                 font=('Segoe UI', 10), relief='flat',
                 padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Buttons
        btn_frame = tk.Frame(self.dialog, bg=ModernTheme.DARK['surface'],
                            highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        btn_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        btn_container = tk.Frame(btn_frame, bg=ModernTheme.DARK['surface'])
        btn_container.pack(pady=15)
        
        tk.Button(btn_container, text="💾 Save", command=self.save,
                 bg=ModernTheme.DARK['success'], fg='white',
                 font=('Segoe UI', 11, 'bold'), relief='flat',
                 padx=30, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_container, text="Cancel", command=self.dialog.destroy,
                 bg=ModernTheme.DARK['surface_light'], fg=ModernTheme.DARK['text'],
                 font=('Segoe UI', 11), relief='flat',
                 padx=30, pady=10, cursor='hand2').pack(side=tk.LEFT, padx=5)
    
    def create_section(self, parent, title):
        """Create a section header"""
        tk.Label(parent, text=title,
                font=('Segoe UI', 12, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(anchor='w', padx=15, pady=(15, 5))
        
        separator = tk.Frame(parent, bg=ModernTheme.DARK['border'], height=1)
        separator.pack(fill=tk.X, padx=20, pady=5)
    
    def browse_mods(self):
        path = filedialog.askdirectory(title="Select Local Mods Folder")
        if path:
            self.mods_path.delete(0, tk.END)
            self.mods_path.insert(0, path)
    
    def browse_backup(self):
        path = filedialog.askdirectory(title="Select Backup Folder")
        if path:
            self.backup_path.delete(0, tk.END)
            self.backup_path.insert(0, path)
    
    def clear_credentials(self):
        if messagebox.askyesno("Confirm", "Clear all saved credentials?"):
            self.app.prefs.credentials = {}
            self.app.prefs.save_preferences()
            messagebox.showinfo("Success", "Credentials cleared!")
    
    def reset_preferences(self):
        if messagebox.askyesno("Confirm", "Reset all preferences to defaults?"):
            self.app.prefs.clear_all()
            messagebox.showinfo("Success", "Preferences reset! Restart the app.")
            self.dialog.destroy()
    
    def save(self):
        """Save all preferences"""
        self.app.prefs.set('remember_credentials', self.remember_creds.get())
        self.app.prefs.set('auto_connect', self.auto_connect.get())
        self.app.prefs.set('auto_fetch', self.auto_fetch.get())
        self.app.prefs.set('auto_refresh', self.auto_refresh.get())
        self.app.prefs.set('refresh_interval', int(self.refresh_interval.get()))
        self.app.prefs.set('console_lines', int(self.console_lines.get()))
        self.app.prefs.set('default_memory', self.default_memory.get())
        self.app.prefs.set('local_mods_path', self.mods_path.get())
        self.app.prefs.set('backup_path', self.backup_path.get())
        
        messagebox.showinfo("Success", "Preferences saved!")
        self.dialog.destroy()
