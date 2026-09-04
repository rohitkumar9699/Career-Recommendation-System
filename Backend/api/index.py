import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_recommendation_system.settings')

if os.getenv('VERCEL'):
	from django import setup
	from django.core.management import call_command

	setup()
	call_command('migrate', interactive=False, verbosity=0)
	call_command('collectstatic', interactive=False, verbosity=0, clear=False)

from career_recommendation_system.wsgi import application
