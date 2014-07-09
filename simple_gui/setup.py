
from distutils.core import setup
import py2exe, sys
from distutils.filelist import findall
import os


sys.path.append("C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")

#includes = ["scipy.sparse.csgraph._validation", "scipy.spatial.kdtree", "scipy.sparse.csgraph._shortest_path"]

setup(name = 'FBGSimpleWXApp', version = '0.1',windows=['FBGSimpleWXApp.py'], py_modules=['FBGSimpleWXApp'],
    options={
        'py2exe': {
                    'packages' : ['pytz'],
                    'excludes': ['_gtkagg', '_tkagg'],
                    #'includes':includes,
                    'dll_excludes': ['libgdk-win32-2.0-0.dll','libgdk_pixbuf-2.0-0.dll', 'libgobject-2.0-0.dll']
                   }
        }
)
