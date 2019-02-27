# -*- mode: python -*-

block_cipher = None


a = Analysis(['engine.py', 'data.py', 'ui_interface.py', 'main.py'],
             pathex=['D:\\Programs\\Python\\excel_indexer'],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='engine',
          debug=False,
          strip=False,
          upx=True,
          runtime_tmpdir=None,
          console=True )
