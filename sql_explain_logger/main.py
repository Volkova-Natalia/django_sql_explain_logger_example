"""
For using, you should copy (and rename to "sql_explain_logger.py") the file to your django app to package, for example, "utils".



See example in ..\project_sample\backend_django
WHERE
- copy of the file: ..\project_sample\backend_django\apps\sample\utils\sql_explain_logger.py
- using the function in ..\project_sample\backend_django\apps\sample\views.py
- logging settings in ..\project_sample\backend_django\backend_django\settings\local.py

You can see the logs when run tests: ..\project_sample\backend_django\apps\sample\tests.py
"""

import logging
from django.db import connection

logger = logging.getLogger(__name__)


def sql_explain_logger():
    for i, query in enumerate(connection.queries):
        sql = query['sql']
        if 'SELECT' in sql or 'DELETE' in sql or 'INSERT' in sql or 'REPLACE' in sql or 'UPDATE' in sql:
            sql_explain = 'EXPLAIN FORMAT=JSON ' + sql
            msg = 'Execution Plan:\n' + sql_explain + '\n'
            with connection.cursor() as cursor:
                cursor.execute(sql_explain)
                row = cursor.fetchone()
                msg += row[0]
            logger.debug(msg)
