
from distutils.core import setup
import py2exe, sys
from distutils.filelist import findall
import os
import matplotlib

matplotlibdatadir = matplotlib.get_data_path()
matplotlibdata = findall(matplotlibdatadir)
matplotlibdata_files = []
for f in matplotlibdata:
    dirname = os.path.join('matplotlibdata', f[len(matplotlibdatadir)+1:])
    matplotlibdata_files.append((os.path.split(dirname)[0], [f]))

sys.path.append("C:\\Program Files\\Microsoft Visual Studio 9.0\\VC\\redist\\x86\\Microsoft.VC90.CRT")

includes = ["scipy.sparse.csgraph._validation", "scipy.spatial.kdtree", "scipy.sparse.csgraph._shortest_path"]

setup(name = 'NrsWXApp', version = '0.1',windows=['NrsWXApp.py'], py_modules=['NrsWXApp'],
    options={
        'py2exe': {
                    'packages' : ['matplotlib', 'pytz'],
                    'excludes': ['_gtkagg', '_tkagg'],
                    'includes':includes,
                    'dll_excludes': ['libgdk-win32-2.0-0.dll','libgdk_pixbuf-2.0-0.dll', 'libgobject-2.0-0.dll']
                   }
        },
    data_files=matplotlib.get_py2exe_datafiles()
)
