import tkinter as tk
from PIL import Image, ImageTk, ImageDraw, ImageFilter
import io

def create_gradient_background(width=1200, height=800):
    """Create a beautiful gradient background"""
    # Create gradient image
    img = Image.new('RGB', (width, height), '#E6F3FF')
    draw = ImageDraw.Draw(img)
    
    # Create diagonal gradient effect
    for i in range(height):
        for j in range(width):
            # Calculate color based on position
            ratio_y = i / height
            ratio_x = j / width
            
            # Blend colors diagonally
            r = int(230 + (255 - 230) * ratio_y * 0.5 + (240 - 230) * ratio_x * 0.3)
            g = int(243 + (255 - 243) * ratio_y * 0.7 + (248 - 243) * ratio_x * 0.2)
            b = int(255)
            
            if i % 4 == 0 and j % 4 == 0:  # Sample every 4th pixel for performance
                color = (min(255, r), min(255, g), b)
                draw.rectangle([j, i, j+4, i+4], fill=color)
    
    # Add money symbols as watermark
    watermark_color = (200, 220, 240, 80)
    for x in range(100, width-100, 200):
        for y in range(100, height-100, 150):
            # Draw rupee symbol
            draw.text((x, y), "₹", fill=watermark_color)
            draw.text((x+50, y+30), "💰", fill=watermark_color)
    
    return img

def create_financial_pattern(width=1200, height=800):
    """Create a financial themed background pattern"""
    img = Image.new('RGBA', (width, height), (245, 250, 255, 255))
    draw = ImageDraw.Draw(img)
    
    # Add subtle grid pattern
    grid_color = (200, 220, 240, 30)
    for x in range(0, width, 40):
        draw.line([(x, 0), (x, height)], fill=grid_color, width=1)
    for y in range(0, height, 40):
        draw.line([(0, y), (width, y)], fill=grid_color, width=1)
    
    # Add some financial symbols as watermark
    symbol_color = (180, 200, 230, 20)
    
    # Draw rupee symbols
    for i in range(5):
        for j in range(3):
            x = 200 + i * 200
            y = 150 + j * 200
            # Simple rupee symbol representation
            draw.text((x, y), "₹", fill=symbol_color, font=None)
    
    # Add chart-like elements
    for i in range(3):
        x_start = 100 + i * 300
        y_start = 400
        # Draw simple bar chart pattern
        for bar in range(5):
            bar_x = x_start + bar * 20
            bar_height = 20 + (bar * 10)
            draw.rectangle([bar_x, y_start - bar_height, bar_x + 15, y_start], 
                         fill=(150, 180, 220, 15))
    
    return img

def set_background_image(window, image_type="gradient"):
    """Set background image for a tkinter window"""
    try:
        # Get window size
        window.update_idletasks()
        width = window.winfo_width() or 1200
        height = window.winfo_height() or 800
        
        if image_type == "gradient":
            bg_image = create_gradient_background(width, height)
        else:
            bg_image = create_financial_pattern(width, height)
        
        # Convert PIL image to PhotoImage
        photo = ImageTk.PhotoImage(bg_image)
        
        # Create canvas for background
        canvas = tk.Canvas(window, width=width, height=height, highlightthickness=0)
        canvas.place(x=0, y=0, relwidth=1, relheight=1)
        canvas.create_image(0, 0, anchor="nw", image=photo)
        canvas.image = photo  # Keep a reference
        
        # Send canvas to back
        canvas.lower()
        
        return canvas
        
    except Exception as e:
        print(f"Could not set background: {e}")
        # Fallback to solid color
        window.configure(bg="#E6F3FF")
        return None