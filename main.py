"""Modern Minecraft Server Manager - Main Application"""
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox, filedialog
import threading
from ui_components import ModernTheme, ModernButton, ModernEntry, Card
from ssh_manager import SSHManager
from server_manager import ServerManager
from mod_manager import ModManager
from player_manager import PlayerManager
from file_manager import FileManager
from config import Config
from preferences import Preferences

class MinecraftServerManager:
    def __init__(self, root):
        self.root = root
        self.root.title("Minecraft Server Manager")
        
        # Load preferences
        self.prefs = Preferences()
        
        # Apply window size from preferences
        window_size = self.prefs.get('window_size', '1600x900')
        self.root.geometry(window_size)
        self.root.configure(bg=ModernTheme.DARK['bg'])
        
        # Save window size on close
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        ModernTheme.apply_style()
        
        self.ssh = None
        self.server = None
        self.mods = None
        self.players = None
        self.files = None
        
        self.setup_ui()
        self.root.after(500, self.prompt_connection)
    
    def setup_ui(self):
        self.create_header()
        self.create_main_content()
    
    def create_header(self):
        header = Card(self.root)
        header.pack(fill=tk.X, padx=0, pady=0)
        
        content = tk.Frame(header, bg=ModernTheme.DARK['surface'])
        content.pack(fill=tk.X, padx=20, pady=15)
        
        title = tk.Label(content, text="⛏️ MINECRAFT SERVER MANAGER",
                        font=('Segoe UI', 24, 'bold'),
                        bg=ModernTheme.DARK['surface'], 
                        fg=ModernTheme.DARK['accent'])
        title.pack(side=tk.LEFT)
        
        # Logout button
        self.logout_btn = tk.Button(content, text="🚪 Logout",
                            command=self.logout,
                            bg=ModernTheme.DARK['error'], fg='white',
                            font=('Segoe UI', 10, 'bold'), relief='flat',
                            padx=15, pady=8, cursor='hand2', borderwidth=0,
                            state=tk.DISABLED)
        self.logout_btn.pack(side=tk.RIGHT, padx=5)
        
        # Help button
        help_btn = tk.Button(content, text="❓ Help",
                            command=self.show_tutorial,
                            bg=ModernTheme.DARK['info'], fg='white',
                            font=('Segoe UI', 10, 'bold'), relief='flat',
                            padx=15, pady=8, cursor='hand2', borderwidth=0)
        help_btn.pack(side=tk.RIGHT, padx=5)
        
        self.status_indicator = tk.Label(content, text="● Disconnected",
                                         font=('Segoe UI', 12, 'bold'),
                                         bg=ModernTheme.DARK['surface'],
                                         fg=ModernTheme.DARK['error'])
        self.status_indicator.pack(side=tk.RIGHT, padx=20)
        
        self.server_status = tk.Label(content, text="Server: Unknown",
                                      font=('Segoe UI', 11),
                                      bg=ModernTheme.DARK['surface'],
                                      fg=ModernTheme.DARK['text_secondary'])
        self.server_status.pack(side=tk.RIGHT, padx=20)
    
    def create_main_content(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        from tabs.dashboard_tab import DashboardTab
        from tabs.mods_tab import ModsTab
        from tabs.players_tab import PlayersTab
        from tabs.files_tab import FilesTab
        from tabs.settings_tab import SettingsTab
        
        self.dashboard = DashboardTab(self.notebook, self)
        self.mods_tab = ModsTab(self.notebook, self)
        self.players_tab = PlayersTab(self.notebook, self)
        self.files_tab = FilesTab(self.notebook, self)
        self.settings_tab = SettingsTab(self.notebook, self)
        
        self.notebook.add(self.dashboard.frame, text="🎮 Dashboard")
        self.notebook.add(self.mods_tab.frame, text="🔧 Mods")
        self.notebook.add(self.players_tab.frame, text="👥 Players")
        self.notebook.add(self.files_tab.frame, text="📁 Files")
        self.notebook.add(self.settings_tab.frame, text="⚙️ Settings")
        
        # Bind tab change event for auto-fetch
        self.notebook.bind('<<NotebookTabChanged>>', self.on_tab_changed)
    
    def on_tab_changed(self, event):
        """Auto-fetch data when tab is selected"""
        if not self.ssh:
            return
        
        # Check if auto-fetch is enabled
        if not self.prefs.get('auto_fetch', True):
            return
        
        selected_tab = self.notebook.select()
        tab_text = self.notebook.tab(selected_tab, "text")
        
        # Auto-fetch based on tab
        if "Mods" in tab_text:
            self.log("🔄 Auto-fetching mods...")
            self.mods_tab.refresh_mods()
        elif "Players" in tab_text:
            self.log("🔄 Auto-fetching players...")
            self.players_tab.refresh_players()
        elif "Files" in tab_text:
            self.log("🔄 Auto-fetching files...")
            self.files_tab.browse_files()
        elif "Settings" in tab_text:
            self.log("🔄 Auto-loading settings...")
            self.settings_tab.load_properties()
        elif "Dashboard" in tab_text:
            self.log("🔄 Auto-updating stats...")
            self.dashboard.show_performance()
    
    def prompt_connection(self):
        # Show tutorial on first run
        if self.prefs.get('show_tutorial', True):
            if messagebox.askyesno("Welcome!", 
                                  "👋 Welcome to Minecraft Server Manager!\n\n"
                                  "Would you like to see a quick tutorial?\n\n"
                                  "This will show you how to:\n"
                                  "• Connect to your server\n"
                                  "• Install Minecraft servers\n"
                                  "• Manage mods and players\n"
                                  "• Use admin commands"):
                self.show_tutorial()
            
            # Don't show again
            self.prefs.set('show_tutorial', False)
        
        # Auto-connect if enabled
        if self.prefs.get('auto_connect', False):
            last_server = self.prefs.get_last_server()
            if last_server:
                self.log("🔄 Auto-connecting to last server...")
                if self.connect(
                    last_server['hostname'],
                    last_server['username'],
                    last_server['password'],
                    last_server.get('port', 22)
                ):
                    return
        
        # Show connection dialog
        dialog = ConnectionDialog(self.root, self)
        self.root.wait_window(dialog.dialog)
    
    def show_tutorial(self):
        from dialogs.tutorial_dialog import TutorialDialog
        TutorialDialog(self.root, self)
    
    def connect(self, hostname, username, password, port=22):
        try:
            self.ssh = SSHManager(hostname, username, password, port)
            self.ssh.connect()
            
            self.server = ServerManager(self.ssh)
            self.mods = ModManager(self.ssh)
            self.players = PlayerManager(self.ssh)
            self.files = FileManager(self.ssh)
            
            self.status_indicator.config(text="● Connected", 
                                        fg=ModernTheme.DARK['success'])
            self.logout_btn.config(state=tk.NORMAL)
            
            # Save credentials if enabled
            if self.prefs.get('remember_credentials', False):
                self.prefs.save_credentials(hostname, username, password, port)
                self.prefs.set_last_server(hostname)
            
            self.dashboard.on_connected()
            self.update_server_status()
            
            return True
        except Exception as e:
            messagebox.showerror("Connection Error", str(e))
            return False
    
    def logout(self):
        """Disconnect and show login dialog"""
        if messagebox.askyesno("Logout", "Are you sure you want to disconnect from the server?"):
            # Disconnect SSH
            if self.ssh:
                self.ssh.disconnect()
            
            # Reset managers
            self.ssh = None
            self.server = None
            self.mods = None
            self.players = None
            self.files = None
            
            # Update UI
            self.status_indicator.config(text="● Disconnected", 
                                        fg=ModernTheme.DARK['error'])
            self.server_status.config(text="Server: Unknown",
                                     fg=ModernTheme.DARK['text_secondary'])
            self.logout_btn.config(state=tk.DISABLED)
            
            # Clear dashboard
            if hasattr(self, 'dashboard'):
                self.dashboard.on_disconnected()
            
            # Show connection dialog
            self.prompt_connection()
    
    def on_closing(self):
        """Handle window close"""
        # Save window size
        geometry = self.root.geometry()
        self.prefs.set('window_size', geometry)
        
        # Close SSH connection
        if self.ssh:
            self.ssh.disconnect()
        
        self.root.destroy()
    
    def update_server_status(self):
        if not self.server:
            return
        
        def update():
            try:
                status = self.server.get_status()
                if status['running']:
                    self.server_status.config(
                        text=f"Server: Running ({status.get('type', 'Unknown')})",
                        fg=ModernTheme.DARK['success']
                    )
                else:
                    self.server_status.config(
                        text="Server: Stopped",
                        fg=ModernTheme.DARK['error']
                    )
            except:
                pass
        
        threading.Thread(target=update, daemon=True).start()
    
    def log(self, message):
        if hasattr(self, 'dashboard'):
            self.dashboard.log(message)

class ConnectionDialog:
    def __init__(self, parent, app):
        self.app = app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Connect to Server")
        self.dialog.geometry("550x550")
        self.dialog.configure(bg=ModernTheme.DARK['bg'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        self.dialog.resizable(False, False)
        
        self.create_ui()
    
    def create_ui(self):
        card = tk.Frame(self.dialog, bg=ModernTheme.DARK['surface'], 
                       highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        content = tk.Frame(card, bg=ModernTheme.DARK['surface'])
        content.pack(fill=tk.BOTH, expand=True, padx=30, pady=30)
        
        title = tk.Label(content, text="🔌 Server Connection",
                        font=('Segoe UI', 18, 'bold'),
                        bg=ModernTheme.DARK['surface'],
                        fg=ModernTheme.DARK['accent'])
        title.pack(pady=(0, 20))
        
        # Saved servers dropdown
        saved_servers = self.app.prefs.get_all_servers()
        if saved_servers:
            saved_frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
            saved_frame.pack(fill=tk.X, pady=10)
            
            tk.Label(saved_frame, text="Saved Servers:", width=12, anchor='w',
                    bg=ModernTheme.DARK['surface'], fg=ModernTheme.DARK['text'],
                    font=('Segoe UI', 10, 'bold')).pack(side=tk.LEFT, padx=(0, 10))
            
            self.server_var = tk.StringVar()
            server_combo = ttk.Combobox(saved_frame, textvariable=self.server_var,
                                       values=saved_servers, state='readonly',
                                       font=('Segoe UI', 10))
            server_combo.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
            server_combo.bind('<<ComboboxSelected>>', self.load_server)
        
        fields = [
            ("Hostname/IP:", "hostname", ""),
            ("Port:", "port", "22"),
            ("Username:", "username", "root"),
            ("Password:", "password", "")
        ]
        
        self.entries = {}
        
        for label_text, key, default in fields:
            frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
            frame.pack(fill=tk.X, pady=10)
            
            label = tk.Label(frame, text=label_text, width=12, anchor='w',
                           bg=ModernTheme.DARK['surface'],
                           fg=ModernTheme.DARK['text'],
                           font=('Segoe UI', 10, 'bold'))
            label.pack(side=tk.LEFT, padx=(0, 10))
            
            entry = tk.Entry(frame, bg=ModernTheme.DARK['surface_light'],
                           fg=ModernTheme.DARK['text'], font=('Segoe UI', 10),
                           relief='flat', insertbackground=ModernTheme.DARK['text'])
            entry.insert(0, default)
            if key == "password":
                entry.config(show='●')
            entry.pack(side=tk.LEFT, fill=tk.X, expand=True, ipady=10, padx=5)
            entry.config(highlightthickness=1, highlightbackground=ModernTheme.DARK['border'],
                        highlightcolor=ModernTheme.DARK['accent'])
            
            self.entries[key] = entry
        
        # Options
        options_frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
        options_frame.pack(fill=tk.X, pady=15)
        
        self.remember_var = tk.BooleanVar(value=self.app.prefs.get('remember_credentials', False))
        tk.Checkbutton(options_frame, text="Remember credentials",
                      variable=self.remember_var,
                      bg=ModernTheme.DARK['surface'], fg=ModernTheme.DARK['text'],
                      selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 9)).pack(anchor='w')
        
        self.auto_connect_var = tk.BooleanVar(value=self.app.prefs.get('auto_connect', False))
        tk.Checkbutton(options_frame, text="Auto-connect on startup",
                      variable=self.auto_connect_var,
                      bg=ModernTheme.DARK['surface'], fg=ModernTheme.DARK['text'],
                      selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 9)).pack(anchor='w')
        
        # Bind Enter key
        for entry in self.entries.values():
            entry.bind('<Return>', lambda e: self.connect())
        
        btn_frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
        btn_frame.pack(pady=(20, 0))
        
        connect_btn = tk.Button(btn_frame, text="🔌 Connect", command=self.connect,
                               bg=ModernTheme.DARK['accent'], fg='white',
                               font=('Segoe UI', 11, 'bold'), relief='flat',
                               padx=30, pady=12, cursor='hand2', borderwidth=0)
        connect_btn.pack(side=tk.LEFT, padx=5)
        
        settings_btn = tk.Button(btn_frame, text="⚙️ Settings", command=self.show_settings,
                                bg=ModernTheme.DARK['surface_light'], fg=ModernTheme.DARK['text'],
                                font=('Segoe UI', 11), relief='flat',
                                padx=30, pady=12, cursor='hand2', borderwidth=0)
        settings_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.dialog.destroy,
                              bg=ModernTheme.DARK['surface_light'], fg=ModernTheme.DARK['text'],
                              font=('Segoe UI', 11), relief='flat',
                              padx=30, pady=12, cursor='hand2', borderwidth=0)
        cancel_btn.pack(side=tk.LEFT, padx=5)
        
        # Clear saved servers button
        if saved_servers:
            clear_frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
            clear_frame.pack(pady=(15, 0))
            
            clear_btn = tk.Button(clear_frame, text="🗑️ Clear Saved Servers", 
                                 command=self.clear_saved_servers,
                                 bg=ModernTheme.DARK['error'], fg='white',
                                 font=('Segoe UI', 9), relief='flat',
                                 padx=15, pady=8, cursor='hand2', borderwidth=0)
            clear_btn.pack()
    
    def load_server(self, event=None):
        """Load saved server credentials"""
        hostname = self.server_var.get()
        if hostname in self.app.prefs.credentials:
            creds = self.app.prefs.credentials[hostname]
            self.entries['hostname'].delete(0, tk.END)
            self.entries['hostname'].insert(0, creds['hostname'])
            self.entries['username'].delete(0, tk.END)
            self.entries['username'].insert(0, creds['username'])
            self.entries['port'].delete(0, tk.END)
            self.entries['port'].insert(0, creds.get('port', 22))
            
            # Password is already decoded in load_credentials
            password = creds.get('password', '')
            self.entries['password'].delete(0, tk.END)
            self.entries['password'].insert(0, password)
    
    def show_settings(self):
        """Show preferences dialog"""
        from dialogs.preferences_dialog import PreferencesDialog
        PreferencesDialog(self.dialog, self.app)
    
    def clear_saved_servers(self):
        """Clear all saved server credentials"""
        if messagebox.askyesno("Clear Saved Servers", 
                              "Are you sure you want to delete all saved server credentials?\n\n"
                              "This cannot be undone."):
            self.app.prefs.clear_all_credentials()
            messagebox.showinfo("Success", "All saved servers have been cleared.")
            self.dialog.destroy()
            # Reopen dialog to refresh
            ConnectionDialog(self.app.root, self.app)
    
    def connect(self):
        hostname = self.entries['hostname'].get()
        port = int(self.entries['port'].get() or 22)
        username = self.entries['username'].get()
        password = self.entries['password'].get()
        
        if not hostname or not username:
            messagebox.showerror("Error", "Hostname and username are required!")
            return
        
        # Save preferences
        self.app.prefs.set('remember_credentials', self.remember_var.get())
        self.app.prefs.set('auto_connect', self.auto_connect_var.get())
        
        if self.app.connect(hostname, username, password, port):
            self.dialog.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = MinecraftServerManager(root)
    root.mainloop()
