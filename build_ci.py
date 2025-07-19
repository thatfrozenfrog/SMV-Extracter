#!/usr/bin/env python3
"""
Simplified Nuitka build script for CI/CD
Handles cross-platform builds with better error handling
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def get_platform_info():
    """Get platform and architecture info"""
    system = platform.system().lower()
    arch = "x64" if platform.machine().lower() in ["x86_64", "amd64"] else "x86"
    return system, arch

def build_with_nuitka():
    """Build the application with Nuitka"""
    system, arch = get_platform_info()
    
    print(f"Building SMV-Extracter for {system}-{arch}")
    print(f"Python version: {sys.version}")
    
    # Base Nuitka command
    cmd = [
        sys.executable, "-m", "nuitka",
        "--standalone",
        "--assume-yes-for-downloads",
        "--output-dir=dist",
        f"--output-filename=SMV-Extracter-{system}-{arch}",
        "--include-package=customtkinter",
        "--include-package=yt_dlp", 
        "--include-package=moviepy",
        "--include-package=numpy",
        "--include-package=PIL",
        "--include-package=requests",
        "--include-package=ffmpeg",
        "--enable-plugin=tk-inter",
        "--nofollow-import-to=pytest",  # Exclude test frameworks
        "--nofollow-import-to=setuptools",  # Reduce bloat
        "main.py"
    ]
    
    # Platform-specific options
    if system == "windows":
        cmd.extend([
            "--windows-console-mode=disable",
            "--windows-company-name=SMV-Extracter",
            "--windows-product-name=SMV Video Extractor",
            "--windows-file-version=1.0.0",
            "--windows-product-version=1.0.0",
        ])
    
    print(f"Running: {' '.join(cmd)}")
    
    try:
        # Run the build with real-time output
        result = subprocess.run(cmd, check=True, text=True)
        print("Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"Build failed with exit code {e.returncode}")
        return False

def create_installer():
    """Create platform-specific installer"""
    system, arch = get_platform_info()
    dist_dir = Path("dist")
    
    if system == "windows":
        installer_content = '''@echo off
echo Installing SMV-Extracter...
mkdir "%USERPROFILE%\\SMV-Extracter" 2>nul
xcopy /E /Y "main.dist\\*" "%USERPROFILE%\\SMV-Extracter\\"
echo.
echo SMV-Extracter installed to %USERPROFILE%\\SMV-Extracter
echo You can create a desktop shortcut to the executable.
pause
'''
        installer_path = dist_dir / "install.bat"
    else:
        installer_content = '''#!/bin/bash
echo "Installing SMV-Extracter..."
sudo mkdir -p /opt/SMV-Extracter
sudo cp -r main.dist/* /opt/SMV-Extracter/
sudo ln -sf /opt/SMV-Extracter/SMV-Extracter-linux-x64 /usr/local/bin/smv-extracter
echo "✅ SMV-Extracter installed to /opt/SMV-Extracter"
echo "You can run it with: smv-extracter"
'''
        installer_path = dist_dir / "install.sh"
    
    installer_path.write_text(installer_content)
    if system != "windows":
        os.chmod(installer_path, 0o755)
    
    print(f"Created installer: {installer_path}")

if __name__ == "__main__":
    if build_with_nuitka():
        create_installer()
        print("Build process completed!")
    else:
        sys.exit(1)
