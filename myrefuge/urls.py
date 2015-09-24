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
from refugee.views import RefugeeSignupWizard, RefugeSpaceWishList
from citizen_refuge.views import (CitizenRefugeSignupWizard, CitizenRefugeSpaceList,
                                  CitizenRefugeSpaceDetail, CitizenRefugeSearchView,
                                  CitizenRefugeSpaceApplication, CitizenRefugeMySpaceList,
                                  CitizenRefugeSpaceMessage, CitizenRefugeSpaceApplicationList,
                                  CitizenRefugeSpaceStatus, CitizenRefugeSearchResultView)

urlpatterns = [
    url(r'^home/$', 'common.views.home', name='home'),
    url(r'^$', CitizenRefugeSearchView.as_view(), name='search_home'),
    url(r'^search/', CitizenRefugeSearchResultView.as_view(), name='search'),

    url(r'^accounts/(?P<username>(?!signout|signup|signin)[\@\.\w-]+)/update/'+
                        '(?P<type>(personal|family))?',
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


]
