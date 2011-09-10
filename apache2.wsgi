import os
import sys

sys.stdout = sys.stderr

# path
root_path = '/home/sa/www'
project_path = '/home/sa/www/projcube'
if project_path not in sys.path:
    sys.path.append(project_path)
if root_path not in sys.path:
    sys.path.append(root_path)

# settings
import settings
os.environ['DJANGO_SETTINGS_MODULE'] = 'projcube.settings'

# wsgi
import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
