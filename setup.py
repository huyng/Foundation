#!/usr/bin/env python
from distutils.core import setup
import os.path as P


CONFIGPATH = P.abspath(P.expanduser('~/.evoke'))

setup( name='evoke (evk)',
       version='0.1',
       description='Easily create, use, organize, and share often used code snippets and project templates',
       author='Huy Nguyen',
       author_email='huy@huyng.com',
       data_files=[(CONFIGPATH, ['config/config.yaml'])],
       scripts=['scripts/evk'] )