import sys
import json
import shutil
import coreapi
import getpass
import zipfile
import requests
from coreapi import codecs, Client

SESSION_TOKEN=None

def quit(opt, client, schema):
    return 'exit'

def display(opt, client, schema):
    print('options:\n\
        register - register a new user\n\
        login - login with <username>, <password>\n\
        list - lists all apps\n\
        install <app> - install an app from the list of apps\n\
        help - list options\n\
        quit - exit client')
    return True

def formHeader():
    global SESSION_TOKEN
    return {'Authorization': 'Token {}'.format(SESSION_TOKEN)}

def register(opt, client, schema):
    while True:
        username = input('username:')
        if not username:
            print('username required')
            continue
        pswd = getpass.getpass('password:')
        if not pswd:
            print('password required')
            continue
        pswdchk = getpass.getpass('password(confirm):')
        if pswd != pswdchk:
            print('passwords do not match')
            continue
        email = input('email:')
        if not email:
            print('email required')
            continue
        break
    try:
        new_user = client.action(
                        schema, ['register', 'create'],
                        params={
                            "username"  :username,
                            'password'  :pswd,
                            'email'     :email
                        }
                    )
    except Exception as e:
        print(e)
        return False
    print('user registered')
    return True

def login(opt, client, schema):
    while True:
        username = input('username:')
        password = getpass.getpass('password:')
        if username and password:
            break
        else:
            print('username or password not valid')
            continue
    params = {'username': username, 'password': password}
    try:
        action = ['login', 'create']
        result = client.action(schema, action, params)
        action = ['token', 'create']
        result = client.action(schema, action, params)
        print(formHeader())
    except Exception as e:
        print(e)
        print('validation failed')
        return False
    global SESSION_TOKEN
    SESSION_TOKEN = result['token']
    print(SESSION_TOKEN, formHeader())
    auth = coreapi.auth.TokenAuthentication(
        scheme='OAUTH',
        token=SESSION_TOKEN
    )
    client = coreapi.Client(auth=auth)
    print(username + ' logged in')
    return True#{'client':client}

def list_apps(opt, client, schema):
#    print(client.auth)
    if opt == 'installed':
        for file in next(os.walk('./apps/'))[1]:
            print(file)
        return True
    elif opt == 'all' or not opt:
        try:
            print(formHeader())
            response = requests.request(
                            method='GET',
                            url='http://fas.42king.com:8197/api/apps/',
                            headers=formHeader()
                        )
            appList = json.loads(response.content)
            appList = json.loads(appList['apps'])
#            for key in appList: print (key)
            if appList:
                try:
                    print('Apps:')
                    for app in appList:
#                        print(app)
                        print('\t' + app['fields']['name'])
                except Exception as e:
                    print(e)
                    print('apps could not be displayed')
                    return False
        except Exception as e:
            print(e)
            print('not authorized')
            return False
    else:
        print(opt + ' is an invalid option, try \'list installed\' or \'list all\'')
        return True

def install(app, client, schema):
    print(schema)
    result = client.action(schema, keys=['download', 'read'], params={'path':app})
    #response = client.get('http://fas.42king.com:8197/api/download/' + result)
    print(result)
#    sys.exit(1)
    zip_ref = zipfile.ZipFile(result, 'r')
    zip_ref.extractall('./apps/' + app)
    zip_ref.close()
    print(result)
    while True:
            print('would you like to install another app?:')
            list_apps(None, client, schema)
            yano = input('[ya\\\\no]: ')
            if 'y' in yano:
                continue
            elif 'n' in yano:
                break
            else:
                print('incorrect (input == [\'ya\', \'no\'])')

def run_client():
    t = True
    client = coreapi.Client()
    try:
        schema = client.get('http://fas.42king.com:8197/api/schema')
        print('Welcome to Krby CLI Client!')
        display(None, None, None)
    except Exception as e:
        print(e)
        print('server down for maintenence')
        t = False
    result = None
    while t:
        opt = input('$> ').split()
        opt.append(None)
        if opt[0] in func:
            result = func[opt[0]](opt[1], client, schema)
        if result == False:
            print('there was an error with your request')
            continue
        elif isinstance(result, dict):
            print('client updated with auth')
            client = result['client']
            schema = client.get('http://fas.42king.com:8197/api/schema')
        elif result == 'exit':
            t = False
    print('Goodbye!')

def test_client_connection():
    client = coreapi.Client()
    schema = client.get('http://fas.42king.com:8197/api/schema/')
    action = ['token', 'create']
    params = {'username': "test", 'password': 'test'}
    result = client.action(schema, action, params)
    
    action = ['login', 'create']
    print(result)
    auth = coreapi.auth.TokenAuthentication(
        scheme='OAUTH',
        token=result['token']
    )
    result = client.action(schema, action, params)
    print(result)
    clent = coreapi.Client(auth=auth)
    print(client.get('http://fas.42king.com:8197/api/apps/'))


func = {
        'register'  :register,
        'login'     :login,
        'list'      :list_apps,
        'install'   :install,
        'help'      :display,
        'quit'      :quit,
}

if __name__ == "__main__":
    '''
    loaded config = load config file
    client = coreapi.Client(loaded config)
    while true:
        try client.connection:
            client.establish connection
        except Exception as err:
            handle(err)
        client.query(client started package={status, etc...})
        client.recieve({updated packages})
        install deps(client.packageList)
        prepare programs to launch

    client = coreapi.Client(CONF_PATH)
    running = True
    try:
        client.connect()
        while running:
            cmd = input('シェル$> ')
            parsed = client.parse(cmd)
            if isinstance(parsed, dict):
                running = client.process(parsed)
            else:
                print(parsed)
            print (running)
    except Exception as err:
        print_exc()
        handle(err)
    '''
#    test_client_connection()
    run_client()
