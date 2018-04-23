# This file is needed to impport the package
import os
import sys

# Append current folder to path
ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.insert(0, ROOT)


from create_inputs import main

if __name__ == '__main__':
    main()
