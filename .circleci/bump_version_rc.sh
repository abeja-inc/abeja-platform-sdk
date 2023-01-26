#!/bin/sh
VERSION=`PYTHONPATH=./ poetry version | cut -d ' ' -f 2`

if [ `echo '${VERSION}' | grep 'rc'` ]; then
    poetry version "${VERSION}"
else
    poetry version "${VERSION}rc1"
fi
