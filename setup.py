#!/usr/bin/env python
from distutils.core import setup
import os.path as P

LOCAL = P.abspath(P.expanduser('~/.evoke'))

setup( name='evoke (evk)',
       version='0.1',
       description='Easily create, use, organize, and share your often-used & well-worn code snippets and project templates',
       author='Huy Nguyen',
       author_email='huy@huyng.com',
       packages=['evoke'],
       data_files=[(LOCAL, ['datafiles/config', 
                            'datafiles/completions', 
                            'datafiles/evoke.sh'])],
       scripts=['scripts/evk'] )