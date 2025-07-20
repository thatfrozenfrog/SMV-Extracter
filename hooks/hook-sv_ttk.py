#!/usr/bin/env python3
"""
PyInstaller hook for sv_ttk package
Enhanced hook for single executable builds
"""

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules

# Collect all sv_ttk data, binaries, and hidden imports
datas, binaries, hiddenimports = collect_all('sv_ttk')

# Explicitly collect data files (themes, etc.)
sv_ttk_datas = collect_data_files('sv_ttk')
datas.extend(sv_ttk_datas)

# Collect all submodules
sv_ttk_submodules = collect_submodules('sv_ttk')
hiddenimports.extend(sv_ttk_submodules)

# Try to copy metadata safely
try:
    from PyInstaller.utils.hooks import copy_metadata
    sv_ttk_metadata = copy_metadata('sv-ttk')  # Note: package name with hyphen
    datas.extend(sv_ttk_metadata)
except Exception:
    # If metadata copy fails, continue without it
    pass

# Ensure all important sv_ttk modules are included
hiddenimports.extend([
    'sv_ttk',
    'sv_ttk.themes',
    'sv_ttk.constants',
    'sv_ttk.loader',
])
