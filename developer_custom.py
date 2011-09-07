#coding=utf8
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'projcube',
        #'NAME': os.path.join(ROOT, '../MEDIA/testDB.sqlite'),
        'USER': 'root',                      # Not used with sqlite3.
        #'USER': '',                      # Not used with sqlite3.
        'PASSWORD': 'nodemix',                  # Not used with sqlite3.
        #'PASSWORD': '',                  # Not used with sqlite3.
        'HOST': '',                      # Set to empty string for localhost. Not used with sqlite3.
        #'HOST': '10.10.10.59',                      # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '',                      # Set to empty string for default. Not used with sqlite3.
        #'PORT': '3306',                      # Set to empty string for default. Not used with sqlite3.
    }
}

ROOT_PATH = '/home/sa/www/projcube'
LOG_DIR = '/home/sa/log'
