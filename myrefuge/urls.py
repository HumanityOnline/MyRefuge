"""myrefuge URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from refugee.views import RefugeeSignupWizard
from citizen_refuge.views import CitizenRefugeSignupWizard

urlpatterns = [
    url(r'^$', 'common.views.home'),
    url(r'^accounts/(?P<username>[\.\w-]+)/edit/$',
        'common.views.edit_profile',
        name='userena_profile_edit'),
    
    url(r'^accounts?/(?P<username>(?!signout|signup|signin)[\@\.\w-]+)/$',
       'common.views.profile_detail',
       name='userena_profile_detail'),
    
    url(r'^accounts/', include('userena.urls')),
    url(r'^refugee/', RefugeeSignupWizard.as_view(), name='refugee'),
    url(r'^refuge-provider/', CitizenRefugeSignupWizard.as_view(), name='refuge_provider'),
    url(r'^admin/', include(admin.site.urls)),
]
