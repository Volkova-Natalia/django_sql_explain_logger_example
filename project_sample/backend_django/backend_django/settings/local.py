"""
    Developer's desktop/workstation.
"""

from .base import *

# print(__file__)


DEBUG = bool(strtobool(os.getenv('DEBUG', 'True')))

ALLOWED_HOSTS.append('localhost')
ALLOWED_HOSTS.append('127.0.0.1')

DATABASES = {}
if 'DATABASES_DEFAULT' in os.environ:
    DATABASES['default'] = eval(os.getenv('DATABASES_DEFAULT'))
else:
    # DATABASES['default'] = {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': os.getenv('MYSQL_DATABASE', 'django_sql_explain_logger_example_mysql_local'),
        'USER': os.getenv('MYSQL_USER'),
        'PASSWORD': os.getenv('MYSQL_ROOT_PASSWORD'),
        'HOST': os.getenv('MYSQL_HOST', 'localhost'),   # different for simple work and for docker
        'PORT': os.getenv('MYSQL_PORT'),
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }


FRONTEND_SCHEME = os.getenv('FRONTEND_SCHEME', 'http')
FRONTEND_HOST = os.getenv('FRONTEND_HOST', 'localhost:3000')

CORS_ALLOW_ALL_ORIGINS = bool(strtobool(os.getenv('CORS_ALLOW_ALL_ORIGINS', 'False')))

# CORS_ALLOWED_ORIGINS.append('http://localhost:3000')
# CORS_ALLOWED_ORIGINS.append('http://127.0.0.1:3000')
CORS_ALLOWED_ORIGINS.append(FRONTEND_SCHEME + r'://' + FRONTEND_HOST)

CORS_ALLOW_CREDENTIALS = bool(strtobool(os.getenv('CORS_ALLOW_CREDENTIALS', 'True')))

# CSRF_TRUSTED_ORIGINS.append('localhost:3000')
# CSRF_TRUSTED_ORIGINS.append('127.0.0.1:3000')
CSRF_TRUSTED_ORIGINS.append(FRONTEND_HOST)





# ---------- LOGGER ----------

is_logging = True
is_logging_sql_explain = True
is_logging_to_file = False


if (is_logging):
    try:
        from sqlparse import format as sqlformat
    except ImportError:
        sqlformat = lambda s, reindent=None: s

    from colorama import (
        init as color_init,
        deinit as color_deinit,
        Fore as color,
        Style as color_style,
    )
    color_init()

    from django.utils.termcolors import colorize
    import time


    def filter_db_backends(record):
        if not hasattr(record, 'stack_patched'):
            if (
                hasattr(record, 'duration') and
                hasattr(record, 'sql') and
                hasattr(record, 'params')
            ):
                if record.duration > 0.05:
                    record.my_message = colorize(
                        text=('\n(%.10f secs)' + '\n%s') % (record.duration,
                                                            '\n'.join(sqlformat(record.sql, reindent=True).strip().splitlines())),
                        fg='red'
                    )
                else:
                    record.my_message = colorize(
                        text=('\n(%.10f secs)' + '\n%s') % (record.duration,
                                                            record.sql),
                        fg='white'
                    )
            else:
                record.stack_patched = True
                return False
            record.stack_patched = True
            return True
        return False


    def filter_sql_explain_logger(record):
        if not is_logging_sql_explain:
            return False
        if not hasattr(record, 'stack_patched'):
            fg = 'green'
            if '"access_type": "ALL"' in record.msg:
                fg = 'red'
            record.my_message = colorize(
                text='\n' + record.msg,
                fg=fg
             )
            record.stack_patched = True
            return True
        return False


    def filter_server(record):
        if not hasattr(record, 'stack_patched'):
            if (
                    hasattr(record, 'request') and
                    hasattr(record, 'status_code')
            ):
                record.my_message = colorize(
                    text='\n[%s]  \"%s\" %s %s' % (time.strftime('%d/%b/%Y %H:%M:%S', time.localtime(record.created)),
                                                   record.args[0], record.args[1], record.args[2]),
                    fg='yellow'
                )
            else:
                record.stack_patched = True
                return False
            record.stack_patched = True
            return True
        return False


    def filter_server_logger(record):
        if not hasattr(record, 'stack_patched'):
            record.my_message = colorize(
                text='\n[%s]  %s' % (time.strftime('%d/%b/%Y %H:%M:%S', time.localtime(record.created)),
                                     record.msg),
                fg='yellow'
             )
            record.stack_patched = True
            return True
        return False

    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'loggers': {
            'django.db.backends': {
                'level': 'DEBUG',
                'handlers': ['console_db_backends', 'file_db_backends'] if is_logging_to_file else ['console_db_backends'],
            },
            'apps.sample.utils.sql_explain_logger': {
                'level': 'DEBUG',
                'handlers': ['console_sql_explain_logger', 'file_sql_explain_logger'] if is_logging_to_file else ['console_sql_explain_logger'],
            },
            'django.server': {
                # Log messages related to the handling of requests received by the server invoked by the "manage.py runserver" command.
                # Will not log for tests.
                'handlers': ['console_server', 'file_server'] if is_logging_to_file else ['console_server'],
            },
            'apps.sample.utils.server_logger': {
                # Just for this example because of we use "manage.py test" command to demonstrate logging and can ot use 'django.server'.
                'level': 'DEBUG',
                'handlers': ['console_server_logger', 'file_server_logger'] if is_logging_to_file else ['console_server_logger'],
            }
        },
        'handlers': {
            'console_db_backends': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['filter_db_backends'],
                'formatter': 'format_db_backends',
            },
            'file_db_backends': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filters': ['filter_db_backends'],
                'formatter': 'format_db_backends',
                'filename': 'debug.log',
            },
            'console_sql_explain_logger': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['filter_sql_explain_logger'],
                'formatter': 'format_sql_explain_logger',
            },
            'file_sql_explain_logger': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filters': ['filter_sql_explain_logger'],
                'formatter': 'format_sql_explain_logger',
                'filename': 'debug.log',
            },
            'console_server': {
                'class': 'logging.StreamHandler',
                'filters': ['filter_server'],
                'formatter': 'format_server',
            },
            'file_server': {
                'class': 'logging.FileHandler',
                'filters': ['filter_server'],
                'formatter': 'format_server',
                'filename': 'debug.log',
            },
            'console_server_logger': {
                'level': 'DEBUG',
                'class': 'logging.StreamHandler',
                'filters': ['filter_server_logger'],
                'formatter': 'format_server_logger',
            },
            'file_server_logger': {
                'level': 'DEBUG',
                'class': 'logging.FileHandler',
                'filters': ['filter_server_logger'],
                'formatter': 'format_server_logger',
                'filename': 'debug.log',
            },
        },
        'filters': {
            'filter_db_backends': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': filter_db_backends,
            },
            'filter_sql_explain_logger': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': filter_sql_explain_logger,
            },
            'filter_server': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': filter_server,
            },
            'filter_server_logger': {
                '()': 'django.utils.log.CallbackFilter',
                'callback': filter_server_logger,
            },
        },
        'formatters': {
            'format_db_backends': {
                'format': '{my_message}',
                'style': '{',
            },
            'format_sql_explain_logger': {
                'format': '{my_message}',
                'style': '{',
            },
            'format_server': {
                'format': '{my_message}',
                'style': '{',
            },
            'format_server_logger': {
                'format': '{my_message}',
                'style': '{',
            },
        }
    }
