#!/usr/bin/env python3
"""
PyInstaller hook for sv_ttk package
Enhanced hook for single executable builds
"""

from PyInstaller.utils.hooks import collect_all, collect_data_files, collect_submodules


datas, binaries, hiddenimports = collect_all('sv_ttk')


sv_ttk_datas = collect_data_files('sv_ttk')
datas.extend(sv_ttk_datas)


sv_ttk_submodules = collect_submodules('sv_ttk')
hiddenimports.extend(sv_ttk_submodules)


try:
    from PyInstaller.utils.hooks import copy_metadata
    sv_ttk_metadata = copy_metadata('sv-ttk')  
    datas.extend(sv_ttk_metadata)
except Exception:
    
    pass


hiddenimports.extend([
    'sv_ttk',
    'sv_ttk.themes',
    'sv_ttk.constants',
    'sv_ttk.loader',
])
