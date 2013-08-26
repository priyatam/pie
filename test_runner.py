import sys, os
sys.path.append(".") # Add bake to PYTHONPATH
os.chdir("test")

import test.tests as tests
tests.main()

