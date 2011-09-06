import os
import sys

sys.stdout = sys.stderr

# path
root_path = '/home/sa'
project_path = '/home/sa/projcube'
if project_path not in sys.path:
    sys.path.append(project_path)
    sys.path.append(root_path)

# settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

# wsgi
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
