import sys
from pylint.lint import Run
from anybadge import Badge
from io import StringIO

stdout = sys.stdout
sys.stdout = StringIO()
file = "ddpp.py"

ARGS = ["ddpp.py", "ddpp_classes.py" '--reports=n']
Run(ARGS, exit=False)
output = sys.stdout.getvalue()
sys.stdout = stdout
last_line = output.split('\n')[-3]
score = last_line.split()[6].split('/')[0]
thresholds = {2: 'red',
              4: 'orange',
              6: 'yellow',
              10: 'green'}
badge = Badge('pylint', score, thresholds=thresholds)
badge.write_badge("pylint.svg")
