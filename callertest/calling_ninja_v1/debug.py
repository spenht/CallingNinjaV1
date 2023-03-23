import os
from django.core.management import execute_from_command_line

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'calling_ninja_v1.settings')
execute_from_command_line(['manage.py', 'runserver', '--noreload', '--verbosity', '3'])
