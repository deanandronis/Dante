# -*- mode: python -*-
files_tree = Tree('C:\Users\Dean\Documents\GitHub\Dante')
a = Analysis(['main.py', 'entities.py'],
             pathex=['C:\\Users\\Dean\\Documents\\GitHub\\Dante'],
             hiddenimports=[],
             hookspath=None,
             runtime_hooks=None)
pyz = PYZ(a.pure)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='main.exe',
          debug=False,
          strip=None,
          upx=True,
          console=True )	  
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
			   files_tree,
               strip=None,
               upx=True,
               name='main'
			   
			   )
