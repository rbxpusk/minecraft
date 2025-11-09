"""Players management tab"""
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import threading
from ui_components import ModernTheme, ModernButton, Card

class PlayersTab:
    def __init__(self, parent, app):
        self.app = app
        self.frame = tk.Frame(parent, bg=ModernTheme.DARK['bg'])
        self.setup_ui()
    
    def setup_ui(self):
        # Quick actions
        quick_label = tk.Label(self.frame, text="⚡ Quick Actions",
                              font=('Segoe UI', 12, 'bold'),
                              bg=ModernTheme.DARK['bg'],
                              fg=ModernTheme.DARK['accent'])
        quick_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        actions = Card(self.frame)
        actions.pack(fill=tk.X, padx=10, pady=5)
        
        btn_container = tk.Frame(actions, bg=ModernTheme.DARK['surface'])
        btn_container.pack(pady=15)
        
        buttons = [
            ("🔄 Refresh", self.refresh_players, 'primary'),
            ("👑 Op Player", self.op_player, 'warning'),
            ("👤 Deop Player", self.deop_player, 'secondary'),
            ("🚫 Kick Player", self.kick_player, 'warning'),
            ("🔨 Ban Player", self.ban_player, 'error'),
            ("✅ Unban Player", self.unban_player, 'success'),
            ("💬 Message Player", self.message_player, 'primary'),
            ("🎮 Change Gamemode", self.change_gamemode, 'primary'),
        ]
        
        for text, cmd, style in buttons:
            ModernButton(btn_container, text=text, command=cmd, style=style).pack(
                side=tk.LEFT, padx=5
            )
        
        # Selection info
        self.selection_label = tk.Label(self.frame, text="💡 Tip: Select a player to perform actions",
                                       font=('Segoe UI', 10),
                                       bg=ModernTheme.DARK['bg'],
                                       fg=ModernTheme.DARK['text_secondary'])
        self.selection_label.pack(anchor='w', padx=15, pady=5)
        
        list_label = tk.Label(self.frame, text="👥 Online Players",
                             font=('Segoe UI', 12, 'bold'),
                             bg=ModernTheme.DARK['bg'],
                             fg=ModernTheme.DARK['accent'])
        list_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        list_card = Card(self.frame)
        list_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Username", "UUID", "Status")
        self.tree = ttk.Treeview(list_card, columns=columns, show="headings", height=10)
        
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=250)
        
        # Bind selection and double-click events
        self.tree.bind('<<TreeviewSelect>>', self.on_player_select)
        self.tree.bind('<Double-Button-1>', lambda e: self.show_player_menu())
        
        scrollbar = ttk.Scrollbar(list_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        whitelist_label = tk.Label(self.frame, text="📋 Whitelist Management",
                                   font=('Segoe UI', 12, 'bold'),
                                   bg=ModernTheme.DARK['bg'],
                                   fg=ModernTheme.DARK['accent'])
        whitelist_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        wl_actions = Card(self.frame)
        wl_actions.pack(fill=tk.X, padx=10, pady=5)
        
        wl_btn_container = tk.Frame(wl_actions, bg=ModernTheme.DARK['surface'])
        wl_btn_container.pack(pady=10)
        
        wl_buttons = [
            ("➕ Add to Whitelist", self.add_whitelist, 'success'),
            ("➖ Remove from Whitelist", self.remove_whitelist, 'error'),
            ("🔒 Enable Whitelist", lambda: self.send_cmd("whitelist on"), 'warning'),
            ("🔓 Disable Whitelist", lambda: self.send_cmd("whitelist off"), 'secondary'),
        ]
        
        for text, cmd, style in wl_buttons:
            ModernButton(wl_btn_container, text=text, command=cmd, style=style).pack(
                side=tk.LEFT, padx=5
            )
    
    def get_selected_player(self):
        """Get the selected player from the tree"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            return item['values'][0]  # Username is first column
        return None
    
    def refresh_players(self):
        if not self.app.players:
            return
        
        # Show loading indicator
        self.selection_label.config(
            text="🔄 Loading players...",
            fg=ModernTheme.DARK['warning']
        )
        
        def refresh():
            try:
                players = self.app.players.get_online_players()
                self.tree.delete(*self.tree.get_children())
                
                for player in players:
                    self.tree.insert('', tk.END, values=(
                        player['username'], player['uuid'], player['status']
                    ))
                
                self.selection_label.config(
                    text=f"✅ {len(players)} players online - Select one to perform actions",
                    fg=ModernTheme.DARK['success']
                )
                self.app.log(f"✅ Found {len(players)} online players")
            except Exception as e:
                self.selection_label.config(
                    text="❌ Error loading players",
                    fg=ModernTheme.DARK['error']
                )
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def op_player(self):
        # Try to get selected player first
        username = self.get_selected_player()
        
        # If no selection, ask for username
        if not username:
            username = simpledialog.askstring("Op Player", "Enter username:")
        
        if username:
            self.app.players.op_player(username)
            self.app.log(f"👑 Opped {username}")
    
    def deop_player(self):
        username = self.get_selected_player()
        
        if not username:
            username = simpledialog.askstring("Deop Player", "Enter username:")
        
        if username:
            self.app.players.deop_player(username)
            self.app.log(f"👤 Deopped {username}")
    
    def kick_player(self):
        username = self.get_selected_player()
        
        if not username:
            username = simpledialog.askstring("Kick Player", "Enter username:")
        
        if username:
            reason = simpledialog.askstring("Reason", "Enter reason (optional):") or ""
            self.app.players.kick_player(username, reason)
            self.app.log(f"🚫 Kicked {username}")
            self.refresh_players()
    
    def ban_player(self):
        username = self.get_selected_player()
        
        if not username:
            username = simpledialog.askstring("Ban Player", "Enter username:")
        
        if username:
            reason = simpledialog.askstring("Reason", "Enter reason (optional):") or ""
            self.app.players.ban_player(username, reason)
            self.app.log(f"🔨 Banned {username}")
            self.refresh_players()
    
    def unban_player(self):
        username = self.get_selected_player()
        
        if not username:
            username = simpledialog.askstring("Unban Player", "Enter username:")
        
        if username:
            self.app.players.unban_player(username)
            self.app.log(f"✅ Unbanned {username}")
    
    def add_whitelist(self):
        username = self.get_selected_player()
        
        if not username:
            username = simpledialog.askstring("Add to Whitelist", "Enter username:")
        
        if username:
            self.app.players.add_to_whitelist(username)
            self.app.log(f"➕ Added {username} to whitelist")
    
    def remove_whitelist(self):
        username = self.get_selected_player()
        
        if not username:
            username = simpledialog.askstring("Remove from Whitelist", "Enter username:")
        
        if username:
            self.app.players.remove_from_whitelist(username)
            self.app.log(f"➖ Removed {username} from whitelist")
    
    def send_cmd(self, cmd):
        if self.app.server:
            self.app.server.send_command(cmd)
            self.app.log(f">>> {cmd}")
    
    def message_player(self):
        username = self.get_selected_player()
        
        if not username:
            username = simpledialog.askstring("Message Player", "Enter username:")
        
        if username:
            message = simpledialog.askstring("Message", f"Message to {username}:")
            if message:
                self.app.server.send_command(f"msg {username} {message}")
                self.app.log(f"💬 Sent message to {username}")
    
    def change_gamemode(self):
        username = self.get_selected_player()
        
        if not username:
            username = simpledialog.askstring("Change Gamemode", "Enter username:")
        
        if username:
            dialog = tk.Toplevel(self.frame)
            dialog.title("Select Gamemode")
            dialog.geometry("300x250")
            dialog.configure(bg=ModernTheme.DARK['bg'])
            dialog.transient(self.frame)
            
            tk.Label(dialog, text="🎮 Select Gamemode",
                    font=('Segoe UI', 14, 'bold'),
                    bg=ModernTheme.DARK['bg'],
                    fg=ModernTheme.DARK['accent']).pack(pady=20)
            
            modes = [
                ("🎮 Survival", "survival"),
                ("🎨 Creative", "creative"),
                ("👁️ Spectator", "spectator"),
                ("🗺️ Adventure", "adventure")
            ]
            
            for text, mode in modes:
                tk.Button(dialog, text=text,
                         command=lambda m=mode: self.set_gamemode(username, m, dialog),
                         bg=ModernTheme.DARK['accent'], fg='white',
                         font=('Segoe UI', 11), relief='flat',
                         padx=30, pady=10, cursor='hand2', width=15).pack(pady=5)
    
    def set_gamemode(self, username, mode, dialog):
        self.app.server.send_command(f"gamemode {mode} {username}")
        self.app.log(f"🎮 Changed {username} to {mode}")
        dialog.destroy()
    
    def on_player_select(self, event):
        """Update selection label when player is selected"""
        player = self.get_selected_player()
        if player:
            self.selection_label.config(
                text=f"✅ Selected: {player} - Click any action button or double-click for menu",
                fg=ModernTheme.DARK['success']
            )
        else:
            self.selection_label.config(
                text="💡 Tip: Select a player to perform actions",
                fg=ModernTheme.DARK['text_secondary']
            )
    
    def show_player_menu(self):
        """Show quick action menu for selected player"""
        player = self.get_selected_player()
        if not player:
            return
        
        menu = tk.Menu(self.frame, tearoff=0, bg=ModernTheme.DARK['surface'],
                      fg=ModernTheme.DARK['text'], activebackground=ModernTheme.DARK['accent'],
                      activeforeground='white')
        
        menu.add_command(label=f"👑 Op {player}", command=self.op_player)
        menu.add_command(label=f"👤 Deop {player}", command=self.deop_player)
        menu.add_separator()
        menu.add_command(label=f"💬 Message {player}", command=self.message_player)
        menu.add_command(label=f"🎮 Change Gamemode", command=self.change_gamemode)
        menu.add_separator()
        menu.add_command(label=f"🚫 Kick {player}", command=self.kick_player)
        menu.add_command(label=f"🔨 Ban {player}", command=self.ban_player)
        
        # Show menu at mouse position
        try:
            menu.tk_popup(self.tree.winfo_pointerx(), self.tree.winfo_pointery())
        finally:
            menu.grab_release()
