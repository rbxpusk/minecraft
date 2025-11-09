"""SSH connection and command execution"""
import paramiko
import time

class SSHManager:
    def __init__(self, hostname, username, password, port=22):
        self.hostname = hostname
        self.username = username
        self.password = password
        self.port = port
        self.client = None
    
    def connect(self):
        self.client = paramiko.SSHClient()
        self.client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.client.connect(
            self.hostname,
            port=self.port,
            username=self.username,
            password=self.password,
            timeout=10
        )
        return True
    
    def disconnect(self):
        if self.client:
            self.client.close()
            self.client = None
    
    def execute(self, command, timeout=30):
        if not self.client:
            raise Exception("Not connected")
        
        stdin, stdout, stderr = self.client.exec_command(command, timeout=timeout)
        output = stdout.read().decode('utf-8', errors='ignore')
        error = stderr.read().decode('utf-8', errors='ignore')
        return output, error
    
    def get_sftp(self):
        if not self.client:
            raise Exception("Not connected")
        return self.client.open_sftp()
