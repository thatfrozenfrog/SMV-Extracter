#!/usr/bin/env python3
"""
Cross-platform build script for SMV-Extracter using Nuitka
Supports Windows and Ubuntu/Linux builds
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

class NuitkaBuildManager:
    def __init__(self):
        self.platform = platform.system().lower()
        self.arch = platform.machine().lower()
        self.project_root = Path(__file__).parent
        self.dist_dir = self.project_root / "dist"
        
    def get_build_command(self):
        """Generate Nuitka build command for current platform"""
        
        base_cmd = [
            sys.executable, "-m", "nuitka",
            "--standalone",
            "--assume-yes-for-downloads",
            "--remove-output",
            "--output-dir=dist",
            f"--output-filename=SMV-Extracter-{self.platform}-{self.arch}",
            "--follow-imports",
            "--include-package=customtkinter",
            "--include-package=yt_dlp", 
            "--include-package=moviepy",
            "--include-package=numpy",
            "--include-package=PIL",
            "--include-package=requests",
            "--include-package=ffmpeg",
            "--enable-plugin=tk-inter",
            "main.py"
        ]
        
        # Platform-specific options
        if self.platform == "windows":
            base_cmd.extend([
                "--windows-console-mode=disable",  # Updated syntax
                "--windows-company-name=SMV-Extracter",
                "--windows-product-name=SMV Video Extractor", 
                "--windows-file-version=1.0.0",
                "--windows-product-version=1.0.0",
                # "--windows-icon-from-ico=icon.ico",  # Uncomment if you have an icon
            ])
        elif self.platform == "linux":
            base_cmd.extend([
                "--linux-console-mode=enable",  # Keep console for Linux
            ])
        elif self.platform == "darwin":  # macOS
            base_cmd.extend([
                "--macos-create-app-bundle",
                "--macos-app-name=SMV-Extracter",
            ])
            
        return base_cmd
    
    def check_dependencies(self):
        """Check if all required dependencies are installed"""
        print("🔍 Checking dependencies...")
        
        required_packages = [
            "customtkinter", "yt_dlp", "moviepy", "numpy", 
            "PIL", "requests", "ffmpeg"
        ]
        
        missing = []
        for package in required_packages:
            try:
                if package == "ffmpeg":
                    __import__("ffmpeg")  # ffmpeg-python imports as 'ffmpeg'
                else:
                    __import__(package.replace("-", "_"))
                print(f"  ✅ {package}")
            except ImportError:
                missing.append(package)
                print(f"  ❌ {package}")
        
        if missing:
            print(f"\n❌ Missing packages: {', '.join(missing)}")
            print("Install them with: pip install -r requirements.txt")
            return False
        
        print("✅ All dependencies found!")
        return True
    
    def estimate_size(self):
        """Estimate final executable size"""
        size_estimates = {
            "windows": "80-120 MB",
            "linux": "70-100 MB", 
            "darwin": "90-130 MB"
        }
        return size_estimates.get(self.platform, "80-120 MB")
    
    def build(self):
        """Execute the build process"""
        print(f"🚀 Building SMV-Extracter for {self.platform} ({self.arch})")
        print(f"📦 Estimated size: {self.estimate_size()}")
        print(f"📁 Output directory: {self.dist_dir}")
        
        if not self.check_dependencies():
            return False
        
        # Clean previous builds
        if self.dist_dir.exists():
            print("🧹 Cleaning previous builds...")
            import shutil
            shutil.rmtree(self.dist_dir)
        
        # Build command
        cmd = self.get_build_command()
        print(f"\n⚡ Running: {' '.join(cmd)}")
        
        try:
            # Run Nuitka compilation
            result = subprocess.run(cmd, check=True, capture_output=True, text=True)
            print("✅ Build completed successfully!")
            
            # Show output info
            built_files = list(self.dist_dir.glob("*"))
            if built_files:
                print(f"\n📦 Built files in {self.dist_dir}:")
                for file in built_files:
                    if file.is_file():
                        size_mb = file.stat().st_size / (1024 * 1024)
                        print(f"  📄 {file.name} ({size_mb:.1f} MB)")
                    else:
                        print(f"  📁 {file.name}/")
            
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"❌ Build failed!")
            print(f"Error: {e.stderr}")
            return False
    
    def create_installer_script(self):
        """Create simple installer script for the built executable"""
        if self.platform == "windows":
            installer_content = f'''@echo off
echo Installing SMV-Extracter...
mkdir "%USERPROFILE%\\SMV-Extracter" 2>nul
xcopy /E /Y "SMV-Extracter-{self.platform}-{self.arch}.dist\\*" "%USERPROFILE%\\SMV-Extracter\\"
echo.
echo ✅ SMV-Extracter installed to %USERPROFILE%\\SMV-Extracter
echo You can create a desktop shortcut to the executable.
pause
'''
            installer_path = self.dist_dir / "install.bat"
            
        else:  # Linux/macOS
            installer_content = f'''#!/bin/bash
echo "Installing SMV-Extracter..."
sudo mkdir -p /opt/SMV-Extracter
sudo cp -r SMV-Extracter-{self.platform}-{self.arch}.dist/* /opt/SMV-Extracter/
sudo ln -sf /opt/SMV-Extracter/SMV-Extracter-{self.platform}-{self.arch} /usr/local/bin/smv-extracter
echo "✅ SMV-Extracter installed to /opt/SMV-Extracter"
echo "You can run it with: smv-extracter"
'''
            installer_path = self.dist_dir / "install.sh"
        
        installer_path.write_text(installer_content)
        if self.platform != "windows":
            os.chmod(installer_path, 0o755)
        
        print(f"📦 Created installer: {installer_path}")

def main():
    """Main build function"""
    builder = NuitkaBuildManager()
    
    print("=" * 50)
    print("🔨 SMV-Extracter Nuitka Build Tool")
    print("=" * 50)
    
    if builder.build():
        builder.create_installer_script()
        print("\n🎉 Build process completed!")
        print(f"📁 Check the 'dist' folder for your executable")
        print(f"🌍 Platform: {builder.platform} ({builder.arch})")
    else:
        print("\n💥 Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
