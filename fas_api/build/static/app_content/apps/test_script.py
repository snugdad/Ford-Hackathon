import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fasapi.settings")

import django
django.setup()

FILE =  'kirby_client_v1.0.0.zip'

from clientAPI.models import FasApp
app = FasApp(appFile=FILE, name=FILE)
app.save()

