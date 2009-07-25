set -e
set -x
env CLASSPATH=$(python -c 'import os ; from os.path import * ; print ":".join(join("cp", b) for b in sorted(os.listdir("cp")))') /home/jwal/system/jython2.5.0/bin/jython etree_test.py
