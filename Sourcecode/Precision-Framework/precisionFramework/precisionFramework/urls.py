"""precisionFramework URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from .views import landing_page, home_files, home, register, change_password

from django.contrib.auth import views as auth_views

urlpatterns = [
    url(r'^pf/', include('precisionFramework.apps.precisionCalculator.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^$', home, name='homeauth'),
    url(r'^home$', home, name='homeauth'),
    url(r'^(?P<filename>(robots.txt)|(humans.txt))$',
        home_files, name='home-files'),
    url(r'^login/$', auth_views.login, name='login'),
    url(r'^logout/$', auth_views.logout, name='logout'),
    url(r'^register/$', register, name='register'),
    url(r'^change-password/$', change_password, name='change_password'),
]
