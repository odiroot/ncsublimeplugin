#!/usr/bin/env python
import sys
import re
import json

# Regexp for matching erronous doctest report
ERROR_RE = re.compile('File\s+\"(?P<file>.+?\.py)\"\,'
    '\s+line\s+(?P<line>\d+)\,\s+in\s+(?P<func>.*)$', re.MULTILINE)

EXPECTED_RE = re.compile('^Expected\:$')
GOT_RE = re.compile('^Got\:$')
TIP_FMT = 'Expected: %s, Got %s'


def find_details(error_line, lines):
    lines = lines[error_line:]
    expected = ''
    got = ''

    for i, line in enumerate(lines):
        if re.match(GOT_RE, line):
            expected = lines[i - 1].strip()
        if '*' in line:
            got = lines[i - 1].strip()

        if expected and got:
            break

    return expected, got


def error_line(doctest_out):
    lines = doctest_out.split('\n')
    errors = []

    i = 0
    while i < len(lines):
        line = lines[i]
        match = re.match(ERROR_RE, line)
        if match:
            expected, got = find_details(i, lines)
            name, line, func = match.groups()
            errors.append({
                'src': name,
                'line': line,
                'func': func,
                'explanation': TIP_FMT % (expected, got),
            })

        i += 1
    return errors


if __name__ == '__main__':
    text = sys.stdin.read()
    errors = error_line(text)
    print json.dumps(errors)
