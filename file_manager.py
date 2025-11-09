"""File and backup management"""
import os
from datetime import datetime

class FileManager:
    def __init__(self, ssh_manager, server_dir="/root/minecraft"):
        self.ssh = ssh_manager
        self.server_dir = server_dir
    
    def list_directory(self, path=None):
        if path is None:
            path = self.server_dir
        
        output, _ = self.ssh.execute(f"ls -lh {path} 2>/dev/null || echo ''")
        files = []
        
        for line in output.strip().split('\n')[1:]:
            if line:
                parts = line.split()
                if len(parts) >= 9:
                    files.append({
                        'name': parts[8],
                        'size': parts[4],
                        'date': f"{parts[5]} {parts[6]}",
                        'type': 'dir' if parts[0].startswith('d') else 'file'
                    })
        
        return files
    
    def get_logs(self, lines=100):
        output, _ = self.ssh.execute(
            f"tail -{lines} {self.server_dir}/logs/latest.log 2>/dev/null || echo 'No logs found'"
        )
        return output
    
    def clear_logs(self):
        self.ssh.execute(f"rm -rf {self.server_dir}/logs/*.log.gz")
        self.ssh.execute(f"echo '' > {self.server_dir}/logs/latest.log")
        return True
    
    def backup_world(self, world_name='world'):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f"backup_{world_name}_{timestamp}.tar.gz"
        backup_path = f"/root/backups/{backup_name}"
        
        self.ssh.execute("mkdir -p /root/backups")
        self.ssh.execute(
            f"cd {self.server_dir} && tar -czf {backup_path} {world_name}/ 2>/dev/null"
        )
        
        return backup_name
    
    def list_backups(self):
        output, _ = self.ssh.execute("ls -lh /root/backups/*.tar.gz 2>/dev/null || echo ''")
        backups = []
        
        for line in output.strip().split('\n'):
            if line and '.tar.gz' in line:
                parts = line.split()
                if len(parts) >= 9:
                    backups.append({
                        'name': parts[8].split('/')[-1],
                        'size': parts[4],
                        'date': f"{parts[5]} {parts[6]} {parts[7]}"
                    })
        
        return backups
    
    def restore_backup(self, backup_name):
        self.ssh.execute(
            f"cd {self.server_dir} && tar -xzf /root/backups/{backup_name}"
        )
        return True
    
    def download_file(self, remote_path, local_path):
        sftp = self.ssh.get_sftp()
        sftp.get(remote_path, local_path)
        sftp.close()
        return True
    
    def upload_file(self, local_path, remote_path):
        sftp = self.ssh.get_sftp()
        sftp.put(local_path, remote_path)
        sftp.close()
        return True
