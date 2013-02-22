#!/usr/bin/env python
import sys
import re
import json

# Regexp for matching erronous doctest report
ERROR_RE = re.compile('File\s+\"(?P<file>\w+\.py)\"\,'
    '\s+line\s+(?P<line>\d+)\,\s+in\s+(?P<func>.*)$', re.MULTILINE)


def error_line(doctest_out):
    errors = []
    for line in doctest_out.split('\n'):
        match = re.match(ERROR_RE, line)
        if match:
            name, line, func = match.groups()
            errors.append({
                'src': name,
                'line': line,
                'func': func
            })

    return errors


if __name__ == '__main__':
    text = sys.stdin.read()
    errors = error_line(text)
    print json.dumps(errors)
