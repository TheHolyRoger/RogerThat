#!/usr/bin/python

if "rogerthat-dist" in __file__:
    # Dist environment.
    import os
    import sys
    sys.path.append(sys.path.pop(0))
    sys.path.insert(0, os.getcwd())

    import hummingbot
    hummingbot.set_prefix_path(os.getcwd())
else:
    # Dev environment.
    from os.path import dirname, realpath
    import sys
    sys.path.insert(0, dirname(dirname(realpath(__file__))))
