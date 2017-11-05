# -*- mode: python -*-

block_cipher = None


a = Analysis(['Main.py'],
             pathex=['/Users/gongqingfeng/coder/codes/DrcomUI'],
             binaries=[],
             datas=[],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='Main',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='/Users/gongqingfeng/coder/codes/DrcomUI/images/python_128px.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='Main')
app = BUNDLE(coll,
             name='Main.app',
             icon='/Users/gongqingfeng/coder/codes/DrcomUI/images/python_128px.ico',
             bundle_identifier=None)
