import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'career_recommendation_system.settings')

if os.getenv('VERCEL'):
	from django import setup
	from django.core.management import call_command

	setup()
	call_command('migrate', interactive=False, verbosity=0)

	from django.contrib.auth import get_user_model

	superuser_email = os.getenv('DJANGO_SUPERUSER_EMAIL', 'admin@gmail.com')
	superuser_password = os.getenv('DJANGO_SUPERUSER_PASSWORD', 'admin')
	if superuser_email and superuser_password:
		user_model = get_user_model()
		if not user_model.objects.filter(email=superuser_email).exists():
			user_model.objects.create_superuser(
				email=superuser_email,
				password=superuser_password,
				username=os.getenv('DJANGO_SUPERUSER_USERNAME', 'admin'),
				mobile=os.getenv('DJANGO_SUPERUSER_MOBILE', '0000000000'),
				gender=os.getenv('DJANGO_SUPERUSER_GENDER', 'unspecified'),
			)

from career_recommendation_system.wsgi import application
