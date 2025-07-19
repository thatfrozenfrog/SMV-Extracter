# SMV-Extracter Cross-Platform Builds

This GitHub Actions workflow automatically builds SMV-Extracter for both Windows and Ubuntu Linux using Nuitka.

## How It Works

### 🔄 **Automatic Builds**
- **Every push** to main branch
- **Every pull request**
- **Manual trigger** via GitHub Actions
- **Tagged releases** (v1.0.0, etc.)

### 🎯 **Supported Platforms**
- **Windows 10/11** (x64)
- **Ubuntu 18.04+** (x64)

### 📦 **Build Process**
1. **Setup Environment**: Python 3.11 + dependencies
2. **Install FFmpeg**: Platform-specific installation
3. **Nuitka Compilation**: Python → Native executable
4. **Package Creation**: ZIP (Windows) / TAR.GZ (Linux)
5. **Release Creation**: Automatic GitHub releases

### 💾 **Download Sizes**
- **Windows**: ~80-120 MB
- **Linux**: ~70-100 MB

## Manual Build

To build locally:

```bash
# Install dependencies
pip install nuitka
pip install -r requirements.txt

# Run build script
python build_ci.py
```

## Creating Releases

1. **Tag your commit**:
   ```bash
   git tag v1.0.0
   git push origin v1.0.0
   ```

2. **GitHub Actions will**:
   - Build for both platforms
   - Create release with binaries
   - Upload installation packages

## Installation for End Users

### Windows
1. Download `SMV-Extracter-Windows-x64.zip`
2. Extract to any folder
3. Run `install.bat`

### Linux
1. Download `SMV-Extracter-Linux-x64.tar.gz`
2. Extract: `tar -xzf SMV-Extracter-Linux-x64.tar.gz`
3. Run: `sudo ./install.sh`

## Benefits

✅ **No Python Required** - Customers don't need Python installed
✅ **Cross-Platform** - Same codebase builds everywhere  
✅ **Automatic Updates** - Push code → Get releases
✅ **Traditional Installers** - Familiar installation experience
✅ **Small Downloads** - Only ~80-120MB per platform
