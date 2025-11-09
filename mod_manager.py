"""Mod management functionality"""
import os
import zipfile
from pathlib import Path

class ModManager:
    def __init__(self, ssh_manager, server_dir="/root/minecraft"):
        self.ssh = ssh_manager
        self.server_dir = server_dir
        self.mods_dir = f"{server_dir}/mods"
    
    def list_mods(self):
        output, _ = self.ssh.execute(f"ls -lh {self.mods_dir}/*.jar 2>/dev/null || echo ''")
        mods = []
        
        for line in output.strip().split('\n'):
            if line and '.jar' in line:
                parts = line.split()
                if len(parts) >= 9:
                    size = parts[4]
                    name = parts[8].split('/')[-1]
                    date = f"{parts[5]} {parts[6]} {parts[7]}"
                    mods.append({'name': name, 'size': size, 'date': date})
        
        return mods
    
    def upload_mod(self, local_path):
        sftp = self.ssh.get_sftp()
        remote_path = f"{self.mods_dir}/{os.path.basename(local_path)}"
        sftp.put(local_path, remote_path)
        sftp.close()
        return True
    
    def delete_mod(self, mod_name):
        self.ssh.execute(f"rm -f {self.mods_dir}/{mod_name}")
        return True
    
    def download_mod_url(self, url, filename=None):
        if not filename:
            filename = url.split('/')[-1]
        
        self.ssh.execute(f"cd {self.mods_dir} && wget -q '{url}' -O '{filename}'")
        return True
    
    def clear_all_mods(self):
        self.ssh.execute(f"rm -rf {self.mods_dir}/*.jar")
        return True
    
    def find_duplicates(self):
        mods = self.list_mods()
        seen = {}
        duplicates = []
        
        for mod in mods:
            base_name = mod['name'].rsplit('-', 1)[0].lower()
            if base_name in seen:
                duplicates.append((seen[base_name], mod['name']))
            else:
                seen[base_name] = mod['name']
        
        return duplicates
    
    def install_modpack(self, zip_path):
        self.ssh.execute(f"mkdir -p {self.mods_dir}")
        
        sftp = self.ssh.get_sftp()
        remote_zip = f"/tmp/modpack.zip"
        sftp.put(zip_path, remote_zip)
        sftp.close()
        
        self.ssh.execute(f"unzip -o {remote_zip} -d {self.server_dir}")
        self.ssh.execute(f"rm {remote_zip}")
        
        return True
