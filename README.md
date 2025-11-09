# Minecraft Server Manager

Manage your Minecraft server without SSH commands. Control your server and install new ones directly to your VPS.

## Features

**Server stuff:**
- Start, stop, restart your server
- Watch the console in real-time
- Send commands without typing `/`
- See CPU, RAM, and player count
- Install any server type (Fabric, Forge, Vanilla, Paper, Purpur)

**Mod management:**
- Upload mods from your computer
- Download mods from URLs
- One-click install popular mods
- Search and filter your mods
- Delete mods 
- Export your mod list

**Player management:**
- See who's online
- Op/deop players
- Kick or ban troublemakers
- Send private messages
- Change gamemodes
- Manage whitelist
- Just click a player and hit any button - no typing names!

**Admin commands:**
- 20+ quick command buttons
- Change time and weather
- Teleport players
- Give items and XP
- Set world borders
- Kill all mobs
- And more...

**File management:**
- Browse server files
- View and clear logs
- Create world backups
- Restore from backups

## Getting started

1. **Install Python** (3.8 or newer)

2. **Download this:**
```bash
git clone https://github.com/rbxpusk/minecraft-server-manager.git
cd minecraft-server-manager
pip install -r requirements.txt
```

3. **Run it:**
```bash
python main.py
```

4. **Connect to your server:**
   - Enter your server's IP
   - Port (usually 22)
   - Username (usually root)
   - Password
   - Hit Connect

5. Done. The tutorial will guide you through the rest.

## Key Features

- **Saved credentials** - Auto-connect on startup
- **Smart selection** - Click once, use anywhere
- **Double-click actions** - Quick delete and menus
- **Auto-refresh** - Live log updates
- **Quick commands** - 20+ admin buttons
- **Performance stats** - CPU, RAM, uptime monitoring
- **Preferences** - Customize paths, memory, intervals
- **Tutorial** - Built-in guide for first-time users

## Requirements

- Python 3.8+
- A VPS with SSH access
- That's it!

## Security

**Important:**
- Never commit credentials to git
- Credentials are stored in `~/.minecraft_server_manager/` (excluded from git)
- Passwords are base64 encoded (not plaintext, but not true encryption)
- For production, use SSH keys instead of passwords
- Keep your VPS updated and secure

## Tips

- Use Fabric for modded servers (faster than Forge)
- Start with 4GB RAM, increase if needed
- Backup before major changes
- Check mod version compatibility
- Install Fabric API first for Fabric mods
- Use whitelist for private servers

## Project structure

```
main.py              - Start here
config.py            - Settings
ssh_manager.py       - Handles SSH
server_manager.py    - Server controls
mod_manager.py       - Mod operations
player_manager.py    - Player management
file_manager.py      - File operations
ui_components.py     - UI theme
tabs/                - All the tabs
dialogs/             - Popup windows
```

## Contributing

Found a bug? Want a feature? Open an issue or send a PR. All contributions welcome!

## License

MIT - do whatever you want with it.

## Credits

Built with Python and Tkinter. Uses Paramiko for SSH. Made for the Minecraft community.

## Support

- Help button in app
- Built-in tutorial
- GitHub issues

---

Made by pusk
