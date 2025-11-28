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
            ("🌍 Export World", self.export_world, 'success'),
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

    def export_world(self):
        """Export complete world with all data to local machine"""
        if not self.app.ssh:
            messagebox.showerror("Error", "Not connected to server")
            return
        
        # Ask where to save
        save_path = filedialog.askdirectory(title="Select folder to save world export")
        if not save_path:
            return
        
        def export():
            try:
                self.app.log("🌍 Starting world export...")
                self.app.log("⚠️ This may take several minutes for large worlds!")
                
                # Create timestamp for export
                import time
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                export_name = f"world_export_{timestamp}"
                
                # Create temporary archive on server
                self.app.log("📦 Creating archive on server...")
                archive_cmd = (
                    f"cd ~/minecraft && "
                    f"tar -czf /tmp/{export_name}.tar.gz "
                    f"--exclude='world*/session.lock' "  # Exclude lock files
                    f"world*/playerdata "  # Player data (inventories, positions)
                    f"world*/stats "  # Player statistics
                    f"world*/advancements "  # Player advancements
                    f"world*/data "  # World data (maps, structures)
                    f"world*/region "  # World chunks
                    f"world*/DIM-1 "  # Nether
                    f"world*/DIM1 "  # End
                    f"world*/level.dat "  # World info
                    f"world*/level.dat_old "
                    f"server.properties "
                    f"ops.json "
                    f"whitelist.json "
                    f"banned-players.json "
                    f"banned-ips.json "
                    f"usercache.json "
                    f"2>&1"
                )
                
                output, _ = self.app.ssh.execute(archive_cmd)
                self.app.log(f"Archive output: {output[:200]}")
                
                # Check archive size
                size_output, _ = self.app.ssh.execute(f"du -h /tmp/{export_name}.tar.gz")
                size = size_output.split()[0] if size_output else "Unknown"
                self.app.log(f"📊 Archive size: {size}")
                
                # Download using SFTP
                self.app.log("📥 Downloading to local machine...")
                self.app.log("⏳ Please wait, this may take a while...")
                
                import paramiko
                sftp = self.app.ssh.client.open_sftp()
                
                local_file = f"{save_path}/{export_name}.tar.gz"
                remote_file = f"/tmp/{export_name}.tar.gz"
                
                # Download with progress
                def progress_callback(transferred, total):
                    percent = (transferred / total) * 100 if total > 0 else 0
                    if int(percent) % 10 == 0:  # Log every 10%
                        self.app.log(f"📥 Downloaded: {percent:.0f}%")
                
                sftp.get(remote_file, local_file, callback=progress_callback)
                sftp.close()
                
                # Clean up server
                self.app.log("🧹 Cleaning up server...")
                self.app.ssh.execute(f"rm -f /tmp/{export_name}.tar.gz")
                
                # Extract locally
                self.app.log("📂 Extracting archive...")
                import tarfile
                with tarfile.open(local_file, 'r:gz') as tar:
                    tar.extractall(f"{save_path}/{export_name}")
                
                # Delete archive after extraction
                import os
                os.remove(local_file)
                
                self.app.log(f"✅ World exported successfully!")
                self.app.log(f"📁 Location: {save_path}/{export_name}")
                
                messagebox.showinfo("Export Complete",
                    f"World exported successfully!\n\n"
                    f"Location: {save_path}/{export_name}\n\n"
                    f"Contents:\n"
                    f"• All world chunks (region files)\n"
                    f"• Player data (inventories, positions, health)\n"
                    f"• Player stats and advancements\n"
                    f"• World data (maps, structures)\n"
                    f"• Nether and End dimensions\n"
                    f"• server.properties\n"
                    f"• Ops, whitelist, bans\n\n"
                    f"Your player 'puskevi' data is included!")
                
            except Exception as e:
                self.app.log(f"❌ Export failed: {e}")
                messagebox.showerror("Export Failed", 
                    f"Failed to export world:\n{e}\n\n"
                    f"Make sure you have enough disk space and permissions.")
        
        threading.Thread(target=export, daemon=True).start()
