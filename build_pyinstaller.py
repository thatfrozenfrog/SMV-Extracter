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
    
    # Get sv_ttk package path for manual data inclusion
    try:
        import sv_ttk
        sv_ttk_path = Path(sv_ttk.__file__).parent
        sv_ttk_data = f"{sv_ttk_path};sv_ttk"
        print(f"Found sv_ttk at: {sv_ttk_path}")
    except ImportError:
        print("Warning: sv_ttk not found, adding as hidden import only")
        sv_ttk_data = None
    
    # Try to use uv's Python executable, but fall back to direct installation
    try:
        # Check if we're in a uv environment
        result = subprocess.run(["uv", "--version"], capture_output=True, text=True, check=True)
        print(f"Found uv: {result.stdout.strip()}")
        
        # Install PyInstaller using uv pip
        print("Installing PyInstaller using uv...")
        subprocess.run(["uv", "pip", "install", "pyinstaller"], check=True)
        
        # Use the system Python but with uv-managed packages
        python_exe = sys.executable
        print(f"Using Python executable: {python_exe}")
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        # Fallback to pip if uv fails
        print("uv not available or failed, using pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        python_exe = sys.executable
        print(f"Using Python executable: {python_exe}")
    
    cmd = [
        python_exe, "-m", "PyInstaller",
        "--onedir",  
        "--windowed",  
        "--name", f"SMV-Extracter-{system}-{arch}",
        "--distpath", "dist",
        "--workpath", "build",
        "--specpath", ".",
        "--additional-hooks-dir", "hooks",  # Use custom hooks
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
        "--collect-all", "customtkinter",
        "--collect-all", "yt_dlp",
        "--collect-all", "sv_ttk",
        "--collect-data", "sv_ttk",
        "--collect-submodules", "sv_ttk",
        "main.py"
    ]
    
    # Add sv_ttk data manually if found
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
    """Create installer script"""
    system = platform.system().lower()
    dist_dir = Path("dist")
    
    if system == "windows":
        installer_content = '''@echo off
echo Installing SMV-Extracter...
mkdir "%USERPROFILE%\\SMV-Extracter" 2>nul
xcopy /E /Y "SMV-Extracter-windows-x64\\*" "%USERPROFILE%\\SMV-Extracter\\"
echo.
echo SMV-Extracter installed to %USERPROFILE%\\SMV-Extracter
echo You can create a desktop shortcut to the executable.
pause
'''
        installer_path = dist_dir / "install.bat"
    
    installer_path.write_text(installer_content)
    print(f"Created installer: {installer_path}")

def create_zip_archive():
    """Create ZIP archive using fast .NET compression"""
    system = platform.system().lower()
    arch = "x64" if platform.machine().lower() in ["x86_64", "amd64"] else "x86"
    
    if system == "windows":
        
        powershell_script = f'''
Add-Type -AssemblyName System.IO.Compression.FileSystem
$sourceDir = "dist\\SMV-Extracter-{system}-{arch}"
$zipFile = "dist\\SMV-Extracter-Windows-x64.zip"
if (Test-Path $zipFile) {{ Remove-Item $zipFile -Force }}
[IO.Compression.ZipFile]::CreateFromDirectory($sourceDir, $zipFile, 'Fastest', $false)
Write-Host "Created ZIP archive: $zipFile"
'''
        try:
            result = subprocess.run([
                "powershell", "-Command", powershell_script
            ], check=True, capture_output=True, text=True)
            print("ZIP archive created successfully using .NET API")
            return True
        except subprocess.CalledProcessError as e:
            print(f"Failed to create ZIP archive: {e}")
            print(f"Error output: {e.stderr}")
            return False
    
    return False

if __name__ == "__main__":
    # Use PyInstaller from uv environment but run directly (not through uv run)
    print("Building with PyInstaller from uv environment...")
    
    if build_with_pyinstaller():
        create_installer()
        create_zip_archive()
        print("Build process completed!")
    else:
        sys.exit(1)
