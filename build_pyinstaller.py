#!/usr/bin/env python3
"""
PyInstaller build script for SMV-Extracter
More reliable than Nuitka for complex applications
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def build_with_pyinstaller():
    """Build the application with PyInstaller"""
    system = platform.system().lower()
    arch = "x64" if platform.machine().lower() in ["x86_64", "amd64"] else "x86"
    
    print(f"Building SMV-Extracter with PyInstaller for {system}-{arch}")
    
    
    venv_python = None
    possible_paths = [
        Path(".venv/Scripts/python.exe"),      
        Path("src/.venv/Scripts/python.exe"),  
        Path("venv/Scripts/python.exe"),       
        Path(".venv/bin/python"),              
        Path("src/.venv/bin/python"),          
        Path("venv/bin/python")                
    ]
    
    
    current_python = sys.executable
    if "venv" in current_python.lower():
        venv_python = current_python
        print(f"Using current uv environment Python: {venv_python}")
    else:
        for path in possible_paths:
            if path.exists():
                venv_python = str(path.absolute())
                print(f"Found uv virtual environment Python: {venv_python}")
                break
    
    
    sv_ttk_data = None
    if venv_python:
        try:
            
            result = subprocess.run([venv_python, "-c", "import sv_ttk; print(sv_ttk.__file__)"], 
                                  capture_output=True, text=True, check=True)
            sv_ttk_file = result.stdout.strip()
            sv_ttk_path = Path(sv_ttk_file).parent
            sv_ttk_data = f"{sv_ttk_path};sv_ttk"
            print(f"Found sv_ttk at: {sv_ttk_path}")
        except subprocess.CalledProcessError:
            print("Warning: sv_ttk not found in virtual environment")
    else:
        try:
            import sv_ttk
            sv_ttk_path = Path(sv_ttk.__file__).parent
            sv_ttk_data = f"{sv_ttk_path};sv_ttk"
            print(f"Found sv_ttk at: {sv_ttk_path}")
        except ImportError:
            print("Warning: sv_ttk not found, adding as hidden import only")
    
    
    try:
        
        if venv_python:
            print(f"Using detected uv environment Python: {venv_python}")
            
            
            print("Installing PyInstaller in uv environment...")
            subprocess.run(["uv", "pip", "install", "pyinstaller"], check=True)
            
            python_exe = venv_python
            print(f"Using uv environment Python: {python_exe}")
        else:
            raise FileNotFoundError("No virtual environment found")
        
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        print(f"uv environment not found or failed: {e}")
        
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        python_exe = sys.executable
        print(f"Using system Python: {python_exe}")
    
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--onefile", 
        "--windowed",  
        "--name", f"SMV-Extracter-{system}-{arch}",
        "--distpath", "dist",
        "--workpath", "build",
        "--specpath", ".",
        "--additional-hooks-dir", "hooks",  
        "--add-data", "src;src",  
        "--hidden-import", "customtkinter",
        "--hidden-import", "yt_dlp",
        "--hidden-import", "moviepy",
        "--hidden-import", "numpy",
        "--hidden-import", "PIL",
        "--hidden-import", "ffmpeg",
        "--hidden-import", "requests",
        "--hidden-import", "sv_ttk",
        "--hidden-import", "sv_ttk.themes",
        "--hidden-import", "sv_ttk.constants",
        "--hidden-import", "sv_ttk.loader",
        "--collect-all", "customtkinter",
        "--collect-all", "yt_dlp",
        "--collect-all", "sv_ttk",
        "--collect-data", "sv_ttk",
        "--collect-submodules", "sv_ttk",
        "main.py"
    ]
    
    
    if sv_ttk_data:
        cmd.insert(-1, "--add-data")
        cmd.insert(-1, sv_ttk_data)
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True)
        print("PyInstaller build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"PyInstaller build failed with exit code {e.returncode}")
        return False

def create_installer():
    """Create installer script - Not needed for single file executable"""
    print("Skipping installer creation for single file executable")
    return True

def create_zip_archive():
    """Create ZIP archive - Not needed for single file executable"""
    print("Skipping ZIP creation for single file executable")
    return True

if __name__ == "__main__":
    
    print("Building with PyInstaller using uv virtual environment...")
    print("Expected workflow:")
    print("1. pip install uv")
    print("2. uv venv")
    print("3. Activate virtual environment")
    print("4. uv pip install -r requirements.txt")
    print("5. python build_pyinstaller.py")
    print()
    
    if build_with_pyinstaller():
        create_installer()
        create_zip_archive()
        print("Build process completed!")
    else:
        sys.exit(1)
