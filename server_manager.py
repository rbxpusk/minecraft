"""Minecraft server operations"""
import time
import re

class ServerManager:
    def __init__(self, ssh_manager, minecraft_dir="/root/minecraft"):
        self.ssh = ssh_manager
        self.mc_dir = minecraft_dir
    
    def start(self, memory="4G"):
        self.ssh.execute(f"cd {self.mc_dir} && screen -dmS minecraft bash -c 'java -Xmx{memory} -Xms2G -jar server.jar nogui'")
        time.sleep(3)
        return self.get_status()
    
    def stop(self):
        output, _ = self.ssh.execute("screen -ls | grep minecraft | awk '{print $1}'")
        if output.strip():
            sessions = output.strip().split('\n')
            for session in sessions:
                if session.strip():
                    self.ssh.execute(f"screen -S {session} -X stuff 'stop^M'")
            time.sleep(5)
            for session in sessions:
                if session.strip():
                    self.ssh.execute(f"screen -S {session} -X quit 2>/dev/null || true")
        
        self.ssh.execute("pkill -f 'java.*server.jar' 2>/dev/null || true")
        return True
    
    def restart(self):
        self.stop()
        time.sleep(5)
        return self.start()
    
    def get_status(self):
        output, _ = self.ssh.execute("ps aux | grep 'java.*server.jar' | grep -v grep")
        
        if output.strip():
            server_type = "Forge" if "forge" in output.lower() else "Vanilla"
            if "fabric" in output.lower():
                server_type = "Fabric"
            return {"running": True, "type": server_type}
        
        forge_check, _ = self.ssh.execute(f"ls {self.mc_dir}/server.jar 2>&1")
        installed = "server.jar" in forge_check
        
        return {"running": False, "installed": installed}
    
    def send_command(self, command):
        self.ssh.execute(f"screen -S minecraft -X stuff '{command}^M'")
        return True
    
    def get_logs(self, lines=50):
        output, _ = self.ssh.execute(f"cd {self.mc_dir} && tail -{lines} logs/latest.log 2>/dev/null || echo 'No logs'")
        return output
    
    def cleanup_screens(self):
        output, _ = self.ssh.execute("screen -ls | grep minecraft | awk '{print $1}'")
        if output.strip():
            sessions = output.strip().split('\n')
            for session in sessions:
                if session.strip():
                    self.ssh.execute(f"screen -S {session} -X quit 2>/dev/null || true")
            self.ssh.execute("pkill -f 'java.*server.jar' 2>/dev/null || true")
            return len(sessions)
        return 0
