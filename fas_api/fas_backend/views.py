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
cache.clear()
#from django.views.generic.base import View
#from django.contrib.auth.models import User
from django.http import HttpResponse, Http404
from django.views.generic.base import TemplateView
from django.views.decorators.cache import cache_page
from django.contrib.auth.decorators import login_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth import authenticate, login, logout
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework.views import APIView
from rest_framework import authentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.compat import coreapi, coreschema
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework import mixins, generics,renderers, status
from rest_framework.schemas import ManualSchema, SchemaGenerator
from rest_framework.decorators import api_view, renderer_classes
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication

# Redis cache settings
CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)

'''
def download(request, path):
	file_path = os.path.join(settings.MEDIA_ROOT, request['path'])
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/zip")
			response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
			return response
		raise Http404	
'''

class Download(APIView, TemplateView):
	'''
	if user is authenticated
	download option from request
	or return 404
	'''
	template_name = 'download.html'
	authentication_classes = (
			authentication.TokenAuthentication,
			authentication.SessionAuthentication
		)

	def get(self, request, path, format=None):
		file_path = os.path.join(settings.APP_ROOT, path+'/')
		# if path in cache
		app = cache.get(path)
		if app is None:
			app = FasApp.objects.filter(name=path)
			cache.set(path, app, timeout=CACHE_TTL)
		if os.path.exists(file_path) and app:
			ha = hash_dir(file_path)
			tru_path = 'app_upload/apps/'+path+'/'+path+'.'+ha
			shutil.make_archive(tru_path, 'zip', file_path)
			
			with open(tru_path+'.zip', 'rb') as fh:
				response = HttpResponse(fh.read(), content_type="application/zip")
				response['Content-Disposition'] = 'inline; filename='+path
			os.remove(tru_path+'.zip')
			return response
		raise Http404

class Logout(APIView, TemplateView):
        def post(self, request, format='application/json'):
                user = logout(request)
                return Response({
                                'resp':'user logged out',
                        })

class Login(APIView, TemplateView):
	template_name = 'login/index.html'

	if coreapi is not None and coreschema is not None:
		schema = get_man_schema('login')
		print (schema)

	def post(self, request, format='application/json'):
		user = authenticate(username=request.data['username'], password=request.data['password'])
		serializer = FasUserSerializer(data=request.data)
		if serializer.is_valid():
			user = serializer.save()	
		if user is not None:
			login(request, user)
			return Response({
				'resp':'user logged in',
			})
		else:
			return Response({'status':'user invalid'})

class UserCreate(APIView, TemplateView):
	'''
	consumes a POST request and generates a user with
	valid user/pass/email
	'''
	if coreapi is not None and coreschema is not None:
		schema = get_man_schema()

	def post(self, request, format='application/json'):
		serializer = FasUserSerializer(data=request.data, context={'request': request})
		user = None
		if serializer.is_valid():
			user = serializer.save()
#			permission = Permission.objects.get(
#					codename='can_download',
#					name='Can download apps',
#					content_type=ContentType.objects.get_for_app(FasApp),
#				)
#			user.user_permissions.add(permission)
		if user:
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class HomePage(TemplateView):
	'''
	root index will change in future
	'''
	template_name = ('indexa.html')

	def get(request):
		return render(request)

@api_view
@renderer_classes([renderers.CoreJSONRenderer])
def schema_view(request):
	print('danke memes')
	generator = SchemaGenerator(
			title='Fas API',
			url='https://fas.42king.com/api/schema',
		)
	return Response(generator.get_schema())

#@cache_page(CACHE_TTL)
class FasAppList(generics.ListCreateAPIView, TemplateView):
	'''
	query all available FasApps and return the to the user with a json response
	'''
	serializer_class = FasAppSerializer
	authentication_classes = (
			authentication.TokenAuthentication,
			authentication.SessionAuthentication
		)

	def get(self, request, *args, **kwargs):
#		print('USER IS AUTHENTICATED ==', request.user.is_authenticated)
		if request.user.is_authenticated:
			apps = cache.get('fasapps')
			if apps is None:	
				apps = FasApp.objects.all()
				cache.set('fasapps', apps, timeout=CACHE_TTL)
			content = {
				'status': 'request was permitted',
				'apps': serializers.serialize('json', apps),
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

class FasUserList(generics.ListAPIView):
	\'\'\'
	admin list of all users
	\'\'\'
	# TODO : admin only reads
	queryset = FasUser.objects.all()
	serializer_class = FasUserSerializer

#@cache_page(CACHE_TTL)
class FasUserDetail(generics.RetrieveAPIView):
	\'\'\'
	admin detail of all users
	\'\'\'
	# TODO : admin only reads
	queryset = FasUser.objects.all()
	serializer_class = FasUserSerializer
'''
