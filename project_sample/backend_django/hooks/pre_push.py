import os
from dotenv import load_dotenv

load_dotenv()
APPLICATION_ENVIRONMENT = os.getenv('APPLICATION_ENVIRONMENT')

if APPLICATION_ENVIRONMENT == 'local':
    with open(r'../../.git/hooks/pre-push', 'tw') as file:
        file.write(r"""#!/bin/sh
echo "| log pre-push | start hook"        
git stash -q --keep-index


cd project_sample/backend_django


echo "| log pre-push | begin delete venv:"
find venv/* -delete
echo "| log pre-push | end delete venv"

echo "| log pre-push | begin virtualenv venv"
virtualenv venv
echo "| log pre-push | end virtualenv venv"

echo "| log pre-push | begin source venv/Scripts/activate"
source venv/Scripts/activate
echo "| log pre-push | end source venv/Scripts/activate"

echo "| log pre-push | begin pip install -r requirements/local.txt"
pip install -r requirements/local.txt
echo "| log pre-push | end pip install -r requirements/local.txt"


echo "| log pre-push | begin ./manage.py test"
./manage.py test
RESULT_test=$?
echo "| log pre-push | end ./manage.py test"

echo "| log pre-push | begin deactivate"
deactivate
echo "| log pre-push | end deactivate"


[ $RESULT_test -ne 0 ] && echo "
------------------
Result: FAIL TESTS
------------------
"


git stash pop -q
echo "| log pre-push | stop hook"
[ $RESULT_test -ne 0 ] && exit 1
exit 0
""")
