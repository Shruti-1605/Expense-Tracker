"""
Build script to create executable using PyInstaller
Run this script to package the expense tracker into a standalone executable
"""

import os
import subprocess
import sys

def build_executable():
    """Build the executable using PyInstaller"""
    
    # PyInstaller command
    cmd = [
        'pyinstaller',
        '--onefile',                    # Create a single executable file
        '--windowed',                   # Don't show console window (for GUI apps)
        '--name=ExpenseTracker',        # Name of the executable
        '--icon=assets/icon.ico',       # App icon (if available)
        '--add-data=data;data',         # Include data folder
        '--hidden-import=tkinter',      # Ensure tkinter is included
        '--hidden-import=matplotlib',   # Ensure matplotlib is included
        '--hidden-import=PIL',          # Ensure Pillow is included
        'app.py'                        # Main application file
    ]
    
    print("Building executable...")
    print("Command:", ' '.join(cmd))
    
    try:
        # Run PyInstaller
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("Build successful!")
        print("Executable created in 'dist' folder")
        
        # Show build output
        if result.stdout:
            print("\nBuild output:")
            print(result.stdout)
            
    except subprocess.CalledProcessError as e:
        print("Build failed!")
        print("Error:", e.stderr)
        return False
    
    except FileNotFoundError:
        print("PyInstaller not found. Please install it first:")
        print("pip install pyinstaller")
        return False
    
    return True

def install_pyinstaller():
    """Install PyInstaller if not already installed"""
    try:
        import PyInstaller
        print("PyInstaller is already installed")
        return True
    except ImportError:
        print("Installing PyInstaller...")
        try:
            subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'pyinstaller'])
            print("PyInstaller installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("Failed to install PyInstaller")
            return False

if __name__ == "__main__":
    print("=== Expense Tracker Build Script ===")
    
    # Check if we're in the right directory
    if not os.path.exists('app.py'):
        print("Error: app.py not found. Please run this script from the project root directory.")
        sys.exit(1)
    
    # Install PyInstaller if needed
    if not install_pyinstaller():
        sys.exit(1)
    
    # Build the executable
    if build_executable():
        print("\n=== Build Complete ===")
        print("Your executable is ready in the 'dist' folder!")
        print("You can distribute the ExpenseTracker.exe file to users.")
    else:
        print("\n=== Build Failed ===")
        sys.exit(1)