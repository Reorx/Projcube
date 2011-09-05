import os
import sys

sys.stdout = sys.stderr

# path
project_path = '/home/sa/projcube'
if project_path not in sys.path:
    sys.path.append(project_path)

# settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'projcube.settings'

# wsgi
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
