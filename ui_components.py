"""Modern UI components and styling"""
import tkinter as tk
from tkinter import ttk

class ModernTheme:
    DARK = {
        'bg': '#0d1117',
        'surface': '#161b22',
        'surface_light': '#21262d',
        'border': '#30363d',
        'text': '#c9d1d9',
        'text_secondary': '#8b949e',
        'accent': '#58a6ff',
        'accent_hover': '#79c0ff',
        'success': '#3fb950',
        'warning': '#d29922',
        'error': '#f85149',
        'info': '#1f6feb'
    }
    
    @staticmethod
    def apply_style():
        style = ttk.Style()
        style.theme_use('clam')
        
        theme = ModernTheme.DARK
        
        style.configure('TFrame', background=theme['bg'])
        style.configure('Surface.TFrame', background=theme['surface'])
        
        style.configure('TLabel', background=theme['bg'], foreground=theme['text'], 
                       font=('Segoe UI', 10))
        style.configure('Title.TLabel', font=('Segoe UI', 16, 'bold'), 
                       foreground=theme['accent'])
        style.configure('Subtitle.TLabel', font=('Segoe UI', 12, 'bold'))
        
        style.configure('TButton', background=theme['accent'], foreground='white',
                       borderwidth=0, focuscolor='none', padding=(15, 8),
                       font=('Segoe UI', 10, 'bold'))
        style.map('TButton', background=[('active', theme['accent_hover'])])
        
        style.configure('Success.TButton', background=theme['success'])
        style.configure('Warning.TButton', background=theme['warning'])
        style.configure('Error.TButton', background=theme['error'])
        
        style.configure('TNotebook', background=theme['bg'], borderwidth=0)
        style.configure('TNotebook.Tab', background=theme['surface'], 
                       foreground=theme['text'], padding=(20, 10), borderwidth=0)
        style.map('TNotebook.Tab', 
                 background=[('selected', theme['accent'])],
                 foreground=[('selected', 'white')])
        
        style.configure('Treeview', background=theme['surface'], 
                       foreground=theme['text'], fieldbackground=theme['surface'],
                       borderwidth=0, font=('Segoe UI', 9))
        style.configure('Treeview.Heading', background=theme['surface_light'],
                       foreground=theme['text'], borderwidth=0, 
                       font=('Segoe UI', 10, 'bold'))
        style.map('Treeview', background=[('selected', theme['accent'])])

class ModernButton(tk.Button):
    def __init__(self, parent, text, command=None, style='primary', **kwargs):
        theme = ModernTheme.DARK
        
        colors = {
            'primary': (theme['accent'], 'white'),
            'success': (theme['success'], 'white'),
            'warning': (theme['warning'], 'black'),
            'error': (theme['error'], 'white'),
            'secondary': (theme['surface_light'], theme['text'])
        }
        
        bg, fg = colors.get(style, colors['primary'])
        
        super().__init__(
            parent, text=text, command=command,
            bg=bg, fg=fg, activebackground=bg, activeforeground=fg,
            relief='flat', borderwidth=0, cursor='hand2',
            font=('Segoe UI', 10, 'bold'), padx=20, pady=10,
            **kwargs
        )
        
        self.bind('<Enter>', lambda e: self.config(bg=self._lighten_color(bg)))
        self.bind('<Leave>', lambda e: self.config(bg=bg))
    
    def _lighten_color(self, color):
        return color

class ModernEntry(tk.Entry):
    def __init__(self, parent, placeholder='', **kwargs):
        theme = ModernTheme.DARK
        super().__init__(
            parent, bg=theme['surface_light'], fg=theme['text'],
            relief='flat', borderwidth=0, insertbackground=theme['text'],
            font=('Segoe UI', 10), **kwargs
        )
        self.config(highlightthickness=1, highlightbackground=theme['border'],
                   highlightcolor=theme['accent'])

class Card(tk.Frame):
    def __init__(self, parent, **kwargs):
        theme = ModernTheme.DARK
        super().__init__(parent, bg=theme['surface'], relief='flat', **kwargs)
        self.config(highlightthickness=1, highlightbackground=theme['border'])
