import os
import shutil
import zipfile

from fas_backend.models import FasApp, FasUser
from fas_backend.hashit import hash_dir, zipdir
from fas_backend.serializers import FasAppSerializer, FasUserSerializer
from fas_backend.permissions import IsOwnerOrReadOnly, getPermit, get_man_schema

from django.conf import settings
from django.core import serializers
from django.shortcuts import render
from django.core.cache import cache
#from django.views.generic.base import View
from django.contrib.auth import authenticate, login
#from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.schemas import ManualSchema
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import mixins, generics,renderers, status
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Redis cache settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

def download(request, path):
	file_path = os.path.join(settings.MEDIA_ROOT, request['path'])
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/zip")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
		raise Http404	

class Download(APIView):
	'''
	if user is authenticated
	download option from request
	or return 404
	'''
#	permission_classes = (IsAuthenticated,)
#	@login_required
	def get(self, request, path, format=None):
		print('error @ fasapi_v.2/fas/fas_backend/views.py line 76')
		file_path = os.path.join(settings.APP_ROOT, path)
		print(file_path)
#		return None
#		serializer = FasUserSerializer(data=request.data)
#		if serializer.is_valid():
		if request.user.is_authenticated:
			print('FUGGIN WORKS')
		if os.path.exists(file_path):
    # ziph is zipfile handle
			ha = hash_dir(file_path)
			dirPath = file_path.split('/')

			ha_file = file_path + '/' + str(ha) + '.zip'

			print('HA FILE == ', ha_file)
			shutil.make_archive('app_upload/apps/' + path  + '/' + ha, 'zip', file_path)
#			zipf = zipfile.ZipFile('app_upload/apps/' + path + '/' + ha + '.zip', 'w', zipfile.ZIP_DEFLATED)
#			zipdir('app_upload/apps/' + path + '/', zipf)
#			zipf.close()


			with open(ha_file, 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="application/zip")
				response['Content-Disposition'] = 'inline; filename=' + path
			os.remove('app_upload/apps/' + path + '/' + ha + '.zip')
			return response
		raise Http404
		#return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class Login(APIView):

	if coreapi is not None and coreschema is not None:
		schema = get_man_schema('login')

	def post(self, request, format='application/json'):
		user = authenticate(username=request.data['username'], password=request.data['password'])
#		print('USER IS AUTHENTICATED LOGIN == ', user.is_authenticated)
		serializer = FasUserSerializer(data=request.data)#, context={'request': request})
		if serializer.is_valid():
			user = serializer.save()	
		if user is not None:
#			print(request, user)
			login(request, user)
			print(user.is_authenticated)
#			return Response(serializer.data, status=status.HTTP_201_CREATED)
			return Response({
				'resp':'user logged in',
#				'user':serializer.data,
			})
		else:
			return Response({'status':'user invalid'})

class UserCreate(APIView):
	'''
	consumes a POST request and generates a user with
	valid user/pass/email
	'''
	if coreapi is not None and coreschema is not None:
		schema = get_man_schema()


	def post(self, request, format='application/json'):
		serializer = FasUserSerializer(data=request.data, context={'request': request})
		user = None
#		permission = getPerm()
		if serializer.is_valid():
			user = serializer.save()
			permission = Permission.objects.get(
					codename='can_download',
					name='Can download apps',
					content_type=ContentType.objects.get_for_app(FasApp),
				)
			user.user_permissions.add(permission)

		if user:
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def index(request):
	'''
	root index will change in future
	'''
	return render(request, 'index.html')

@api_view
@renderer_classes([renderers.CoreJSONRenderer])
def schema_view(request):
    '''
    generates a scheman of the API
    endpoints
    '''
    generator = schemas.SchemaGenerator(
					title='Fas API',
					url='http://fas.42king.com:8197/api/schema/',
			)
    return Response(generator.get_schema())

#@cache_page(CACHE_TTL)
class FasAppList(generics.ListCreateAPIView):
	'''
	query all available FasApps and return the to the user with a json response
	'''
	queryset = FasApp.objects.all()
	serializer_class = FasAppSerializer
	authentication_classes = (
			authentication.TokenAuthentication,
			authentication.SessionAuthentication
		)
#	permission_classes = (IsAuthenticated,)

	def get(self, request, *args, **kwargs):
#		user = None
#		request = self.context.get("request")
#		if request and hasattr(request, "user"):
#			user = request.user
#		print(user)
#		print(args)
#		print(kwargs)
#		print('OK FUCKO')
#		print(request)
		print(request.auth)
#		print(request.scheme)
#		print(request.body)
#		print(request.META['HTTP_AUTHORIZATION'])
		
#		print(request.session)
#		print(Token.objects.filter(token=request.data['token']).exists)
#		print(request.data)
#		print(request.user)
		print('BIG IF TRU == ', request.user.is_authenticated)
		if request.user.is_authenticated:
			content = {
				'status': 'request was permitted',
				'apps': serializers.serialize('json', self.get_queryset()),
			}
			return Response(content)
		return Response({'status': 'request not permitted, please log in'})

class CreateFasAuthToken(ObtainAuthToken):
	'''
	if a user is authenticated, we provide a session token to make
	interactions with the API
	'''
	def get(self, request, *args, **kwargs):
		serializer = self.serializer_class(data=request.data,
						context={'request': request})
		serializer.is_valid(raise_exception=True)
		user = serializer.validated_data['user']
		token, created = Token.objects.get_or_create(user=user)
		return Response({
			'token': token.key,
			'user_id': user.pk,
			'email': user.email
		})
'''
# TODO : do something with this
#@cache_page(CACHE_TTL)
class FasAppDetail(generics.RetrieveUpdateDestroyAPIView):
	queryset = FasApp.objects.all()
	serializer_class = FasAppSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                      		IsOwnerOrReadOnly,)
'''

#@cache_page(CACHE_TTL)
class FasUserList(generics.ListAPIView):
	'''
	admin list of all users
	'''
	# TODO : admin only reads
	queryset = FasUser.objects.all()
	serializer_class = FasUserSerializer

#@cache_page(CACHE_TTL)
class FasUserDetail(generics.RetrieveAPIView):
	'''
	admin detail of all users
	'''
	# TODO : admin only reads
	queryset = FasUser.objects.all()
	serializer_class = FasUserSerializer
