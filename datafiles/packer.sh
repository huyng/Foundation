## {{{ http://code.activestate.com/recipes/497000/ (r1)
#!/bin/sh
# This is a self-extracting executable.
# Execute this like any normal executable.
# You may need to "chmod a+x" this file.
# This is a binary ZIP file with a Python loader header.
#
# Bourne shell loader:
PYTHON=$(which python 2>/dev/null)
if [ ! -x "$PYTHON" ] ; then
    echo "Python not found!"
    exit 1
fi
exec $PYTHON -c "
# Python loader:
import sys, os
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
import zipfile
print sys.argv
zf = zipfile.ZipFile(fname)
zf.extractall('/tmp/')

" $0 $@
# Zip file:
## end of http://code.activestate.com/recipes/497000/ }}}
