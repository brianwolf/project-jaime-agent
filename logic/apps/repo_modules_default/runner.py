import sys

import tools

sys.stdout = open('logs.log', 'a')
sys.stderr = open('logs.log', 'a')

try:
    import module

except Exception as e:
    tools.log.error(e.with_traceback())
    exit(1)
