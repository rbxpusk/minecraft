"""Settings and configuration tab"""
import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
from ui_components import ModernTheme, ModernButton, ModernEntry, Card

class SettingsTab:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent, bg=ModernTheme.DARK['bg'])
        self.setup_ui()
    
    def setup_ui(self):
        props_label = tk.Label(self.frame, text="⚙️ server.properties",
                              font=('Segoe UI', 12, 'bold'),
                              bg=ModernTheme.DARK['bg'],
                              fg=ModernTheme.DARK['accent'])
        props_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        props_card = Card(self.frame)
        props_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.props_text = scrolledtext.ScrolledText(
            props_card, height=20,
            bg=ModernTheme.DARK['surface_light'],
            fg=ModernTheme.DARK['text'],
            font=('Consolas', 9), relief='flat'
        )
        self.props_text.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        actions = Card(self.frame)
        actions.pack(fill=tk.X, padx=10, pady=10)
        
        btn_container = tk.Frame(actions, bg=ModernTheme.DARK['surface'])
        btn_container.pack(pady=10)
        
        buttons = [
            ("📂 Load", self.load_properties, 'primary'),
            ("💾 Save", self.save_properties, 'success'),
            ("🔄 Restart Server", self.restart_server, 'warning'),
        ]
        
        for text, cmd, style in buttons:
            ModernButton(btn_container, text=text, command=cmd, style=style).pack(
                side=tk.LEFT, padx=5
            )
        
        quick_label = tk.Label(self.frame, text="⚡ Quick Settings",
                              font=('Segoe UI', 12, 'bold'),
                              bg=ModernTheme.DARK['bg'],
                              fg=ModernTheme.DARK['accent'])
        quick_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        quick_card = Card(self.frame)
        quick_card.pack(fill=tk.X, padx=10, pady=5)
        
        quick_container = tk.Frame(quick_card, bg=ModernTheme.DARK['surface'])
        quick_container.pack(pady=15, padx=15)
        
        settings = [
            ("Max Players:", "max-players", "20"),
            ("View Distance:", "view-distance", "10"),
            ("Difficulty:", "difficulty", "normal"),
            ("Gamemode:", "gamemode", "survival"),
        ]
        
        self.setting_entries = {}
        
        for i, (label, key, default) in enumerate(settings):
            tk.Label(quick_container, text=label, bg=ModernTheme.DARK['surface'],
                    fg=ModernTheme.DARK['text'], font=('Segoe UI', 10)).grid(
                row=i//2, column=(i%2)*2, padx=10, pady=5, sticky='w'
            )
            
            entry = ModernEntry(quick_container, width=15)
            entry.insert(0, default)
            entry.grid(row=i//2, column=(i%2)*2+1, padx=10, pady=5)
            
            self.setting_entries[key] = entry
    
    def load_properties(self):
        if not self.app.ssh:
            return
        
        def load():
            try:
                output, _ = self.app.ssh.execute("cat /root/minecraft/server.properties")
                self.props_text.delete(1.0, tk.END)
                self.props_text.insert(1.0, output)
                self.app.log("✅ Properties loaded")
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=load, daemon=True).start()
    
    def save_properties(self):
        if not self.app.ssh:
            return
        
        content = self.props_text.get(1.0, tk.END)
        
        def save():
            try:
                sftp = self.app.ssh.get_sftp()
                with sftp.open('/root/minecraft/server.properties', 'w') as f:
                    f.write(content)
                sftp.close()
                self.app.log("✅ Properties saved")
                messagebox.showinfo("Success", "Restart server to apply changes")
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=save, daemon=True).start()
    
    def restart_server(self):
        if self.app.server:
            self.app.dashboard.restart_server()
