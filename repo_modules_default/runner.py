import sys

sys.stdout = open('logs.log', 'w')
sys.stderr = open('logs.log', 'w')

try:
    import module
except Exception as e:
    print(e.with_traceback())
