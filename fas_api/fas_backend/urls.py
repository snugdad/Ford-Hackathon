from fas_backend import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include, path
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from rest_framework.schemas import get_schema_view

from rest_framework.authtoken import views as auth

urlpatterns = [
	# list all apps
        path('api/apps', views.FasAppList.as_view()),
	# TODO : change to admin-only permissions
#        path('api/users/$', views.FasUserList.as_view()),
#        path('api/users/(?P<pk>[0-9]+)/$', views.FasUserDetail.as_view()),
        path('api/admin', admin.site.urls),
        path('api/schema', get_schema_view('Fas API')),#get_schema_view('Fas API')),
        path('api/download/<str:path>', views.Download.as_view()),
	path('api/upload', views.Upload.as_view()),
	path('api/token', views.CreateFasAuthToken.as_view()),
	# if not user, create user
	path('api/register', views.UserCreate.as_view()),
	# TODO : user login
	path('api/login', views.Login.as_view(), name='login/index'),
	path('api/logout', views.Logout.as_view()),
	# ?TODO? : user logout
	# TODO : etc
]

#pathpatterns = format_suffix_patterns(urlpatterns)
