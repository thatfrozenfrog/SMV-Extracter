#!/usr/bin/env python3
"""
PyInstaller hook for sv_ttk package
"""

from PyInstaller.utils.hooks import collect_all, collect_data_files

# Collect all sv_ttk files including data files and submodules
datas, binaries, hiddenimports = collect_all('sv_ttk')

# Explicitly collect data files (themes, tcl files, etc.)
sv_ttk_datas = collect_data_files('sv_ttk')
datas.extend(sv_ttk_datas)

# Add any hidden imports that might be missed
hiddenimports.extend([
    'sv_ttk',
    'sv_ttk.themes',
])
