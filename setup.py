import os
from subprocess import Popen


SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CRONFILE = 'crontab.tmp'
cron = '''SHELL=/bin/bash
0 6 * * * cd {0}; source venv/bin/activate && python main.py'''.format(SCRIPT_DIR)


if not os.path.exists(CRONFILE):
    with open(CRONFILE, 'w') as f:
        f.write(cron)

    Popen('crontab {}'.format(CRONFILE), shell=True)
else:
    print('{} already exists!'.format(CRONFILE))

