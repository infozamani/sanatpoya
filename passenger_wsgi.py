import sys
import os
import pymysql

pymysql.install_as_MySQLdb()

# مسیر مطلق پروژه
project_path = '/home/cp65771/sanatpoya'
if project_path not in sys.path:
    sys.path.insert(0, project_path)

# تنظیم متغیر محیطی
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sanatpoya.settings')

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()