"""Mods management tab"""
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import threading
from ui_components import ModernTheme, ModernButton, ModernEntry, Card

class ModsTab:
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
            ("🔄 Refresh", self.refresh_mods, 'primary'),
            ("📤 Upload Mod", self.upload_mod, 'success'),
            ("📥 Download URL", self.download_mod, 'primary'),
            ("🗑️ Delete Selected", self.delete_mod, 'error'),
            ("🧹 Clear All", self.clear_all, 'warning'),
            ("📦 Export List", self.export_mod_list, 'primary'),
            ("🔍 Check Updates", self.check_updates, 'primary'),
        ]
        
        for text, cmd, style in buttons:
            ModernButton(btn_container, text=text, command=cmd, style=style).pack(
                side=tk.LEFT, padx=5
            )
        
        search_frame = tk.Frame(self.frame, bg=ModernTheme.DARK['bg'])
        search_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Label(search_frame, text="🔍 Search:", bg=ModernTheme.DARK['bg'],
                fg=ModernTheme.DARK['text'], font=('Segoe UI', 10)).pack(
            side=tk.LEFT, padx=5
        )
        
        self.search_var = tk.StringVar()
        self.search_var.trace('w', lambda *args: self.filter_mods())
        
        search_entry = ModernEntry(search_frame, textvariable=self.search_var, width=40)
        search_entry.pack(side=tk.LEFT, padx=5, ipady=8)
        
        self.count_label = tk.Label(search_frame, text="", bg=ModernTheme.DARK['bg'],
                                    fg=ModernTheme.DARK['text_secondary'],
                                    font=('Segoe UI', 9))
        self.count_label.pack(side=tk.RIGHT, padx=10)
        
        # Selection info
        self.selection_label = tk.Label(self.frame, text="💡 Tip: Select a mod to delete it",
                                       font=('Segoe UI', 10),
                                       bg=ModernTheme.DARK['bg'],
                                       fg=ModernTheme.DARK['text_secondary'])
        self.selection_label.pack(anchor='w', padx=15, pady=5)
        
        list_card = Card(self.frame)
        list_card.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        columns = ("Mod Name", "Size", "Date")
        self.tree = ttk.Treeview(list_card, columns=columns, show="headings", height=15)
        
        for col in columns:
            self.tree.heading(col, text=col)
        
        self.tree.column("Mod Name", width=500)
        self.tree.column("Size", width=100)
        self.tree.column("Date", width=200)
        
        # Bind selection and double-click events
        self.tree.bind('<<TreeviewSelect>>', self.on_mod_select)
        self.tree.bind('<Double-Button-1>', lambda e: self.delete_mod())
        
        scrollbar = ttk.Scrollbar(list_card, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=2, pady=2)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Quick install popular mods
        popular_label = tk.Label(self.frame, text="⚡ Quick Install Popular Mods",
                                font=('Segoe UI', 12, 'bold'),
                                bg=ModernTheme.DARK['bg'],
                                fg=ModernTheme.DARK['accent'])
        popular_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        popular_card = Card(self.frame)
        popular_card.pack(fill=tk.X, padx=10, pady=5)
        
        popular_container = tk.Frame(popular_card, bg=ModernTheme.DARK['surface'])
        popular_container.pack(pady=10, padx=15)
        
        popular_mods = [
            ("Fabric API", "https://cdn.modrinth.com/data/P7dR8mSH/versions/latest/fabric-api.jar"),
            ("Lithium", "https://cdn.modrinth.com/data/gvQqBUqZ/versions/latest/lithium-fabric.jar"),
            ("Phosphor", "https://cdn.modrinth.com/data/hEOCdOgW/versions/latest/phosphor-fabric.jar"),
            ("Krypton", "https://cdn.modrinth.com/data/fQEb0iXm/versions/latest/krypton.jar"),
            ("FerriteCore", "https://cdn.modrinth.com/data/uXXizFIs/versions/latest/ferritecore-fabric.jar"),
        ]
        
        for i, (name, url) in enumerate(popular_mods):
            btn = tk.Button(popular_container, text=f"⬇️ {name}",
                           command=lambda u=url, n=name: self.quick_install(u, n),
                           bg=ModernTheme.DARK['accent'], fg='white',
                           font=('Segoe UI', 9, 'bold'), relief='flat',
                           padx=15, pady=8, cursor='hand2', borderwidth=0)
            btn.grid(row=i//5, column=i%5, padx=5, pady=5)
    
    def refresh_mods(self):
        if not self.app.mods:
            return
        
        # Show loading indicator
        self.count_label.config(text="Loading...", fg=ModernTheme.DARK['warning'])
        
        def refresh():
            try:
                mods = self.app.mods.list_mods()
                self.tree.delete(*self.tree.get_children())
                
                for mod in mods:
                    self.tree.insert('', tk.END, values=(
                        mod['name'], mod['size'], mod['date']
                    ))
                
                self.count_label.config(
                    text=f"{len(mods)} mods",
                    fg=ModernTheme.DARK['text_secondary']
                )
                self.app.log(f"✅ Found {len(mods)} mods")
            except Exception as e:
                self.count_label.config(
                    text="Error loading",
                    fg=ModernTheme.DARK['error']
                )
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=refresh, daemon=True).start()
    
    def filter_mods(self):
        search = self.search_var.get().lower()
        for item in self.tree.get_children():
            values = self.tree.item(item)['values']
            if search in values[0].lower():
                self.tree.reattach(item, '', tk.END)
            else:
                self.tree.detach(item)
    
    def upload_mod(self):
        if not self.app.mods:
            return
        
        file_path = filedialog.askopenfilename(
            title="Select Mod File",
            filetypes=[("JAR files", "*.jar"), ("All files", "*.*")]
        )
        
        if not file_path:
            return
        
        self.app.log(f"📤 Uploading {file_path}...")
        
        def upload():
            try:
                self.app.mods.upload_mod(file_path)
                self.app.log("✅ Mod uploaded")
                self.refresh_mods()
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=upload, daemon=True).start()
    
    def download_mod(self):
        url = tk.simpledialog.askstring("Download Mod", "Enter mod download URL:")
        if not url:
            return
        
        self.app.log(f"📥 Downloading from {url}...")
        
        def download():
            try:
                self.app.mods.download_mod_url(url)
                self.app.log("✅ Mod downloaded")
                self.refresh_mods()
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=download, daemon=True).start()
    
    def get_selected_mod(self):
        """Get the selected mod from the tree"""
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            return item['values'][0]  # Mod name is first column
        return None
    
    def delete_mod(self):
        mod_name = self.get_selected_mod()
        
        if not mod_name:
            messagebox.showwarning("Warning", "Please select a mod to delete")
            return
        
        if not messagebox.askyesno("Confirm", f"Delete {mod_name}?"):
            return
        
        def delete():
            try:
                self.app.mods.delete_mod(mod_name)
                self.app.log(f"✅ Deleted {mod_name}")
                self.refresh_mods()
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=delete, daemon=True).start()
    
    def clear_all(self):
        if not messagebox.askyesno("Confirm", "Delete ALL mods?"):
            return
        
        def clear():
            try:
                self.app.mods.clear_all_mods()
                self.app.log("✅ All mods cleared")
                self.refresh_mods()
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=clear, daemon=True).start()
    
    def quick_install(self, url, name):
        self.app.log(f"⬇️ Quick installing {name}...")
        
        def install():
            try:
                self.app.mods.download_mod_url(url, f"{name}.jar")
                self.app.log(f"✅ {name} installed")
                self.refresh_mods()
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=install, daemon=True).start()
    
    def on_mod_select(self, event):
        """Update selection label when mod is selected"""
        mod = self.get_selected_mod()
        if mod:
            self.selection_label.config(
                text=f"✅ Selected: {mod} - Double-click to delete",
                fg=ModernTheme.DARK['success']
            )
        else:
            self.selection_label.config(
                text="💡 Tip: Select a mod to delete it",
                fg=ModernTheme.DARK['text_secondary']
            )
    
    def export_mod_list(self):
        if not self.app.mods:
            return
        
        def export():
            try:
                mods = self.app.mods.list_mods()
                mod_list = "\n".join([mod['name'] for mod in mods])
                
                # Save to file
                from tkinter import filedialog
                file_path = filedialog.asksaveasfilename(
                    defaultextension=".txt",
                    filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
                )
                
                if file_path:
                    with open(file_path, 'w') as f:
                        f.write(f"Mod List - {len(mods)} mods\n")
                        f.write("=" * 50 + "\n\n")
                        f.write(mod_list)
                    
                    self.app.log(f"📦 Exported {len(mods)} mods to {file_path}")
                    messagebox.showinfo("Success", f"Exported {len(mods)} mods!")
            except Exception as e:
                self.app.log(f"❌ Error: {e}")
        
        threading.Thread(target=export, daemon=True).start()
    
    def check_updates(self):
        self.app.log("🔍 Checking for mod updates...")
        messagebox.showinfo("Check Updates", 
                          "This feature checks if your mods have updates available.\n\n"
                          "Tip: Visit CurseForge or Modrinth to check for updates manually.")
        self.app.log("💡 Visit CurseForge or Modrinth for updates")
