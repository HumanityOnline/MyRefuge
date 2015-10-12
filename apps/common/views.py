from django.shortcuts import render
from django.http import HttpResponseForbidden, HttpResponse
from django.core.exceptions import PermissionDenied

from citizen_refuge.views import (CitizenRefugeDetail as crd, CitizenRefugeDetailUpdate as crdu)
from refugee.views import (RefugeDetail as rd, RefugeDetailUpdate as rdu)

from django.views.generic import DetailView, TemplateView
from django.conf import settings
from .models import Page
# Create your views here.
def home(request):
    return render(request, 'home.html')

def profile_detail(request, username, **kwargs):
    if request.user.username != username:
        raise PermissionDenied

    #print ('settings.CSRF_COOKIE_NAME', settings.CSRF_COOKIE_NAME)
    #print ('settings.CSRF_HEADER_NAME', settings.CSRF_HEADER_NAME)

    # Get the view by profile type
    user_type = request.user.my_profile.type
    if user_type == 'C':
        return crd.as_view()(request, **kwargs)
    return rd.as_view()(request, **kwargs)

def profile_update(request, username, **kwargs):
    if request.user.username != username:
        raise PermissionDenied

    # Get the view by profile type
    user_type = request.user.my_profile.type
    if user_type == 'C':
        return crdu.as_view()(request, **kwargs)
    return rdu.as_view()(request, **kwargs)


class PageView(DetailView):
    model = Page
    template_name = 'common/page.html'

# for now

class HelpView(TemplateView):
    template_name = 'common/help.html'


def security_scan_file(request):
    content = '6b53be211839d9ea4fc48579a179214d9a503fa36a122f8eb61fa77767d195a2'
    return HttpResponse(content)