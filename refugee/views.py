import os
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from userena.forms import SignupForm
from .forms import RefugeeSignUpBasic, FamilyMemberFormset, RefugeeSignUpAddress

# Create your views here.
class RefugeeSignupWizard(SessionWizardView):
    form_list = [SignupForm, RefugeeSignUpBasic, FamilyMemberFormset, RefugeeSignUpAddress]
    file_storage = FileSystemStorage(location=os.path.join(settings.MEDIA_ROOT, 'refugee'))
    def done(self, form_list, form_dict, **kwargs):
        form_list[0].save()
        print form_dict
