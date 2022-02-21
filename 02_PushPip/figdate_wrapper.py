import venv
import tempfile
import sys
import subprocess
from os.path import join
import shutil

tmp_dir_path = tempfile.mkdtemp()
venv.create(tmp_dir_path, with_pip=True)
subprocess.run([join(tmp_dir_path, 'bin', 'pip'), 'install', 'pyfiglet'])
subprocess.run([join(tmp_dir_path, 'bin', 'python'), '-m', 'figdate', *sys.argv[1:]])
shutil.rmtree(tmp_dir_path)
