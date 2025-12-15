# Professional UI Styles and Themes
import tkinter as tk
from tkinter import ttk

class ModernStyle:
    # Color Palette
    PRIMARY = "#3498DB"      # Blue
    SECONDARY = "#A23B72"    # Purple
    SUCCESS = "#F18F01"      # Orange
    DANGER = "#C73E1D"       # Red
    LIGHT = "#F5F5F5"        # Light Gray
    DARK = "#34495E"         # Dark Blue
    WHITE = "#FFFFFF"
    GRAY = "#BDC3C7"
    
    @staticmethod
    def configure_styles():
        style = ttk.Style()
        
        # Configure modern button styles
        style.configure("Primary.TButton",
                       background="#FFFFFF",  # White background
                       foreground="#000000",   # Black text
                       borderwidth=3,
                       relief="raised",
                       focuscolor="none",
                       padding=(20, 10),
                       font=("Segoe UI", 12, "bold"))
        
        style.configure("Success.TButton",
                       background="#FFFFFF",  # White background
                       foreground="#000000",   # Black text
                       borderwidth=3,
                       relief="raised",
                       focuscolor="none",
                       padding=(15, 8),
                       font=("Segoe UI", 12, "bold"))
        
        style.configure("Danger.TButton",
                       background="#FFFFFF",  # White background
                       foreground="#000000",   # Black text
                       borderwidth=3,
                       relief="raised",
                       focuscolor="none",
                       padding=(15, 8),
                       font=("Segoe UI", 12, "bold"))
        
        # Configure frame styles
        style.configure("Card.TFrame",
                       background=ModernStyle.WHITE,
                       relief="solid",
                       borderwidth=1)
        
        style.configure("Sidebar.TFrame",
                       background="#F8F9FA")  # Light background for sidebar
        
        # Configure label styles
        style.configure("Title.TLabel",
                       background=ModernStyle.WHITE,
                       foreground=ModernStyle.DARK,
                       font=("Segoe UI", 24, "bold"))
        
        style.configure("Heading.TLabel",
                       background=ModernStyle.WHITE,
                       foreground=ModernStyle.DARK,
                       font=("Segoe UI", 16, "bold"))
        
        style.configure("Sidebar.TLabel",
                       background="#F8F9FA",
                       foreground="#2C3E50",
                       font=("Segoe UI", 12))
        
        # Configure sidebar button styles with dark text
        style.configure("Sidebar.TButton",
                       background="#FFFFFF",  # White background
                       foreground="#000000",   # Black text
                       borderwidth=3,
                       relief="raised",
                       focuscolor="none",
                       padding=(15, 12),
                       font=("Segoe UI", 14, "bold"))
        
        style.map("Sidebar.TButton",
                 background=[("active", "#BDC3C7"),    # Darker gray on hover
                           ("pressed", "#95A5A6")],   # Even darker on press
                 foreground=[("active", "#2C3E50"),    # Keep dark text
                           ("pressed", "#2C3E50")],
                 relief=[("pressed", "sunken")])
        
        # Configure entry styles
        style.configure("Modern.TEntry",
                       fieldbackground=ModernStyle.WHITE,
                       borderwidth=2,
                       relief="solid",
                       padding=(10, 8))
        
        # Configure treeview
        style.configure("Modern.Treeview",
                       background=ModernStyle.WHITE,
                       foreground=ModernStyle.DARK,
                       rowheight=30,
                       fieldbackground=ModernStyle.WHITE)
        
        style.configure("Modern.Treeview.Heading",
                       background=ModernStyle.PRIMARY,
                       foreground=ModernStyle.WHITE,
                       font=("Segoe UI", 10, "bold"))

def create_card_frame(parent, **kwargs):
    """Create a modern card-style frame"""
    frame = ttk.Frame(parent, style="Card.TFrame", **kwargs)
    frame.configure(padding=(20, 15))
    return frame

def create_icon_button(parent, text, command, style="Primary.TButton", **kwargs):
    """Create a modern button with consistent styling"""
    return ttk.Button(parent, text=text, command=command, style=style, **kwargs)