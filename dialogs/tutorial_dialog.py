"""Interactive tutorial dialog"""
import tkinter as tk
from tkinter import ttk
from ui_components import ModernTheme

class TutorialDialog:
    def __init__(self, parent, app):
        self.app = app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Tutorial - Minecraft Server Manager")
        self.dialog.geometry("900x700")
        self.dialog.configure(bg=ModernTheme.DARK['bg'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.current_page = 0
        self.pages = self.create_pages()
        
        self.create_ui()
        self.show_page(0)
    
    def create_ui(self):
        # Header
        header = tk.Frame(self.dialog, bg=ModernTheme.DARK['surface'],
                         highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        header.pack(fill=tk.X)
        
        tk.Label(header, text="📚 Quick Start Tutorial",
                font=('Segoe UI', 20, 'bold'),
                bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        # Scrollable content area
        content_container = tk.Frame(self.dialog, bg=ModernTheme.DARK['bg'])
        content_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create canvas and scrollbar
        canvas = tk.Canvas(content_container, bg=ModernTheme.DARK['bg'],
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(content_container, orient=tk.VERTICAL,
                                command=canvas.yview)
        
        self.content_frame = tk.Frame(canvas, bg=ModernTheme.DARK['bg'])
        
        # Configure scrolling
        self.content_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=self.content_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Pack canvas and scrollbar
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mousewheel
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        self._mousewheel_handler = _on_mousewheel
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        self.canvas = canvas
        
        # Unbind on close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        """Clean up before closing"""
        try:
            self.canvas.unbind_all("<MouseWheel>")
        except:
            pass
        self.dialog.destroy()
        
        # Navigation
        nav_frame = tk.Frame(self.dialog, bg=ModernTheme.DARK['surface'],
                            highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        nav_frame.pack(fill=tk.X, side=tk.BOTTOM)
        
        btn_container = tk.Frame(nav_frame, bg=ModernTheme.DARK['surface'])
        btn_container.pack(pady=15)
        
        self.prev_btn = tk.Button(btn_container, text="⬅️ Previous",
                                  command=self.prev_page,
                                  bg=ModernTheme.DARK['surface_light'],
                                  fg=ModernTheme.DARK['text'],
                                  font=('Segoe UI', 11), relief='flat',
                                  padx=20, pady=10, cursor='hand2', borderwidth=0)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.page_label = tk.Label(btn_container, text="",
                                   bg=ModernTheme.DARK['surface'],
                                   fg=ModernTheme.DARK['text'],
                                   font=('Segoe UI', 11))
        self.page_label.pack(side=tk.LEFT, padx=20)
        
        self.next_btn = tk.Button(btn_container, text="Next ➡️",
                                 command=self.next_page,
                                 bg=ModernTheme.DARK['accent'], fg='white',
                                 font=('Segoe UI', 11, 'bold'), relief='flat',
                                 padx=20, pady=10, cursor='hand2', borderwidth=0)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        tk.Button(btn_container, text="Skip Tutorial",
                 command=self.dialog.destroy,
                 bg=ModernTheme.DARK['surface_light'],
                 fg=ModernTheme.DARK['text_secondary'],
                 font=('Segoe UI', 10), relief='flat',
                 padx=15, pady=8, cursor='hand2', borderwidth=0).pack(side=tk.LEFT, padx=20)
    
    def create_pages(self):
        return [
            self.page_welcome,
            self.page_connection,
            self.page_installation,
            self.page_mods,
            self.page_players,
            self.page_admin_commands,
            self.page_backups,
            self.page_done
        ]
    
    def show_page(self, page_num):
        # Clear content
        for widget in self.content_frame.winfo_children():
            widget.destroy()
        
        # Show page
        self.pages[page_num]()
        
        # Update navigation
        self.page_label.config(text=f"Page {page_num + 1} of {len(self.pages)}")
        self.prev_btn.config(state=tk.NORMAL if page_num > 0 else tk.DISABLED)
        
        if page_num == len(self.pages) - 1:
            self.next_btn.config(text="✅ Finish", bg=ModernTheme.DARK['success'])
        else:
            self.next_btn.config(text="Next ➡️", bg=ModernTheme.DARK['accent'])
    
    def next_page(self):
        if self.current_page < len(self.pages) - 1:
            self.current_page += 1
            self.show_page(self.current_page)
        else:
            self.dialog.destroy()
    
    def prev_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.show_page(self.current_page)
    
    def create_section(self, parent, title, content, icon=""):
        frame = tk.Frame(parent, bg=ModernTheme.DARK['surface'],
                        highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        tk.Label(frame, text=f"{icon} {title}",
                font=('Segoe UI', 14, 'bold'),
                bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['accent']).pack(anchor='w', padx=20, pady=(15, 10))
        
        tk.Label(frame, text=content,
                font=('Segoe UI', 11),
                bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['text'],
                justify=tk.LEFT, wraplength=800).pack(anchor='w', padx=20, pady=(0, 15))
        
        return frame
    
    def page_welcome(self):
        tk.Label(self.content_frame, text="👋 Welcome!",
                font=('Segoe UI', 24, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        self.create_section(self.content_frame, "What is this?", 
                           "Minecraft Server Manager is a powerful tool to manage your Minecraft server remotely. "
                           "You can start/stop servers, install mods, manage players, and much more!", "🎮")
        
        self.create_section(self.content_frame, "What you'll learn",
                           "• How to connect to your server via SSH\n"
                           "• Installing different server types (Vanilla, Fabric, Forge, Paper, Purpur)\n"
                           "• Managing mods and modpacks\n"
                           "• Player management and admin commands\n"
                           "• Creating backups and managing files", "📚")
    
    def page_connection(self):
        tk.Label(self.content_frame, text="🔌 Connecting to Your Server",
                font=('Segoe UI', 20, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        self.create_section(self.content_frame, "What you need",
                           "• Server IP address or hostname\n"
                           "• SSH port (usually 22)\n"
                           "• Username (usually 'root')\n"
                           "• Password or SSH key", "📋")
        
        self.create_section(self.content_frame, "How to connect",
                           "1. Enter your server's IP address\n"
                           "2. Enter the SSH port (default: 22)\n"
                           "3. Enter your username\n"
                           "4. Enter your password\n"
                           "5. Click 'Connect'\n\n"
                           "💡 Tip: Your hosting provider should have given you these details!", "🔑")
    
    def page_installation(self):
        tk.Label(self.content_frame, text="📦 Installing a Server",
                font=('Segoe UI', 20, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        self.create_section(self.content_frame, "Server Types",
                           "🧵 Fabric - Best for mods, lightweight, fast\n"
                           "🔨 Forge - Most mods available, heavier\n"
                           "📦 Vanilla - Official Minecraft, no mods\n"
                           "📄 Paper - Optimized vanilla, great performance\n"
                           "💜 Purpur - Paper + extra features", "🎯")
        
        self.create_section(self.content_frame, "Installation Steps",
                           "1. Go to Dashboard tab\n"
                           "2. Click '📦 Install Server'\n"
                           "3. Choose server type (Fabric recommended for mods)\n"
                           "4. Select Minecraft version\n"
                           "5. Choose memory allocation (4GB recommended)\n"
                           "6. Check 'Accept EULA' and 'Auto-start'\n"
                           "7. Click 'Install' and wait 5-10 minutes\n\n"
                           "☕ Java 21 will be installed automatically!", "⚙️")
    
    def page_mods(self):
        tk.Label(self.content_frame, text="🔧 Managing Mods",
                font=('Segoe UI', 20, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        self.create_section(self.content_frame, "Adding Mods",
                           "📤 Upload Mod: Upload .jar files from your computer\n"
                           "📥 Download from URL: Paste direct download link from CurseForge/Modrinth\n"
                           "⚡ Quick Install: One-click install popular mods (Fabric API, Lithium, etc.)\n\n"
                           "⚠️ Important: Always restart server after adding/removing mods!", "➕")
        
        self.create_section(self.content_frame, "Managing Mods",
                           "🔍 Search: Type to filter mods by name\n"
                           "🗑️ Delete: Select a mod and click delete\n"
                           "🧹 Clear All: Remove all mods at once\n"
                           "🔄 Refresh: Update the mod list\n\n"
                           "💡 Tip: Check mod compatibility with your Minecraft version!", "🛠️")
    
    def page_players(self):
        tk.Label(self.content_frame, text="👥 Player Management",
                font=('Segoe UI', 20, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        self.create_section(self.content_frame, "Player Actions",
                           "👑 Op Player: Give admin permissions\n"
                           "👤 Deop Player: Remove admin permissions\n"
                           "🚫 Kick Player: Temporarily remove from server\n"
                           "🔨 Ban Player: Permanently ban a player\n"
                           "✅ Unban Player: Remove a ban", "⚡")
        
        self.create_section(self.content_frame, "Whitelist",
                           "🔒 Enable Whitelist: Only whitelisted players can join\n"
                           "🔓 Disable Whitelist: Anyone can join\n"
                           "➕ Add to Whitelist: Allow a player to join\n"
                           "➖ Remove from Whitelist: Revoke access\n\n"
                           "💡 Tip: Use whitelist for private servers!", "📋")
    
    def page_admin_commands(self):
        tk.Label(self.content_frame, text="⚡ Admin Commands",
                font=('Segoe UI', 20, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        self.create_section(self.content_frame, "Quick Commands",
                           "☀️ /time set day - Set time to day\n"
                           "🌙 /time set night - Set time to night\n"
                           "☀️ /weather clear - Clear weather\n"
                           "🌧️ /weather rain - Make it rain\n"
                           "⚡ /weather thunder - Thunderstorm\n"
                           "🎮 /gamemode creative @a - Creative mode for all\n"
                           "🎮 /gamemode survival @a - Survival mode for all\n"
                           "💾 /save-all - Save the world", "🎯")
        
        self.create_section(self.content_frame, "Advanced Commands",
                           "🚀 /tp <player> <x> <y> <z> - Teleport player\n"
                           "🎁 /give <player> <item> <amount> - Give items\n"
                           "📢 /say <message> - Broadcast message\n"
                           "👥 /list - Show online players\n"
                           "🔄 /reload - Reload server config\n"
                           "⚙️ /difficulty <level> - Change difficulty\n\n"
                           "💡 Tip: Use Tab key for command autocomplete!", "🔧")
    
    def page_backups(self):
        tk.Label(self.content_frame, text="💾 Backups & Files",
                font=('Segoe UI', 20, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['accent']).pack(pady=20)
        
        self.create_section(self.content_frame, "Creating Backups",
                           "1. Go to Files tab\n"
                           "2. Click '💾 Backup World'\n"
                           "3. Wait for backup to complete\n"
                           "4. Backup saved with timestamp\n\n"
                           "⚠️ Always backup before major changes!", "📦")
        
        self.create_section(self.content_frame, "File Management",
                           "📂 Browse Files: View all server files\n"
                           "📄 View Logs: Check server logs for errors\n"
                           "🗑️ Clear Logs: Remove old log files\n"
                           "📋 List Backups: See all available backups\n\n"
                           "💡 Tip: Create backups weekly and before updates!", "🗂️")
    
    def page_done(self):
        tk.Label(self.content_frame, text="🎉 You're Ready!",
                font=('Segoe UI', 24, 'bold'),
                bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['success']).pack(pady=30)
        
        self.create_section(self.content_frame, "Quick Start Checklist",
                           "✅ Connect to your server\n"
                           "✅ Install Minecraft server (Fabric recommended)\n"
                           "✅ Add essential mods (Fabric API, Lithium, etc.)\n"
                           "✅ Configure server.properties\n"
                           "✅ Set up whitelist if needed\n"
                           "✅ Create your first backup\n"
                           "✅ Start playing!", "📝")
        
        self.create_section(self.content_frame, "Need Help?",
                           "📚 Check USER_GUIDE.md for detailed instructions\n"
                           "🔍 View console for error messages\n"
                           "💬 Join Minecraft server admin communities\n"
                           "🐛 Report bugs on GitHub\n\n"
                           "Good luck with your server! 🎮", "❓")
