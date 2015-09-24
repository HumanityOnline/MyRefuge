from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from citizen_refuge.views import (CitizenRefugeDetail as crd, CitizenRefugeDetailUpdate as crdu)
from refugee.views import (RefugeDetail as rd, RefugeDetailUpdate as rdu)

from django.views.generic import TemplateView

# Create your views here.
def home(request):
    return render(request, 'home.html')

def profile_detail(request, username, **kwargs):
    if request.user.username != username:
        raise PermissionDenied

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
