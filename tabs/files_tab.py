"""Files and backup management tab"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import threading
from ui_components import ModernTheme, ModernButton, Card

class FilesTab:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent, bg=ModernTheme.DARK['bg'])
        self.setup_ui()
    
    def setup_ui(self):
        actions = Card(self.frame)
        actions.pack(fill=tk.X, padx=10, pady=10)
        
        btn_container = tk.Frame(actions, bg=ModernTheme.DARK['surface'])
        btn_container.pack(pady=15)
        
        buttons = [
            ("📂 Browse Files", self.browse_files, 'primary'),
            ("📄 View Logs", self.view_logs, 'primary'),
            ("🗑️ Clear Logs", self.clear_logs, 'warning'),
            ("💾 Backup World", self.backup_world, 'success'),
            ("📋 List Backups", self.list_backups, 'primary'),
        ]
        
        for text, cmd, style in buttons:
            ModernButton(btn_container, text=text, command=cmd, style=style).pack(
                side=tk.LEFT, padx=5
            )
        
        list_label = tk.Label(self.frame, text="📁 Server Files",
                             font=('Segoe UI', 12, 'bold'),
                             bg=ModernTheme.DARK['bg'],
                             fg=ModernTheme.DARK['accent'])
        list_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        list_card = Card(self.frame)
        list_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Name", "Type", "Size", "Date")
        self.tree = ttk.Treeview(list_card, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("Name", width=400)
        self.tree.column("Type", width=100)
        self.tree.column("Size", width=100)
        self.tree.column("Date", width=200)
        
        scrollbar = ttk.Scrollbar(list_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    
    def browse_files(self):
        if not self.app.files:
            return
        
        def browse():
            try:
                files = self.app.files.list_directory()
                self.tree.delete(*self.tree.get_children())
                
                for file in files:
                    self.tree.insert('', tk.END, values=(
                        file['name'], file['type'], file['size'], file['date']
                    ))
                
                self.app.log(f"✅ Found {len(files)} files")
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=browse, daemon=True).start()
    
    def view_logs(self):
        if not self.app.files:
            return
        
        def view():
            try:
                logs = self.app.files.get_logs(100)
                self.app.log("📄 Latest logs:")
                self.app.log(logs)
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=view, daemon=True).start()
    
    def clear_logs(self):
        if not messagebox.askyesno("Confirm", "Clear all logs?"):
            return
        
        def clear():
            try:
                self.app.files.clear_logs()
                self.app.log("✅ Logs cleared")
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=clear, daemon=True).start()
    
    def backup_world(self):
        if not self.app.files:
            return
        
        self.app.log("💾 Creating backup...")
        
        def backup():
            try:
                backup_name = self.app.files.backup_world()
                self.app.log(f"✅ Backup created: {backup_name}")
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=backup, daemon=True).start()
    
    def list_backups(self):
        if not self.app.files:
            return
        
        def list_bkp():
            try:
                backups = self.app.files.list_backups()
                self.tree.delete(*self.tree.get_children())
                
                for backup in backups:
                    self.tree.insert('', tk.END, values=(
                        backup['name'], 'backup', backup['size'], backup['date']
                    ))
                
                self.app.log(f"✅ Found {len(backups)} backups")
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=list_bkp, daemon=True).start()
