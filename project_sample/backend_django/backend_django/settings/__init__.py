import os
from dotenv import load_dotenv


# load_dotenv()
env_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) + '/.env'
load_dotenv(dotenv_path=env_path)


APPLICATION_ENVIRONMENT = os.getenv('APPLICATION_ENVIRONMENT')
IMPORT_SETTINGS_ENVIRONMENT = 'from .' + APPLICATION_ENVIRONMENT + ' import *'
exec(IMPORT_SETTINGS_ENVIRONMENT)
