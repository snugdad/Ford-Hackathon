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

print(FILE + str(ha) + '.zip')


zipf = zipfile.ZipFile(FILE + str(ha) + '.zip', 'w', zipfile.ZIP_DEFLATED)
zipdir(FILE, zipf)
zipf.close()


from django.contrib.auth.models import User
from fas_backend.models import FasApp
#app = FasApp(url=ha, name=dirPath[-2])
#app.save()
