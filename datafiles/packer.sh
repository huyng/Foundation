## {{{ http://code.activestate.com/recipes/497000/ (r1)
#!/bin/sh
# This is a self-extracting executable.
# Execute this like any normal executable.
# You may need to "chmod a+x" this file.
# This is a binary ZIP file with a Python loader header.
#
# Bourne shell loader:
PYTHON=$(which python 2>/dev/null)
FDN=$(which fdn 2>/dev/null)
if [ ! -x "$PYTHON" ] ; then
    echo "Python not found!"
    exit 1
fi
if [ ! -x "$FDN" ]; then
    echo "fdn not found, installing ..."
    git clone git://github.com/huyng/Foundation.git
    pushd Foundation
    exec $PYTHON setup.py install --user
fi
exec $PYTHON -c "
# Python loader:
import sys, os
import subprocess as SP
if int(sys.version[0])<2:
    print 'Python version 2.3 final or greater is required.'
    print 'Your version is', sys.version
    os._exit(1)
major = sys.version_info[0]
minor = sys.version_info[1]
releaselevel = sys.version_info[3]
if (major==2 and minor<3) or (major==2 and minor==3 and releaselevel!='final'):
    print 'Python version 2.3 final or greater is required.'
    print 'Your version is', sys.version
    os._exit(1)
fname = sys.argv[1]
SP.call('fdn add %s' % fname, shell=True)
" $0 $@
# Zip file:
## end of http://code.activestate.com/recipes/497000/ }}}
