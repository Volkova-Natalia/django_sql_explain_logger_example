# django_sql_explain_logger_example

The util is designed for logging **execution plan SQL**.  

See more about **Query Execution Plan**:  
https://dev.mysql.com/doc/refman/8.0/en/execution-plan-information.html   

<br>

### Code of the util:  
[sql_explain_logger/main.c ](#https://github.com/Volkova-Natalia/django_sql_explain_logger_example/blob/main/sql_explain_logger/main.py)  

To use, you should copy the file (and rename to, for example, **sql_explain_logger.py**) to your django app in a package, for example, **utils** (create if necessary).  

<br>

### Example of using
See example in [project_sample/backend_django](#https://github.com/Volkova-Natalia/django_sql_explain_logger_example/tree/main/project_sample/backend_django)  
WHERE  
- copy of the file: [project_sample/backend_django/apps/sample/utils/sql_explain_logger.py](#https://github.com/Volkova-Natalia/django_sql_explain_logger_example/blob/main/project_sample/backend_django/apps/sample/utils/sql_explain_logger.py)  
- using the function in [project_sample/backend_django/apps/sample/views.py](#https://github.com/Volkova-Natalia/django_sql_explain_logger_example/blob/main/project_sample/backend_django/apps/sample/views.py)  
- logging settings in [project_sample/backend_django/backend_django/settings/local.py](#https://github.com/Volkova-Natalia/django_sql_explain_logger_example/blob/main/project_sample/backend_django/backend_django/settings/local.py)  

You can see the logs when run tests: [project_sample/backend_django/apps/sample/tests.py](#https://github.com/Volkova-Natalia/django_sql_explain_logger_example/blob/main/project_sample/backend_django/apps/sample/tests.py)  
by the standard django **manage.py test** command.  

<br>

### Example of log
You will see something like this:
```
Execution Plan:
EXPLAIN FORMAT=JSON SELECT `sample_people`.`id`, `sample_people`.`first_name`, `sample_people`.`last_name` FROM `sample_people`
{
  "query_block": {
    "select_id": 1,
    "table": {
      "table_name": "sample_people",
      "access_type": "ALL",
      "rows": 1,
      "filtered": 100
    }
  }
}
```
This log will be **red** because of **"access_type": "ALL"** - the worst case, you should optimize queries.  

<br>
<br>

```
Execution Plan:
EXPLAIN FORMAT=JSON SELECT `sample_people`.`id`, `sample_people`.`first_name`, `sample_people`.`last_name` FROM `sample_people` WHERE `sample_people`.`id` = 1 LIMIT 21
{
  "query_block": {
    "select_id": 1,
    "table": {
      "table_name": "sample_people",
      "access_type": "const",
      "possible_keys": ["PRIMARY"],
      "key": "PRIMARY",
      "key_length": "8",
      "used_key_parts": ["id"],
      "ref": ["const"],
      "rows": 1,
      "filtered": 100
    }
  }
}
```
This log will be **green** - normal case.  

<br>
<br>

See more about **EXPLAIN**:  
https://dev.mysql.com/doc/refman/8.0/en/explain-output.html  
