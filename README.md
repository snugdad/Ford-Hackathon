# Running FAS-API
```
cd fas_api
vi config.sh
```

install python dependencies andset your environment variables in config.sh like:

```
pip3 install -r requirements.txt

...

export FAS_DB_USER='<username>'
```

```
source fas-env/bin/activate
source config.sh
HTTPS=1 python3 manage.py runserver <host>:<port>
```


# Running KRBY-CLI
```
cd fas_cli	
source fas-client-env
python3 client.py
```
