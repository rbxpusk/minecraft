"""Server installation dialog"""
import tkinter as tk
from tkinter import ttk, messagebox
import threading
from ui_components import ModernTheme, ModernButton, ModernEntry, Card

class InstallDialog:
    def __init__(self, parent, app):
        self.app = app
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Install Minecraft Server")
        self.dialog.geometry("700x650")
        self.dialog.configure(bg=ModernTheme.DARK['bg'])
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Version lists
        self.versions = {
            'fabric': ['1.21.3', '1.21.1', '1.21', '1.20.6', '1.20.4', '1.20.1', '1.19.4', '1.19.2', '1.18.2', '1.17.1', '1.16.5'],
            'forge': ['1.21.1', '1.20.6', '1.20.4', '1.20.1', '1.19.4', '1.19.2', '1.18.2', '1.17.1', '1.16.5', '1.12.2'],
            'vanilla': ['1.21.3', '1.21.1', '1.21', '1.20.6', '1.20.4', '1.20.1', '1.19.4', '1.19.2', '1.18.2', '1.17.1', '1.16.5'],
            'paper': ['1.21.3', '1.21.1', '1.21', '1.20.6', '1.20.4', '1.20.1', '1.19.4', '1.19.2', '1.18.2', '1.17.1', '1.16.5'],
            'purpur': ['1.21.1', '1.21', '1.20.6', '1.20.4', '1.20.1', '1.19.4', '1.19.2', '1.18.2', '1.17.1', '1.16.5']
        }
        
        self.create_ui()
    
    def create_ui(self):
        card = tk.Frame(self.dialog, bg=ModernTheme.DARK['surface'],
                       highlightthickness=1, highlightbackground=ModernTheme.DARK['border'])
        card.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Create scrollable content
        canvas = tk.Canvas(card, bg=ModernTheme.DARK['surface'],
                          highlightthickness=0)
        scrollbar = tk.Scrollbar(card, orient=tk.VERTICAL, command=canvas.yview)
        
        content = tk.Frame(canvas, bg=ModernTheme.DARK['surface'])
        
        content.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=content, anchor="nw", width=640)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=30, pady=30)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=30)
        
        # Bind mousewheel
        def _on_mousewheel(event):
            try:
                canvas.yview_scroll(int(-1*(event.delta/120)), "units")
            except:
                pass
        
        self._mousewheel_handler = _on_mousewheel
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # Unbind on close
        self.dialog.protocol("WM_DELETE_WINDOW", self.on_close)
    
    def on_close(self):
        """Clean up before closing"""
        try:
            self.dialog.unbind_all("<MouseWheel>")
        except:
            pass
        self.dialog.destroy()
        
        title = tk.Label(content, text="📦 Server Installation",
                        font=('Segoe UI', 20, 'bold'),
                        bg=ModernTheme.DARK['surface'],
                        fg=ModernTheme.DARK['accent'])
        title.pack(pady=(0, 25))
        
        # Server Type
        type_label = tk.Label(content, text="Server Type:",
                             bg=ModernTheme.DARK['surface'], fg=ModernTheme.DARK['text'],
                             font=('Segoe UI', 11, 'bold'))
        type_label.pack(anchor='w', pady=(10, 5))
        
        type_frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
        type_frame.pack(fill=tk.X, pady=5)
        
        self.server_type = tk.StringVar(value="fabric")
        self.server_type.trace('w', self.update_versions)
        
        types = [
            ("🧵 Fabric (Recommended)", "fabric"),
            ("🔨 Forge", "forge"),
            ("📦 Vanilla", "vanilla"),
            ("📄 Paper (Performance)", "paper"),
            ("💜 Purpur (Features)", "purpur")
        ]
        
        for i, (text, value) in enumerate(types):
            rb = tk.Radiobutton(type_frame, text=text, variable=self.server_type,
                               value=value, bg=ModernTheme.DARK['surface'],
                               fg=ModernTheme.DARK['text'],
                               selectcolor=ModernTheme.DARK['surface_light'],
                               font=('Segoe UI', 10), activebackground=ModernTheme.DARK['surface'],
                               activeforeground=ModernTheme.DARK['accent'])
            rb.grid(row=i//3, column=i%3, sticky='w', padx=10, pady=5)
        
        # Version
        version_label = tk.Label(content, text="Minecraft Version:",
                                bg=ModernTheme.DARK['surface'], fg=ModernTheme.DARK['text'],
                                font=('Segoe UI', 11, 'bold'))
        version_label.pack(anchor='w', pady=(15, 5))
        
        version_frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
        version_frame.pack(fill=tk.X, pady=5)
        
        self.version_combo = ttk.Combobox(version_frame, values=self.versions['fabric'],
                                         font=('Segoe UI', 10), state='readonly', width=15)
        self.version_combo.set('1.21.3')
        self.version_combo.pack(side=tk.LEFT, ipady=5)
        
        # Memory
        memory_label = tk.Label(content, text="Memory Allocation:",
                               bg=ModernTheme.DARK['surface'], fg=ModernTheme.DARK['text'],
                               font=('Segoe UI', 11, 'bold'))
        memory_label.pack(anchor='w', pady=(15, 5))
        
        memory_frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
        memory_frame.pack(fill=tk.X, pady=5)
        
        self.memory_var = tk.StringVar(value="4")
        
        memory_options = [
            ("2 GB (Minimum)", "2"),
            ("4 GB (Recommended)", "4"),
            ("6 GB (Good)", "6"),
            ("8 GB (Great)", "8"),
            ("12 GB (Excellent)", "12"),
            ("16 GB (Maximum)", "16")
        ]
        
        for i, (text, value) in enumerate(memory_options):
            rb = tk.Radiobutton(memory_frame, text=text, variable=self.memory_var,
                               value=value, bg=ModernTheme.DARK['surface'],
                               fg=ModernTheme.DARK['text'],
                               selectcolor=ModernTheme.DARK['surface_light'],
                               font=('Segoe UI', 9))
            rb.grid(row=i//3, column=i%3, sticky='w', padx=10, pady=3)
        
        # Additional Options
        options_label = tk.Label(content, text="Additional Options:",
                                bg=ModernTheme.DARK['surface'], fg=ModernTheme.DARK['text'],
                                font=('Segoe UI', 11, 'bold'))
        options_label.pack(anchor='w', pady=(15, 5))
        
        self.auto_start = tk.BooleanVar(value=True)
        self.accept_eula = tk.BooleanVar(value=True)
        
        tk.Checkbutton(content, text="✅ Accept EULA automatically",
                      variable=self.accept_eula, bg=ModernTheme.DARK['surface'],
                      fg=ModernTheme.DARK['text'], selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 9)).pack(anchor='w', pady=2)
        
        tk.Checkbutton(content, text="🚀 Start server after installation",
                      variable=self.auto_start, bg=ModernTheme.DARK['surface'],
                      fg=ModernTheme.DARK['text'], selectcolor=ModernTheme.DARK['surface_light'],
                      font=('Segoe UI', 9)).pack(anchor='w', pady=2)
        
        # Info
        info = tk.Label(content, 
                       text="⏱️ Installation takes 5-10 minutes\n"
                            "☕ Java 21 will be installed automatically\n"
                            "📦 Server files will be placed in /root/minecraft",
                       bg=ModernTheme.DARK['surface'],
                       fg=ModernTheme.DARK['text_secondary'],
                       font=('Segoe UI', 9), justify=tk.LEFT)
        info.pack(pady=20)
        
        # Buttons
        btn_frame = tk.Frame(content, bg=ModernTheme.DARK['surface'])
        btn_frame.pack(pady=(10, 0))
        
        install_btn = tk.Button(btn_frame, text="📦 Install Server", command=self.install,
                               bg=ModernTheme.DARK['success'], fg='white',
                               font=('Segoe UI', 11, 'bold'), relief='flat',
                               padx=30, pady=12, cursor='hand2', borderwidth=0)
        install_btn.pack(side=tk.LEFT, padx=5)
        
        cancel_btn = tk.Button(btn_frame, text="Cancel", command=self.dialog.destroy,
                              bg=ModernTheme.DARK['surface_light'], fg=ModernTheme.DARK['text'],
                              font=('Segoe UI', 11), relief='flat',
                              padx=30, pady=12, cursor='hand2', borderwidth=0)
        cancel_btn.pack(side=tk.LEFT, padx=5)
    
    def update_versions(self, *args):
        server_type = self.server_type.get()
        self.version_combo['values'] = self.versions.get(server_type, [])
        if self.version_combo['values']:
            self.version_combo.set(self.version_combo['values'][0])
    
    def install(self):
        server_type = self.server_type.get()
        version = self.version_combo.get()
        memory = self.memory_var.get()
        auto_start = self.auto_start.get()
        accept_eula = self.accept_eula.get()
        
        self.dialog.destroy()
        
        self.app.log(f"📦 Installing {server_type.upper()} server {version}...")
        self.app.log(f"💾 Memory: {memory}GB")
        
        def install_process():
            try:
                # Install Java
                self.app.log("☕ Installing Java 21...")
                self.app.ssh.execute("apt update -qq", timeout=120)
                self.app.ssh.execute(
                    "DEBIAN_FRONTEND=noninteractive apt install -y openjdk-21-jdk-headless wget curl",
                    timeout=600
                )
                
                self.app.log("✅ Java installed!")
                self.app.ssh.execute("mkdir -p /root/minecraft")
                
                # Install based on type
                if server_type == "fabric":
                    self.app.log(f"📥 Downloading Fabric {version}...")
                    self.app.ssh.execute(
                        f"cd /root/minecraft && wget -q -O fabric-installer.jar "
                        f"https://maven.fabricmc.net/net/fabricmc/fabric-installer/1.0.0/fabric-installer-1.0.0.jar"
                    )
                    self.app.ssh.execute(
                        f"cd /root/minecraft && java -jar fabric-installer.jar server "
                        f"-mcversion {version} -downloadMinecraft"
                    )
                    self.app.ssh.execute("cd /root/minecraft && mv fabric-server-launch.jar server.jar")
                
                elif server_type == "forge":
                    self.app.log(f"📥 Downloading Forge {version}...")
                    forge_versions = {
                        '1.21.1': '52.0.9',
                        '1.20.6': '50.1.0',
                        '1.20.4': '49.1.0',
                        '1.20.1': '47.3.0',
                        '1.19.4': '45.2.0',
                        '1.19.2': '43.4.0',
                        '1.18.2': '40.2.21',
                        '1.16.5': '36.2.39',
                        '1.12.2': '14.23.5.2860'
                    }
                    forge_ver = forge_versions.get(version, '52.0.9')
                    self.app.ssh.execute(
                        f"cd /root/minecraft && wget -q -O forge-installer.jar "
                        f"https://maven.minecraftforge.net/net/minecraftforge/forge/{version}-{forge_ver}/forge-{version}-{forge_ver}-installer.jar"
                    )
                    self.app.ssh.execute("cd /root/minecraft && java -jar forge-installer.jar --installServer")
                
                elif server_type == "paper":
                    self.app.log(f"📥 Downloading Paper {version}...")
                    self.app.ssh.execute(
                        f"cd /root/minecraft && wget -q -O server.jar "
                        f"https://api.papermc.io/v2/projects/paper/versions/{version}/builds/latest/downloads/paper-{version}-latest.jar"
                    )
                
                elif server_type == "purpur":
                    self.app.log(f"📥 Downloading Purpur {version}...")
                    self.app.ssh.execute(
                        f"cd /root/minecraft && wget -q -O server.jar "
                        f"https://api.purpurmc.org/v2/purpur/{version}/latest/download"
                    )
                
                elif server_type == "vanilla":
                    self.app.log(f"📥 Downloading Vanilla {version}...")
                    self.app.ssh.execute(
                        f"cd /root/minecraft && wget -q -O server.jar "
                        f"https://piston-data.mojang.com/v1/objects/server.jar"
                    )
                
                self.app.log("✅ Server downloaded!")
                
                # Accept EULA
                if accept_eula:
                    self.app.log("📝 Accepting EULA...")
                    self.app.ssh.execute("echo 'eula=true' > /root/minecraft/eula.txt")
                
                # Configure server
                self.app.log("⚙️ Configuring server...")
                props = f"""
max-players=20
view-distance=10
server-port=25565
online-mode=true
difficulty=normal
gamemode=survival
pvp=true
spawn-protection=16
motd=A Minecraft Server
"""
                self.app.ssh.execute(f"cat > /root/minecraft/server.properties << 'EOF'\n{props}\nEOF")
                
                self.app.log("✅ Installation complete!")
                
                # Auto start
                if auto_start:
                    self.app.log("🚀 Starting server...")
                    self.app.server.start(memory=f"{memory}G")
                    self.app.log("✅ Server started!")
                
                messagebox.showinfo("Success", 
                                  f"✅ {server_type.upper()} {version} installed!\n"
                                  f"💾 Memory: {memory}GB\n"
                                  f"{'🚀 Server is starting...' if auto_start else '▶️ Click Start to run'}")
                
                self.app.update_server_status()
                
            except Exception as e:
                self.app.log(f"❌ Installation failed: {e}")
                messagebox.showerror("Error", f"Installation failed:\n{str(e)}")
        
        threading.Thread(target=install_process, daemon=True).start()
