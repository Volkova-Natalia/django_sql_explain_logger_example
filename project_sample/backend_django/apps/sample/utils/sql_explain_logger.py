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
