"""fas URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from fas_backend import views
from django.conf import settings
from django.contrib import admin
from django.views.generic import TemplateView
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url, include
from django.conf.urls.static import static
from django.urls import include, path

urlpatterns = [
	path('/', views.HomePage.as_view()),
	path('', include('fas_backend.urls')),
	path('home', views.HomePage.as_view(), name='index'),
#	url(r'^accounts', include('registration.backends.simple.urls')),
	path('o/', include('oauth2_provider.urls', namespace='oauth2_provider'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

#urlpatterns = format_suffix_patterns(urlpatterns)
