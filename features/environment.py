import os
import django
os.environ["DJANGO_SETTINGS_MODULE"] = "paysure.settings"

from django.test import Client

client = Client()
django.setup()
def before_scenario(context, scenario):
    context.client = client




