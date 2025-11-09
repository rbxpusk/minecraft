"""Dashboard tab with server controls and console"""
import tkinter as tk
from tkinter import scrolledtext, messagebox, simpledialog
import threading
from ui_components import ModernTheme, ModernButton, Card

class DashboardTab:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent, bg=ModernTheme.DARK['bg'])
        self.auto_refresh = False
        self.refresh_job = None
        self.performance_job = None
        self.auto_performance = False
        self.setup_ui()
    
    def setup_ui(self):
        # Stats panel
        stats_frame = tk.Frame(self.frame, bg=ModernTheme.DARK['bg'])
        stats_frame.pack(fill=tk.X, padx=10, pady=10)
        
        stats = [
            ("CPU", "cpu_label"),
            ("RAM", "ram_label"),
            ("Players", "players_label"),
            ("Uptime", "uptime_label")
        ]
        
        for i, (title, attr) in enumerate(stats):
            stat_card = tk.Frame(stats_frame, bg=ModernTheme.DARK['surface'],
                                highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
            stat_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
            
            tk.Label(stat_card, text=title, bg=ModernTheme.DARK['surface'],
                    fg=ModernTheme.DARK['text_secondary'], font=('Segoe UI', 9)).pack(pady=(10, 0))
            
            label = tk.Label(stat_card, text="--", bg=ModernTheme.DARK['surface'],
                           fg=ModernTheme.DARK['accent'], font=('Segoe UI', 16, 'bold'))
            label.pack(pady=(0, 10))
            setattr(self, attr, label)
        
        controls = Card(self.frame)
        controls.pack(fill=tk.X, padx=10, pady=10)
        
        btn_container = tk.Frame(controls, bg=ModernTheme.DARK['surface'])
        btn_container.pack(pady=15)
        
        buttons = [
            ("▶️ Start Server", self.start_server, 'success'),
            ("⏹️ Stop Server", self.stop_server, 'error'),
            ("🔄 Restart", self.restart_server, 'warning'),
            ("🔍 Check Status", self.check_status, 'primary'),
            ("📦 Install Server", self.install_server, 'warning'),
            ("📊 Performance", self.show_performance, 'primary'),
        ]
        
        for text, cmd, style in buttons:
            ModernButton(btn_container, text=text, command=cmd, style=style).pack(
                side=tk.LEFT, padx=5
            )
        
        console_label = tk.Label(self.frame, text="📟 Server Console",
                                font=('Segoe UI', 12, 'bold'),
                                bg=ModernTheme.DARK['bg'],
                                fg=ModernTheme.DARK['accent'])
        console_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        console_card = Card(self.frame)
        console_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        self.console = scrolledtext.ScrolledText(
            console_card, wrap=tk.WORD, height=20,
            bg='#0a0e14', fg='#00ff00',
            font=('Consolas', 10), relief='flat',
            insertbackground='#00ff00'
        )
        self.console.pack(fill=tk.BOTH, expand=True, padx=2, pady=2)
        
        cmd_card = Card(self.frame)
        cmd_card.pack(fill=tk.X, padx=10, pady=10)
        
        cmd_frame = tk.Frame(cmd_card, bg=ModernTheme.DARK['surface'])
        cmd_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(cmd_frame, text="Command:", bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['text'], font=('Segoe UI', 10)).pack(
            side=tk.LEFT, padx=10
        )
        
        self.cmd_entry = tk.Entry(
            cmd_frame, bg=ModernTheme.DARK['surface_light'],
            fg=ModernTheme.DARK['text'], font=('Consolas', 10),
            relief='flat', insertbackground=ModernTheme.DARK['text']
        )
        self.cmd_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5, ipady=8)
        self.cmd_entry.bind("<Return>", lambda e: self.send_command())
        
        ModernButton(cmd_frame, text="Send", command=self.send_command,
                    style='primary').pack(side=tk.LEFT, padx=5)
        ModernButton(cmd_frame, text="Clear", 
                    command=lambda: self.console.delete(1.0, tk.END),
                    style='secondary').pack(side=tk.LEFT, padx=5)
        
        # Quick Commands
        quick_label = tk.Label(self.frame, text="⚡ Quick Commands",
                              font=('Segoe UI', 12, 'bold'),
                              bg=ModernTheme.DARK['bg'],
                              fg=ModernTheme.DARK['accent'])
        quick_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        quick_card = Card(self.frame)
        quick_card.pack(fill=tk.X, padx=10, pady=5)
        
        quick_container = tk.Frame(quick_card, bg=ModernTheme.DARK['surface'])
        quick_container.pack(pady=10, padx=15)
        
        commands = [
            ("☀️ Day", "time set day"),
            ("🌙 Night", "time set night"),
            ("☀️ Clear", "weather clear"),
            ("🌧️ Rain", "weather rain"),
            ("⚡ Thunder", "weather thunder"),
            ("🎮 Creative All", "gamemode creative @a"),
            ("🎮 Survival All", "gamemode survival @a"),
            ("💾 Save World", "save-all"),
            ("📢 Broadcast", None),
            ("🚀 Teleport", None),
            ("🎁 Give Item", None),
            ("👥 List Players", "list"),
            ("🔄 Reload", "reload"),
            ("⚙️ Easy", "difficulty easy"),
            ("⚙️ Normal", "difficulty normal"),
            ("⚙️ Hard", "difficulty hard"),
            ("🌱 Set Spawn", "setworldspawn"),
            ("🔥 Kill All Mobs", "kill @e[type=!player]"),
            ("💎 Give XP", None),
            ("🌍 World Border", None),
        ]
        
        for i, (label, cmd) in enumerate(commands):
            btn = tk.Button(quick_container, text=label,
                           command=lambda c=cmd, l=label: self.quick_command(c, l),
                           bg=ModernTheme.DARK['accent'], fg='white',
                           font=('Segoe UI', 9, 'bold'), relief='flat',
                           padx=12, pady=6, cursor='hand2', borderwidth=0)
            btn.grid(row=i//4, column=i%4, padx=3, pady=3, sticky='ew')
        
        # Auto-refresh options
        refresh_frame = tk.Frame(self.frame, bg=ModernTheme.DARK['bg'])
        refresh_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.auto_refresh_var = tk.BooleanVar()
        tk.Checkbutton(refresh_frame, text="🔄 Auto-refresh logs (5s)",
                      variable=self.auto_refresh_var, command=self.toggle_auto_refresh,
                      bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                      selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
        
        self.auto_performance_var = tk.BooleanVar(value=True)
        tk.Checkbutton(refresh_frame, text="📊 Auto-update stats (10s)",
                      variable=self.auto_performance_var, command=self.toggle_auto_performance,
                      bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                      selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 10)).pack(side=tk.LEFT, padx=10)
    
    def log(self, message):
        self.console.insert(tk.END, f"{message}\n")
        self.console.see(tk.END)
    
    def on_connected(self):
        self.log("✅ Connected")
        self.check_status()
    
    def on_disconnected(self):
        """Handle disconnection"""
        self.console.delete(1.0, tk.END)
        self.log("🚪 Disconnected from server")
        self.performance_labels['cpu'].config(text="CPU: --")
        self.performance_labels['ram'].config(text="RAM: --")
        self.performance_labels['players'].config(text="Players: --")
        self.performance_labels['uptime'].config(text="Uptime: --")
        
        # Stop auto-refresh
        if hasattr(self, 'auto_refresh') and self.auto_refresh:
            self.auto_refresh = False
        if hasattr(self, 'auto_performance') and self.auto_performance:
            self.auto_performance = False
        # Start auto-performance if enabled
        if self.auto_performance_var.get():
            self.start_auto_performance()
    
    def start_server(self):
        if not self.app.server:
            messagebox.showerror("Error", "Not connected to server!")
            return
        
        self.log("▶️ Starting server...")
        
        def start():
            try:
                self.app.server.start()
                self.log("✅ Server started")
                self.app.update_server_status()
            except Exception as e:
                self.log(f"❌ Error: {e}")
        
        threading.Thread(target=start, daemon=True).start()
    
    def stop_server(self):
        if not self.app.server:
            return
        
        self.log("⏹️ Stopping server...")
        
        def stop():
            try:
                self.app.server.stop()
                self.log("✅ Server stopped")
                self.app.update_server_status()
            except Exception as e:
                self.log(f"❌ Error: {e}")
        
        threading.Thread(target=stop, daemon=True).start()
    
    def restart_server(self):
        if not self.app.server:
            return
        
        self.log("🔄 Restarting server...")
        
        def restart():
            try:
                self.app.server.restart()
                self.log("✅ Server restarted")
                self.app.update_server_status()
            except Exception as e:
                self.log(f"❌ Error: {e}")
        
        threading.Thread(target=restart, daemon=True).start()
    
    def check_status(self):
        if not self.app.server:
            return
        
        def check():
            try:
                status = self.app.server.get_status()
                if status['running']:
                    self.log(f"✅ Server is running ({status.get('type', 'Unknown')})")
                else:
                    self.log("⏹️ Server is stopped")
                self.app.update_server_status()
            except Exception as e:
                self.log(f"❌ Error: {e}")
        
        threading.Thread(target=check, daemon=True).start()
    
    def install_server(self):
        from dialogs.install_dialog import InstallDialog
        InstallDialog(self.frame, self.app)
    
    def send_command(self):
        if not self.app.server:
            return
        
        cmd = self.cmd_entry.get().strip()
        if not cmd:
            return
        
        self.log(f">>> {cmd}")
        self.app.server.send_command(cmd)
        self.cmd_entry.delete(0, tk.END)
    
    def toggle_auto_refresh(self):
        self.auto_refresh = self.auto_refresh_var.get()
        if self.auto_refresh:
            self.start_auto_refresh()
        else:
            self.stop_auto_refresh()
    
    def start_auto_refresh(self):
        if self.auto_refresh and self.app.files:
            def refresh():
                try:
                    logs = self.app.files.get_logs(50)
                    # Only show new logs
                    current = self.console.get(1.0, tk.END)
                    if logs not in current:
                        self.console.delete(1.0, tk.END)
                        self.console.insert(1.0, logs)
                        self.console.see(tk.END)
                except:
                    pass
            
            threading.Thread(target=refresh, daemon=True).start()
            self.refresh_job = self.frame.after(5000, self.start_auto_refresh)
    
    def stop_auto_refresh(self):
        if self.refresh_job:
            self.frame.after_cancel(self.refresh_job)
            self.refresh_job = None
    
    def toggle_auto_performance(self):
        """Toggle auto-performance updates"""
        self.auto_performance = self.auto_performance_var.get()
        if self.auto_performance:
            self.app.log("📊 Auto-update stats enabled")
            self.start_auto_performance()
        else:
            self.app.log("📊 Auto-update stats disabled")
            self.stop_auto_performance()
    
    def start_auto_performance(self):
        """Start auto-updating performance stats"""
        if not self.app.ssh:
            return
        
        self.auto_performance = True
        
        if self.auto_performance:
            def update():
                try:
                    # CPU
                    cpu_out, _ = self.app.ssh.execute("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
                    cpu = cpu_out.strip().replace('%us,', '').replace('us,', '')
                    if cpu:
                        self.cpu_label.config(text=f"{cpu}%")
                    
                    # RAM
                    ram_out, _ = self.app.ssh.execute("free -h | grep Mem | awk '{print $3\"/\"$2}'")
                    ram = ram_out.strip()
                    if ram:
                        self.ram_label.config(text=ram)
                    
                    # Players
                    player_out, _ = self.app.ssh.execute(
                        "cd /root/minecraft && tail -100 logs/latest.log 2>/dev/null | "
                        "grep -c 'joined the game' || echo '0'"
                    )
                    players = player_out.strip()
                    if players:
                        self.players_label.config(text=players)
                    
                    # Uptime
                    uptime_out, _ = self.app.ssh.execute("uptime -p")
                    uptime = uptime_out.strip().replace('up ', '')
                    if uptime:
                        self.uptime_label.config(text=uptime[:20])
                except:
                    pass
            
            threading.Thread(target=update, daemon=True).start()
            self.performance_job = self.frame.after(10000, self.start_auto_performance)
    
    def stop_auto_performance(self):
        if self.performance_job:
            self.frame.after_cancel(self.performance_job)
            self.performance_job = None
    
    def show_performance(self):
        """Manual performance update"""
        if not self.app.ssh:
            return
        
        self.app.log("📊 Updating performance stats...")
        
        def get_stats():
            try:
                # CPU
                cpu_out, _ = self.app.ssh.execute("top -bn1 | grep 'Cpu(s)' | awk '{print $2}'")
                cpu = cpu_out.strip().replace('%us,', '').replace('us,', '')
                if cpu:
                    self.cpu_label.config(text=f"{cpu}%")
                
                # RAM
                ram_out, _ = self.app.ssh.execute("free -h | grep Mem | awk '{print $3\"/\"$2}'")
                ram = ram_out.strip()
                if ram:
                    self.ram_label.config(text=ram)
                
                # Players
                player_out, _ = self.app.ssh.execute(
                    "cd /root/minecraft && tail -100 logs/latest.log 2>/dev/null | "
                    "grep -c 'joined the game' || echo '0'"
                )
                players = player_out.strip()
                if players:
                    self.players_label.config(text=players)
                
                # Uptime
                uptime_out, _ = self.app.ssh.execute("uptime -p")
                uptime = uptime_out.strip().replace('up ', '')
                if uptime:
                    self.uptime_label.config(text=uptime[:20])
                
                self.app.log("✅ Performance stats updated")
            except Exception as e:
                self.app.log(f"❌ Error getting stats: {e}")
        
        threading.Thread(target=get_stats, daemon=True).start()
    
    def quick_command(self, cmd, label):
        if not self.app.server:
            return
        
        # Special handlers
        if cmd is None:
            if "Broadcast" in label:
                msg = tk.simpledialog.askstring("Broadcast", "Enter message:")
                if msg:
                    cmd = f"say {msg}"
            elif "Teleport" in label:
                self.show_teleport_dialog()
                return
            elif "Give Item" in label:
                self.show_give_dialog()
                return
            elif "Give XP" in label:
                self.show_xp_dialog()
                return
            elif "World Border" in label:
                self.show_border_dialog()
                return
        
        if cmd:
            self.log(f"⚡ {label}: {cmd}")
            self.app.server.send_command(cmd)
    
    def show_teleport_dialog(self):
        dialog = tk.Toplevel(self.frame)
        dialog.title("Teleport Player")
        dialog.geometry("400x250")
        dialog.configure(bg=ModernTheme.DARK['bg'])
        dialog.transient(self.frame)
        
        tk.Label(dialog, text="🚀 Teleport Player",
                font=('Segoe UI', 16, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        frame = tk.Frame(dialog, bg=ModernTheme.DARK['bg'])
        frame.pack(pady=10)
        
        fields = [
            ("Player:", "player"),
            ("X:", "x"),
            ("Y:", "y"),
            ("Z:", "z")
        ]
        
        entries = {}
        for label, key in fields:
            row = tk.Frame(frame, bg=ModernTheme.DARK['bg'])
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(row, text=label, width=8, anchor='w',
                    bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                    font=('Segoe UI', 10)).pack(side=tk.LEFT)
            
            entry = tk.Entry(row, bg=ModernTheme.DARK['surface_light'],
                           fg=ModernTheme.DARK['text'], font=('Segoe UI', 10),
                           relief='flat', width=20)
            entry.pack(side=tk.LEFT, ipady=5)
            entries[key] = entry
        
        def teleport():
            player = entries['player'].get()
            x = entries['x'].get()
            y = entries['y'].get()
            z = entries['z'].get()
            
            if player and x and y and z:
                cmd = f"tp {player} {x} {y} {z}"
                self.log(f"🚀 Teleporting: {cmd}")
                self.app.server.send_command(cmd)
                dialog.destroy()
        
        tk.Button(dialog, text="Teleport", command=teleport,
                 bg=ModernTheme.DARK['accent'], fg='white',
                 font=('Segoe UI', 11, 'bold'), relief='flat',
                 padx=30, pady=10, cursor='hand2').pack(pady=20)
    
    def show_give_dialog(self):
        dialog = tk.Toplevel(self.frame)
        dialog.title("Give Item")
        dialog.geometry("400x250")
        dialog.configure(bg=ModernTheme.DARK['bg'])
        dialog.transient(self.frame)
        
        tk.Label(dialog, text="🎁 Give Item",
                font=('Segoe UI', 16, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        frame = tk.Frame(dialog, bg=ModernTheme.DARK['bg'])
        frame.pack(pady=10)
        
        fields = [
            ("Player:", "player"),
            ("Item:", "item"),
            ("Amount:", "amount")
        ]
        
        entries = {}
        for label, key in fields:
            row = tk.Frame(frame, bg=ModernTheme.DARK['bg'])
            row.pack(fill=tk.X, pady=5)
            
            tk.Label(row, text=label, width=8, anchor='w',
                    bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                    font=('Segoe UI', 10)).pack(side=tk.LEFT)
            
            entry = tk.Entry(row, bg=ModernTheme.DARK['surface_light'],
                           fg=ModernTheme.DARK['text'], font=('Segoe UI', 10),
                           relief='flat', width=20)
            if key == "amount":
                entry.insert(0, "1")
            entry.pack(side=tk.LEFT, ipady=5)
            entries[key] = entry
        
        def give():
            player = entries['player'].get()
            item = entries['item'].get()
            amount = entries['amount'].get()
            
            if player and item:
                cmd = f"give {player} {item} {amount}"
                self.log(f"🎁 Giving item: {cmd}")
                self.app.server.send_command(cmd)
                dialog.destroy()
        
        tk.Button(dialog, text="Give Item", command=give,
                 bg=ModernTheme.DARK['success'], fg='white',
                 font=('Segoe UI', 11, 'bold'), relief='flat',
                 padx=30, pady=10, cursor='hand2').pack(pady=20)
    
    def show_xp_dialog(self):
        dialog = tk.Toplevel(self.frame)
        dialog.title("Give XP")
        dialog.geometry("400x200")
        dialog.configure(bg=ModernTheme.DARK['bg'])
        dialog.transient(self.frame)
        
        tk.Label(dialog, text="💎 Give XP",
                font=('Segoe UI', 16, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        frame = tk.Frame(dialog, bg=ModernTheme.DARK['bg'])
        frame.pack(pady=10)
        
        tk.Label(frame, text="Player:", width=8, anchor='w',
                bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                font=('Segoe UI', 10)).grid(row=0, column=0, padx=5, pady=5)
        
        player_entry = tk.Entry(frame, bg=ModernTheme.DARK['surface_light'],
                               fg=ModernTheme.DARK['text'], font=('Segoe UI', 10),
                               relief='flat', width=20)
        player_entry.grid(row=0, column=1, padx=5, pady=5, ipady=5)
        
        tk.Label(frame, text="Levels:", width=8, anchor='w',
                bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                font=('Segoe UI', 10)).grid(row=1, column=0, padx=5, pady=5)
        
        xp_entry = tk.Entry(frame, bg=ModernTheme.DARK['surface_light'],
                           fg=ModernTheme.DARK['text'], font=('Segoe UI', 10),
                           relief='flat', width=20)
        xp_entry.insert(0, "10")
        xp_entry.grid(row=1, column=1, padx=5, pady=5, ipady=5)
        
        def give_xp():
            player = player_entry.get()
            levels = xp_entry.get()
            if player and levels:
                cmd = f"xp add {player} {levels} levels"
                self.log(f"💎 Giving XP: {cmd}")
                self.app.server.send_command(cmd)
                dialog.destroy()
        
        tk.Button(dialog, text="Give XP", command=give_xp,
                 bg=ModernTheme.DARK['success'], fg='white',
                 font=('Segoe UI', 11, 'bold'), relief='flat',
                 padx=30, pady=10, cursor='hand2').pack(pady=20)
    
    def show_border_dialog(self):
        dialog = tk.Toplevel(self.frame)
        dialog.title("World Border")
        dialog.geometry("400x200")
        dialog.configure(bg=ModernTheme.DARK['bg'])
        dialog.transient(self.frame)
        
        tk.Label(dialog, text="🌍 World Border",
                font=('Segoe UI', 16, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        frame = tk.Frame(dialog, bg=ModernTheme.DARK['bg'])
        frame.pack(pady=10)
        
        tk.Label(frame, text="Size (blocks):", width=12, anchor='w',
                bg=ModernTheme.DARK['bg'], fg=ModernTheme.DARK['text'],
                font=('Segoe UI', 10)).grid(row=0, column=0, padx=5, pady=5)
        
        size_entry = tk.Entry(frame, bg=ModernTheme.DARK['surface_light'],
                             fg=ModernTheme.DARK['text'], font=('Segoe UI', 10),
                             relief='flat', width=20)
        size_entry.insert(0, "10000")
        size_entry.grid(row=0, column=1, padx=5, pady=5, ipady=5)
        
        def set_border():
            size = size_entry.get()
            if size:
                cmd = f"worldborder set {size}"
                self.log(f"🌍 Setting border: {cmd}")
                self.app.server.send_command(cmd)
                dialog.destroy()
        
        tk.Button(dialog, text="Set Border", command=set_border,
                 bg=ModernTheme.DARK['accent'], fg='white',
                 font=('Segoe UI', 11, 'bold'), relief='flat',
                 padx=30, pady=10, cursor='hand2').pack(pady=20)
