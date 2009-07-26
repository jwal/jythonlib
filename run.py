#/usr/bin/env python

import optparse
import os
import sys

if __name__ == "__main__":
    root = os.path.dirname(os.path.abspath(__file__))
    rootcp = os.path.join(root, "cp")
    parser = optparse.OptionParser(__doc__, prog=sys.argv[0])
    parser.allow_interspersed_args = False
    options, args = parser.parse_args(sys.argv[1:])
    if len(args) == 0:
        args = ["jython", os.path.join(root, "etree_test.py")]
    env = os.environ.copy()
    cp = env.get("CLASSPATH")
    if cp is None:
        cp = []
    else:
        cp = cp.split(os.pathsep)
    cp.extend(os.path.join(rootcp, b) for b in os.listdir(rootcp))
    env["CLASSPATH"] = os.pathsep.join(cp)
    os.execvpe(args[0], args, env)
