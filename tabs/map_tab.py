"""Map Tab - Real-time world map and player tracking"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import webbrowser
from ui_components import ModernTheme, Card

class MapTab:
    def __init__(self, notebook, app):
        self.app = app
        self.frame = tk.Frame(notebook, bg=ModernTheme.DARK['bg'])
        
        self.map_mod = None  # 'dynmap', 'bluemap', 'squaremap', or None
        self.map_url = None
        self.map_port = None
        
        self.setup_ui()
    
    def setup_ui(self):
        # Header
        header = Card(self.frame)
        header.pack(fill=tk.X, padx=10, pady=10)
        
        header_content = tk.Frame(header, bg=ModernTheme.DARK['surface'])
        header_content.pack(fill=tk.X, padx=20, pady=15)
        
        title = tk.Label(header_content, text="🗺️ World Map",
                        font=('Segoe UI', 18, 'bold'),
                        bg=ModernTheme.DARK['surface'],
                        fg=ModernTheme.DARK['accent'])
        title.pack(side=tk.LEFT)
        
        self.status_label = tk.Label(header_content, text="No map mod installed",
                                     font=('Segoe UI', 11),
                                     bg=ModernTheme.DARK['surface'],
                                     fg=ModernTheme.DARK['text_secondary'])
        self.status_label.pack(side=tk.RIGHT)
        
        # Map mod installation
        install_card = Card(self.frame)
        install_card.pack(fill=tk.X, padx=10, pady=10)
        
        install_content = tk.Frame(install_card, bg=ModernTheme.DARK['surface'])
        install_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        tk.Label(install_content, text="📦 Install Map Mod",
                font=('Segoe UI', 14, 'bold'),
                bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['accent']).pack(anchor='w', pady=(0, 10))
        
        tk.Label(install_content, 
                text="Choose a map mod to visualize your world in real-time:",
                font=('Segoe UI', 10),
                bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['text_secondary']).pack(anchor='w', pady=(0, 5))
        
        tk.Label(install_content, 
                text="✨ For Forge servers, use the Quick Install button for automatic setup",
                font=('Segoe UI', 9, 'italic'),
                bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['accent']).pack(anchor='w', pady=(0, 15))
        
        # Map mod options
        mods_frame = tk.Frame(install_content, bg=ModernTheme.DARK['surface'])
        mods_frame.pack(fill=tk.X, pady=10)
        
        # Dynmap
        dynmap_frame = tk.Frame(mods_frame, bg=ModernTheme.DARK['surface_light'],
                               highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        dynmap_frame.pack(fill=tk.X, pady=5)
        
        dynmap_content = tk.Frame(dynmap_frame, bg=ModernTheme.DARK['surface_light'])
        dynmap_content.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(dynmap_content, text="🗺️ Dynmap",
                font=('Segoe UI', 12, 'bold'),
                bg=ModernTheme.DARK['surface_light'],
                fg=ModernTheme.DARK['text']).pack(anchor='w')
        
        tk.Label(dynmap_content, 
                text="Classic map mod with real-time player tracking and markers",
                font=('Segoe UI', 9),
                bg=ModernTheme.DARK['surface_light'],
                fg=ModernTheme.DARK['text_secondary']).pack(anchor='w', pady=(5, 10))
        
        btn_frame = tk.Frame(dynmap_content, bg=ModernTheme.DARK['surface_light'])
        btn_frame.pack(anchor='w')
        
        tk.Button(btn_frame, text="📥 Download",
                 command=lambda: self.install_map_mod('dynmap'),
                 bg=ModernTheme.DARK['accent'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(btn_frame, text="⚡ Quick Install (Forge)",
                 command=lambda: self.quick_install_dynmap_forge(),
                 bg=ModernTheme.DARK['success'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2').pack(side=tk.LEFT)
        
        # BlueMap
        bluemap_frame = tk.Frame(mods_frame, bg=ModernTheme.DARK['surface_light'],
                                highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        bluemap_frame.pack(fill=tk.X, pady=5)
        
        bluemap_content = tk.Frame(bluemap_frame, bg=ModernTheme.DARK['surface_light'])
        bluemap_content.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(bluemap_content, text="🌊 BlueMap",
                font=('Segoe UI', 12, 'bold'),
                bg=ModernTheme.DARK['surface_light'],
                fg=ModernTheme.DARK['text']).pack(anchor='w')
        
        tk.Label(bluemap_content, 
                text="Modern 3D map with smooth rendering and beautiful visuals",
                font=('Segoe UI', 9),
                bg=ModernTheme.DARK['surface_light'],
                fg=ModernTheme.DARK['text_secondary']).pack(anchor='w', pady=(5, 10))
        
        tk.Button(bluemap_content, text="Install BlueMap",
                 command=lambda: self.install_map_mod('bluemap'),
                 bg=ModernTheme.DARK['info'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2').pack(anchor='w')
        
        # Squaremap
        squaremap_frame = tk.Frame(mods_frame, bg=ModernTheme.DARK['surface_light'],
                                  highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        squaremap_frame.pack(fill=tk.X, pady=5)
        
        squaremap_content = tk.Frame(squaremap_frame, bg=ModernTheme.DARK['surface_light'])
        squaremap_content.pack(fill=tk.X, padx=15, pady=15)
        
        tk.Label(squaremap_content, text="🗺️ Squaremap",
                font=('Segoe UI', 12, 'bold'),
                bg=ModernTheme.DARK['surface_light'],
                fg=ModernTheme.DARK['text']).pack(anchor='w')
        
        tk.Label(squaremap_content, 
                text="Lightweight and fast map with minimal performance impact",
                font=('Segoe UI', 9),
                bg=ModernTheme.DARK['surface_light'],
                fg=ModernTheme.DARK['text_secondary']).pack(anchor='w', pady=(5, 10))
        
        tk.Button(squaremap_content, text="Install Squaremap",
                 command=lambda: self.install_map_mod('squaremap'),
                 bg=ModernTheme.DARK['success'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=20, pady=8, cursor='hand2').pack(anchor='w')
        
        # Map viewer
        viewer_card = Card(self.frame)
        viewer_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        viewer_content = tk.Frame(viewer_card, bg=ModernTheme.DARK['surface'])
        viewer_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=15)
        
        tk.Label(viewer_content, text="🌍 Map Viewer",
                font=('Segoe UI', 14, 'bold'),
                bg=ModernTheme.DARK['surface'],
                fg=ModernTheme.DARK['accent']).pack(anchor='w', pady=(0, 10))
        
        # Map controls
        controls_frame = tk.Frame(viewer_content, bg=ModernTheme.DARK['surface'])
        controls_frame.pack(fill=tk.X, pady=10)
        
        tk.Button(controls_frame, text="🔄 Detect Map",
                 command=self.detect_map,
                 bg=ModernTheme.DARK['accent'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls_frame, text="🌐 Open in Browser",
                 command=self.open_map_browser,
                 bg=ModernTheme.DARK['info'], fg='white',
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        tk.Button(controls_frame, text="📊 Map Stats",
                 command=self.show_map_stats,
                 bg=ModernTheme.DARK['surface_light'], fg=ModernTheme.DARK['text'],
                 font=('Segoe UI', 10, 'bold'), relief='flat',
                 padx=15, pady=8, cursor='hand2').pack(side=tk.LEFT, padx=5)
        
        # Map info display
        self.map_info = tk.Text(viewer_content, height=15,
                               bg=ModernTheme.DARK['surface_light'],
                               fg=ModernTheme.DARK['text'],
                               font=('Consolas', 10), relief='flat',
                               wrap=tk.WORD)
        self.map_info.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.map_info.insert('1.0', 
            "📍 Map Viewer\n\n"
            "Install a map mod to visualize your Minecraft world in real-time.\n\n"
            "Features:\n"
            "• Real-time player positions\n"
            "• Chunk visualization\n"
            "• Block-level detail\n"
            "• Markers and waypoints\n"
            "• Web-based interface\n\n"
            "Click 'Detect Map' after installing a map mod to get started."
        )
        self.map_info.config(state=tk.DISABLED)
    
    def install_map_mod(self, mod_type):
        """Install a map mod"""
        if not self.app.ssh:
            messagebox.showerror("Error", "Not connected to server")
            return
        
        def install():
            try:
                self.app.log(f"📦 Installing {mod_type}...")
                
                # Detect server type - check jar files and folders
                output, _ = self.app.ssh.execute(
                    "cd ~/minecraft && ls *.jar 2>/dev/null && ls -d */ 2>/dev/null"
                )
                
                # Check for forge first (more specific)
                if 'forge' in output.lower():
                    server_type = 'forge'
                elif 'fabric' in output.lower():
                    server_type = 'fabric'
                elif 'paper' in output.lower() or 'spigot' in output.lower():
                    server_type = 'paper'
                else:
                    server_type = 'vanilla'
                
                self.app.log(f"Detected server type: {server_type}")
                
                # Forge-specific URLs and instructions
                if server_type == 'forge':
                    forge_urls = {
                        'dynmap': {
                            'url': 'https://www.curseforge.com/minecraft/mc-mods/dynmapforge',
                            'download': 'https://www.curseforge.com/minecraft/mc-mods/dynmapforge/files',
                            'note': 'Works with Forge - most popular choice'
                        },
                        'bluemap': {
                            'url': 'https://www.curseforge.com/minecraft/mc-mods/bluemap',
                            'download': 'https://modrinth.com/plugin/bluemap/versions',
                            'note': 'Modern 3D map - supports Forge'
                        },
                        'squaremap': {
                            'url': 'https://modrinth.com/plugin/squaremap',
                            'download': 'https://modrinth.com/plugin/squaremap/versions',
                            'note': 'Lightweight - check Forge compatibility'
                        }
                    }
                    
                    mod_info = forge_urls[mod_type]
                    
                    message = (
                        f"Installing {mod_type.upper()} for Forge:\n\n"
                        f"📝 {mod_info['note']}\n\n"
                        f"Steps:\n"
                        f"1. Download page will open in browser\n"
                        f"2. Download the Forge version for your MC version\n"
                        f"3. Upload the .jar file to ~/minecraft/mods/\n"
                        f"4. Restart your server\n"
                        f"5. Click 'Detect Map' to find the web interface\n\n"
                        f"Default ports:\n"
                        f"• Dynmap: 8123\n"
                        f"• BlueMap: 8100\n"
                        f"• Squaremap: 8080\n\n"
                        f"Tip: Use the Mods tab to upload the downloaded file!"
                    )
                    
                    messagebox.showinfo(f"Install {mod_type.upper()}", message)
                    webbrowser.open(mod_info['download'])
                    
                else:
                    # Other server types
                    urls = {
                        'dynmap': 'https://modrinth.com/plugin/dynmap',
                        'bluemap': 'https://modrinth.com/plugin/bluemap',
                        'squaremap': 'https://modrinth.com/plugin/squaremap'
                    }
                    
                    message = (
                        f"To install {mod_type.upper()}:\n\n"
                        f"1. Visit: {urls[mod_type]}\n"
                        f"2. Download the {server_type} version\n"
                        f"3. Upload to your mods/plugins folder\n"
                        f"4. Restart the server\n"
                        f"5. Click 'Detect Map' to find the web interface\n\n"
                        f"Default ports:\n"
                        f"• Dynmap: 8123\n"
                        f"• BlueMap: 8100\n"
                        f"• Squaremap: 8080"
                    )
                    
                    messagebox.showinfo(f"Install {mod_type.upper()}", message)
                    webbrowser.open(urls[mod_type])
                
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
                messagebox.showerror("Error", str(e))
        
        threading.Thread(target=install, daemon=True).start()
    
    def quick_install_dynmap_forge(self):
        """Quick install Dynmap for Forge servers"""
        if not self.app.ssh:
            messagebox.showerror("Error", "Not connected to server")
            return
        
        if not messagebox.askyesno("Quick Install", 
            "This will download and install Dynmap for Forge.\n\n"
            "Make sure your server is stopped first!\n\n"
            "Continue?"):
            return
        
        def install():
            try:
                self.app.log("⚡ Quick installing Dynmap for Forge...")
                
                # Detect Minecraft version
                self.app.log("🔍 Detecting Minecraft version...")
                output, _ = self.app.ssh.execute(
                    "cd ~/minecraft && ls *.jar | grep -E 'forge|minecraft' | head -1"
                )
                
                # Try to extract version from jar name
                version = "1.20.1"  # Default fallback
                if "1.21" in output:
                    version = "1.21.1"
                elif "1.20" in output:
                    version = "1.20.1"
                elif "1.19" in output:
                    version = "1.19.2"
                elif "1.18" in output:
                    version = "1.18.2"
                elif "1.16" in output:
                    version = "1.16.5"
                
                self.app.log(f"📌 Detected version: {version}")
                
                # Download Dynmap (using a stable version URL)
                self.app.log("📥 Downloading Dynmap...")
                
                # CurseForge direct download (you'll need to update this URL for specific versions)
                download_cmd = (
                    "cd ~/minecraft/mods && "
                    "wget -O Dynmap-forge.jar "
                    "'https://mediafilez.forgecdn.net/files/5067/684/Dynmap-3.7-forge-1.20.jar' "
                    "2>&1"
                )
                
                output, _ = self.app.ssh.execute(download_cmd)
                
                if "saved" in output.lower() or "downloaded" in output.lower():
                    self.app.log("✅ Dynmap downloaded successfully")
                    
                    messagebox.showinfo("Success", 
                        "Dynmap installed successfully!\n\n"
                        "Next steps:\n"
                        "1. Restart your server\n"
                        "2. Wait for Dynmap to generate config\n"
                        "3. Click 'Detect Map' to find the web interface\n"
                        "4. Access map at: http://your-server-ip:8123\n\n"
                        "Note: Make sure port 8123 is open in your firewall!")
                else:
                    self.app.log("⚠️ Download may have failed, check manually")
                    messagebox.showwarning("Check Installation",
                        "Download completed but couldn't verify.\n\n"
                        "Please check ~/minecraft/mods/ folder\n"
                        "and restart your server.")
                
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
                messagebox.showerror("Error", 
                    f"Installation failed: {e}\n\n"
                    "Try manual installation instead.")
        
        threading.Thread(target=install, daemon=True).start()
    
    def detect_map(self):
        """Detect installed map mod and get URL"""
        if not self.app.ssh:
            messagebox.showerror("Error", "Not connected to server")
            return
        
        def detect():
            try:
                self.app.log("🔍 Detecting map mod...")
                
                # Check for map mods in mods folder
                output, _ = self.app.ssh.execute(
                    "ls ~/minecraft/mods/ 2>/dev/null | grep -iE 'dynmap|bluemap|squaremap'"
                )
                
                self.app.log(f"Found mods: {output.strip()}")
                
                if 'dynmap' in output.lower():
                    self.map_mod = 'dynmap'
                    self.map_port = 8123
                elif 'bluemap' in output.lower():
                    self.map_mod = 'bluemap'
                    self.map_port = 8100
                elif 'squaremap' in output.lower():
                    self.map_mod = 'squaremap'
                    self.map_port = 8080
                else:
                    self.app.log("❌ No map mod detected in mods folder")
                    messagebox.showinfo("Not Found", 
                        "No map mod detected in ~/minecraft/mods/\n\n"
                        "Make sure:\n"
                        "1. Dynmap is uploaded to the mods folder\n"
                        "2. Server has been restarted\n"
                        "3. Check server logs for any errors")
                    return
                
                # Check if server is running
                status_output, _ = self.app.ssh.execute(
                    "screen -ls | grep minecraft"
                )
                
                if not status_output.strip():
                    self.app.log("⚠️ Server is not running")
                    messagebox.showwarning("Server Stopped",
                        f"{self.map_mod.upper()} detected but server is not running!\n\n"
                        f"Start your server first, then try again.")
                    return
                
                # Check if Dynmap web server is running
                self.app.log(f"🔍 Checking if {self.map_mod} web server is running on port {self.map_port}...")
                port_check, _ = self.app.ssh.execute(
                    f"netstat -tuln | grep :{self.map_port} || ss -tuln | grep :{self.map_port}"
                )
                
                # Get server IP
                hostname = self.app.ssh.hostname
                self.map_url = f"http://{hostname}:{self.map_port}"
                
                if port_check.strip():
                    self.app.log(f"✅ Found {self.map_mod.upper()} - Web server is running!")
                    self.status_label.config(
                        text=f"{self.map_mod.upper()} running on port {self.map_port}",
                        fg=ModernTheme.DARK['success']
                    )
                else:
                    self.app.log(f"⚠️ {self.map_mod.upper()} found but web server not detected on port {self.map_port}")
                    self.status_label.config(
                        text=f"{self.map_mod.upper()} detected (web server may be starting...)",
                        fg=ModernTheme.DARK['warning']
                    )
                
                # Update info
                self.map_info.config(state=tk.NORMAL)
                self.map_info.delete('1.0', tk.END)
                
                if port_check.strip():
                    info_text = (
                        f"🗺️ {self.map_mod.upper()} Detected & Running!\n\n"
                        f"Map URL: {self.map_url}\n\n"
                        f"✅ Web server is active on port {self.map_port}\n\n"
                        f"Access your map:\n"
                        f"1. Click 'Open in Browser' below\n"
                        f"2. Or visit: {self.map_url}\n\n"
                        f"Features:\n"
                        f"• Real-time player tracking\n"
                        f"• Interactive world map\n"
                        f"• Zoom and pan controls\n"
                        f"• Markers and waypoints\n"
                        f"• Chat integration\n\n"
                        f"Tip: Bookmark the URL for easy access!"
                    )
                    msg_title = "Map Ready!"
                    msg_text = (
                        f"✅ {self.map_mod.upper()} is running!\n\n"
                        f"URL: {self.map_url}\n\n"
                        f"Click 'Open in Browser' to view your map."
                    )
                else:
                    info_text = (
                        f"🗺️ {self.map_mod.upper()} Detected\n\n"
                        f"Map URL: {self.map_url}\n\n"
                        f"⚠️ Web server not detected on port {self.map_port}\n\n"
                        f"Troubleshooting:\n"
                        f"1. Wait 30-60 seconds for server to fully start\n"
                        f"2. Check server console for Dynmap messages\n"
                        f"3. Make sure port {self.map_port} is open in firewall\n"
                        f"4. Check ~/minecraft/plugins/dynmap/configuration.txt\n"
                        f"5. Try clicking 'Detect Map' again\n\n"
                        f"If still not working:\n"
                        f"• Check server logs for errors\n"
                        f"• Verify Dynmap is compatible with your Forge version\n"
                        f"• Try restarting the server"
                    )
                    msg_title = "Map Detected"
                    msg_text = (
                        f"⚠️ {self.map_mod.upper()} detected but web server not running yet.\n\n"
                        f"Wait for server to fully start, then try:\n"
                        f"• Click 'Detect Map' again\n"
                        f"• Check server console for errors\n"
                        f"• Visit: {self.map_url}"
                    )
                
                self.map_info.insert('1.0', info_text)
                self.map_info.config(state=tk.DISABLED)
                
                messagebox.showinfo(msg_title, msg_text)
                
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
                messagebox.showerror("Error", str(e))
        
        threading.Thread(target=detect, daemon=True).start()
    
    def open_map_browser(self):
        """Open map in web browser"""
        if not self.map_url:
            messagebox.showwarning("No Map", "Click 'Detect Map' first")
            return
        
        self.app.log(f"🌐 Opening map: {self.map_url}")
        webbrowser.open(self.map_url)
    
    def show_map_stats(self):
        """Show map statistics"""
        if not self.app.ssh:
            messagebox.showerror("Error", "Not connected to server")
            return
        
        def get_stats():
            try:
                self.app.log("📊 Fetching map stats...")
                
                # Get world info
                output, _ = self.app.ssh.execute(
                    "du -sh ~/minecraft/world* 2>/dev/null"
                )
                
                # Get chunk count (approximate)
                chunk_output, _ = self.app.ssh.execute(
                    "find ~/minecraft/world*/region -name '*.mca' 2>/dev/null | wc -l"
                )
                
                # Get player data
                player_output, _ = self.app.ssh.execute(
                    "ls ~/minecraft/world*/playerdata/*.dat 2>/dev/null | wc -l"
                )
                
                stats = (
                    f"📊 World Statistics\n\n"
                    f"World Size:\n{output}\n\n"
                    f"Region Files: {chunk_output.strip()}\n"
                    f"Player Data Files: {player_output.strip()}\n\n"
                    f"Map Mod: {self.map_mod.upper() if self.map_mod else 'None'}\n"
                    f"Map URL: {self.map_url if self.map_url else 'Not detected'}"
                )
                
                self.map_info.config(state=tk.NORMAL)
                self.map_info.delete('1.0', tk.END)
                self.map_info.insert('1.0', stats)
                self.map_info.config(state=tk.DISABLED)
                
                self.app.log("✅ Stats loaded")
                
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
                messagebox.showerror("Error", str(e))
        
        threading.Thread(target=get_stats, daemon=True).start()
