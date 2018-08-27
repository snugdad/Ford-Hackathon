import os
import sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "fas.settings")

import django
django.setup()

import zipfile
from app_upload.hashit import hash_dir

def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for file in files:
            ziph.write(os.path.join(root, file))

FILE = sys.argv[1]
ha = hash_dir(FILE)
dirPath = FILE.split('/')

from django.contrib.auth.models import User
from fas_backend.models import FasApp
app = FasApp(name=dirPath[-2])
app.save()
