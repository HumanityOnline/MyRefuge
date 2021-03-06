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
from common.views import HelpView
from refugee.views import RefugeeSignupWizard, RefugeSpaceWishList
from citizen_refuge.views import (CitizenRefugeSignupWizard, CitizenRefugeSpaceList,
                                  CitizenRefugeSpaceDetail, CitizenRefugeSearchView,
                                  CitizenRefugeSpaceApplication, CitizenRefugeMySpaceList,
                                  CitizenRefugeSpaceMessage, CitizenRefugeSpaceApplicationList,
                                  CitizenRefugeSpaceStatus, CitizenRefugeSearchResultView,
                                  CitizenRefugeSpaceEdit, CitizenRefugeSpaceCreate,
                                  LaunchView, LaunchUpdateView)

urlpatterns = [
    url(r'^', include('favicon.urls')),
    url(r'^home/$', 'common.views.home', name='home'),
    url(r'^a7f30687a7805b52c1e8a674434d609626869b13de8a58b7a6f9fc01c0c11db1.txt$', 'common.views.security_scan_file',
        name='security_scan_file'), # support for security scanning
    url(r'^$', CitizenRefugeSearchView.as_view(), name='search_home'),
    url(r'^search/', CitizenRefugeSearchResultView.as_view(), name='search'),
    url(r'^launch/update/$', LaunchUpdateView.as_view(), name='launch_update'),
    url(r'^launch/', LaunchView.as_view(), name='launch'),


    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\@\.\w-]+)/update/'+
                        '(?P<type>(personal|family-delete|family))?/',
        'common.views.profile_update',
        name='profile_update'),
    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\@\.\w-]+)/$',
        'common.views.profile_detail',
        name='userena_profile_detail'),
    
    url(r'^accounts/', include('userena.urls')),
    url(r'^refugee/', RefugeeSignupWizard.as_view(), name='refugee'),
    url(r'^refuge-provider/', CitizenRefugeSignupWizard.as_view(), name='refuge_provider'),
    url(r'^admin/', include(admin.site.urls)),

    url(r'^refuge-spaces/me/', CitizenRefugeMySpaceList.as_view(), name='refuge_myspace_list'),
    url(r'^refuge-spaces/create/', CitizenRefugeSpaceCreate.as_view(),
        name='refuge_myspace_create'),
    url(r'^refuge-spaces/(?P<pk>[\.\w-]+)/edit/', CitizenRefugeSpaceEdit.as_view(),
        name='refuge_space_edit'),
    url(r'^refuge-spaces/(?P<pk>[\.\w-]+)/', CitizenRefugeSpaceDetail.as_view(),
        name='refuge_space_detail'),
    url(r'^refuge-spaces/', CitizenRefugeSpaceList.as_view(), name='refuge_space_list'),

    url(r'^bookings/(?P<pk>[\.\w-]+)/compose/', CitizenRefugeSpaceMessage.as_view(),
        name='refuge_space_application_compose'),
    url(r'^bookings/(?P<pk>[\.\w-]+)/update/', CitizenRefugeSpaceStatus.as_view(),
        name='refuge_space_application_update'),
    url(r'^bookings/(?P<pk>(?!all|pending|declined)[\.\w-]+)/',
        CitizenRefugeSpaceApplication.as_view(), name='refuge_space_application'),
    url(r'^bookings/(?P<status>(all|pending|declined))?',
        CitizenRefugeSpaceApplicationList.as_view(), name='refuge_space_application_list'),

    url(r'^wish-list/', RefugeSpaceWishList.as_view(), name='refuge_wish_list'),

    url(r'^help/', HelpView.as_view(), name='myrefuge_help'),


]
