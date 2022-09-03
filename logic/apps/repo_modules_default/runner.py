import sys

sys.stdout = open('logs.log', 'a')
sys.stderr = open('logs.log', 'a')

try:
    import module
except Exception as e:
    print(e.with_traceback())
    exit(1)
