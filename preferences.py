"""User preferences and credential storage"""
import json
import os
from pathlib import Path
import base64

class Preferences:
    def __init__(self):
        self.config_dir = Path.home() / '.minecraft_server_manager'
        self.config_file = self.config_dir / 'config.json'
        self.credentials_file = self.config_dir / 'credentials.json'
        
        self.config_dir.mkdir(exist_ok=True)
        
        self.prefs = self.load_preferences()
        self.credentials = self.load_credentials()
    
    def load_preferences(self):
        """Load user preferences"""
        defaults = {
            'auto_connect': False,
            'remember_credentials': False,
            'last_server': None,
            'theme': 'dark',
            'auto_refresh': False,
            'auto_fetch': True,
            'refresh_interval': 5,
            'show_tutorial': True,
            'console_lines': 100,
            'default_memory': '4G',
            'local_mods_path': '',
            'backup_path': '',
            'window_size': '1600x900',
            'font_size': 10
        }
        
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    saved = json.load(f)
                    defaults.update(saved)
            except:
                pass
        
        return defaults
    
    def save_preferences(self):
        """Save user preferences"""
        try:
            with open(self.config_file, 'w') as f:
                json.dump(self.prefs, f, indent=2)
        except Exception as e:
            print(f"Error saving preferences: {e}")
    
    def load_credentials(self):
        """Load saved credentials"""
        if not self.credentials_file.exists():
            return {}
        
        try:
            with open(self.credentials_file, 'r') as f:
                data = json.load(f)
                # Decode passwords
                for server_key, server in list(data.items()):
                    if 'password' in server:
                        try:
                            # Try to decode password
                            server['password'] = base64.b64decode(
                                server['password'].encode()
                            ).decode()
                        except Exception:
                            # If decoding fails, remove this server
                            del data[server_key]
                return data
        except Exception:
            return {}
    
    def save_credentials(self, hostname, username, password, port=22):
        """Save server credentials"""
        if not self.prefs.get('remember_credentials'):
            return
        
        # Encode password
        encoded_password = base64.b64encode(password.encode()).decode()
        
        self.credentials[hostname] = {
            'hostname': hostname,
            'username': username,
            'password': encoded_password,
            'port': port
        }
        
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump(self.credentials, f, indent=2)
        except Exception as e:
            print(f"Error saving credentials: {e}")
    
    def get_last_server(self):
        """Get last connected server credentials"""
        last = self.prefs.get('last_server')
        if last and last in self.credentials:
            try:
                creds = self.credentials[last].copy()
                # Decode password if it's still encoded
                if 'password' in creds:
                    try:
                        # Check if it's already decoded (from load_credentials)
                        # If it's encoded, it will be base64
                        test = base64.b64decode(creds['password'].encode())
                        creds['password'] = test.decode()
                    except Exception:
                        # Already decoded or invalid, use as-is
                        pass
                return creds
            except Exception:
                return None
        return None
    
    def set_last_server(self, hostname):
        """Set last connected server"""
        self.prefs['last_server'] = hostname
        self.save_preferences()
    
    def delete_credentials(self, hostname):
        """Delete saved credentials"""
        if hostname in self.credentials:
            del self.credentials[hostname]
            try:
                with open(self.credentials_file, 'w') as f:
                    json.dump(self.credentials, f, indent=2)
            except:
                pass
    
    def get_all_servers(self):
        """Get list of all saved servers"""
        return list(self.credentials.keys())
    
    def get(self, key, default=None):
        """Get preference value"""
        return self.prefs.get(key, default)
    
    def set(self, key, value):
        """Set preference value"""
        self.prefs[key] = value
        self.save_preferences()
    
    def clear_all_credentials(self):
        """Clear all saved credentials"""
        self.credentials = {}
        try:
            if self.credentials_file.exists():
                self.credentials_file.unlink()
            # Also clear last server
            self.prefs['last_server'] = None
            self.save_preferences()
        except Exception as e:
            print(f"Error clearing credentials: {e}")
    
    def clear_all(self):
        """Clear all preferences and credentials"""
        self.prefs = {}
        self.clear_all_credentials()
        self.credentials = {}
        
        try:
            if self.config_file.exists():
                self.config_file.unlink()
            if self.credentials_file.exists():
                self.credentials_file.unlink()
        except:
            pass
