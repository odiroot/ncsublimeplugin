#!/usr/bin/env python
import sys
import re
import collections

# Regexp for matching erronous doctest report
ERROR_RE = re.compile('File\s+\"(?P<file>\w+\.py)\"\,'
    '\s+line\s+(?P<line>\d+)\,\s+in\s+(?P<func>.*)$', re.MULTILINE)

# Format of the error reports
DocError = collections.namedtuple('DocError', ['src', 'line', 'func'])


def error_line(doctest_out):
    errors = []
    for line in doctest_out.split('\n'):
        match = re.match(ERROR_RE, line)
        if match:
            name, line, func = match.groups()
            errors.append(DocError(src=name, line=line, func=func))

    return errors


if __name__ == '__main__':
    print error_line(open(sys.argv[1]).read())
