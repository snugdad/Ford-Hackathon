from fas_backend import views
from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from django.urls import include
from django.contrib import admin
from django.conf import settings
from django.views.static import serve

from rest_framework.schemas import get_schema_view

from rest_framework.authtoken import views as auth

urlpatterns = [
	# list all apps
        url(r'^api/apps', views.FasAppList.as_view()),
	# TODO : change to admin-only permissions
#        url(r'^api/users/$', views.FasUserList.as_view()),
#        url(r'^api/users/(?P<pk>[0-9]+)/$', views.FasUserDetail.as_view()),
        url(r'^api/admin', admin.site.urls),
        url(r'^api/schema', get_schema_view('Fas API')),#get_schema_view('Fas API')),
        url(r'^api/download/(?P<path>.*)$', views.Download.as_view()),
	url(r'^api/token', views.CreateFasAuthToken.as_view()),
	# if not user, create user
	url(r'^api/register', views.UserCreate.as_view()),
	# TODO : user login
	url(r'^api/login', views.Login.as_view()),
	url(r'^api/logout', views.Logout.as_view()),
	# ?TODO? : user logout
	# TODO : etc
]

urlpatterns = format_suffix_patterns(urlpatterns)

