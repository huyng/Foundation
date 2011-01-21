#!/usr/bin/env python
from distutils.core import setup
import os.path as P

LOCAL = P.abspath(P.expanduser('~/.foundation'))

setup( name='foundation (fdn)',
       version='0.1',
       description='Easily create, use, organize, and share your often-used & well-worn code snippets and project templates',
       author='Huy Nguyen',
       author_email='huy@huyng.com',
       packages=['foundation'],
       data_files=[(LOCAL, ['datafiles/config', 
                            'datafiles/completions', 
                            'datafiles/foundation.sh',
                            'datafiles/empty_file',
                            'datafiles/packer.sh'])],
       scripts=['scripts/fdn'] )