import os, yaml

SENDFILE_BACKEND = 'sendfile.backends.xsendfile'
ACTIVATE_RAVEN = False

if(os.environ.get("DISABLE_HAYSTACK", False) != False): HAYSTACK_SIGNAL_PROCESSOR = 'celery_haystack.signals.BaseSignalProcessor'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.FileHandler',
            'filename': '/var/log/truffe2/django.log'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins', 'file'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

app_config = os.environ.get("APP_CONFIG", os.path.dirname(os.path.abspath(__file__)) + "/config.yaml")
    
with open(app_config, 'r') as stream:

    cfg = yaml.safe_load(stream)

hosts = []  # type: List[str]

hosts_from_env = os.environ.get("HOST", "")
if hosts_from_env:
    hosts = hosts_from_env.split(":")
else:
    hosts = cfg["ALLOWED_HOSTS"]

if not hosts:
    raise Exception("Could not deternime Application Host.")

DEBUG = cfg["DEBUG"]
DATABASES = cfg["DATABASES"]

ALLOWED_HOSTS = hosts

EMAIL_HOST = cfg["EMAIL_HOST"]

EMAIL_PORT = cfg["EMAIL_PORT"]

SECRET_KEY = cfg["SECRET_KEY"]

BROKER_URL = cfg["BROKER_URL"]

try: 
    ADMINS = (('Admin', cfg["ADMIN_EMAIL"]))
except:
    ADMINS = (('AGEPIT', 'informatique@agepoly.ch'))

MANAGERS = ADMINS
