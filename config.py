"""Configuration management for Minecraft Server Manager"""

class Config:
    DEFAULT_SSH_PORT = 22
    DEFAULT_MC_PORT = 25565
    DEFAULT_MC_DIR = "/root/minecraft"
    DEFAULT_MEMORY = "4G"
    
    COLORS = {
        'bg': '#1e1e1e',
        'fg': '#ffffff',
        'accent': '#007acc',
        'success': '#4ec9b0',
        'warning': '#ce9178',
        'error': '#f48771',
        'panel': '#252526',
        'input': '#3c3c3c',
        'button': '#0e639c'
    }
    
    CLIENT_ONLY_MODS = [
        'optifine', 'optifabric', 'sodium', 'iris', 'oculus',
        'lambdynamiclights', 'replaymod', 'shulkerboxtooltip',
        'inventoryhud', 'itemscroller', 'litematica', 'minihud',
        'tweakeroo', 'worldedit', 'xaeros', 'journeymap'
    ]
