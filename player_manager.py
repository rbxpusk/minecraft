"""Player management functionality"""
import json

class PlayerManager:
    def __init__(self, ssh_manager, server_dir="/root/minecraft"):
        self.ssh = ssh_manager
        self.server_dir = server_dir
    
    def get_online_players(self):
        output, _ = self.ssh.execute(
            f"cd {self.server_dir} && tail -100 logs/latest.log 2>/dev/null | "
            "grep -E 'joined the game|left the game' | tail -20"
        )
        
        players = []
        online = set()
        
        for line in output.strip().split('\n'):
            if 'joined the game' in line:
                username = line.split(']:')[1].split('joined')[0].strip()
                online.add(username)
            elif 'left the game' in line:
                username = line.split(']:')[1].split('left')[0].strip()
                online.discard(username)
        
        for username in online:
            players.append({'username': username, 'uuid': 'N/A', 'status': 'Online'})
        
        return players
    
    def op_player(self, username):
        self.ssh.execute(f"screen -S minecraft -X stuff 'op {username}^M'")
        return True
    
    def deop_player(self, username):
        self.ssh.execute(f"screen -S minecraft -X stuff 'deop {username}^M'")
        return True
    
    def kick_player(self, username, reason=''):
        cmd = f"kick {username} {reason}".strip()
        self.ssh.execute(f"screen -S minecraft -X stuff '{cmd}^M'")
        return True
    
    def ban_player(self, username, reason=''):
        cmd = f"ban {username} {reason}".strip()
        self.ssh.execute(f"screen -S minecraft -X stuff '{cmd}^M'")
        return True
    
    def unban_player(self, username):
        self.ssh.execute(f"screen -S minecraft -X stuff 'pardon {username}^M'")
        return True
    
    def get_whitelist(self):
        output, _ = self.ssh.execute(f"cat {self.server_dir}/whitelist.json 2>/dev/null || echo '[]'")
        try:
            return json.loads(output)
        except:
            return []
    
    def add_to_whitelist(self, username):
        self.ssh.execute(f"screen -S minecraft -X stuff 'whitelist add {username}^M'")
        return True
    
    def remove_from_whitelist(self, username):
        self.ssh.execute(f"screen -S minecraft -X stuff 'whitelist remove {username}^M'")
        return True
