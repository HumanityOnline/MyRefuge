from django.shortcuts import render
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from citizen_refuge.views import edit_profile as cr
from refugee.views import edit_profile as r

# Create your views here.
def home(request):
    return render(request, 'home.html')

def edit_profile(request, username):
    if request.user.username != username:
        raise PermissionDenied

    # Get the view by profile type
    user_type = request.user.my_profile.type
    if user_type == 'C':
        return cr(request)
    return r(request)
