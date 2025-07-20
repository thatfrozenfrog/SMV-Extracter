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
    
    
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onedir",  
        "--windowed",  
        "--name", f"SMV-Extracter-{system}-{arch}",
        "--distpath", "dist",
        "--workpath", "build",
        "--specpath", ".",
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
        "main.py"
    ]
    
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
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"], check=True)
        print("PyInstaller installed successfully")
    except:
        print("Failed to install PyInstaller")
        sys.exit(1)
    
    if build_with_pyinstaller():
        create_installer()
        create_zip_archive()
        print("Build process completed!")
    else:
        sys.exit(1)
