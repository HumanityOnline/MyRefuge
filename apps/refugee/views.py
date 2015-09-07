import os
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect

from userena.forms import SignupForm
from userena.models import UserenaSignup
from userena import signals as userena_signals
from common.helpers import unique_media_path
from .forms import RefugeeSignUpBasic, FamilyMemberFormset, RefugeeSignUpAddress
from .models import Refugee, FamilyMember

KEYS = ['userena', 'basic', 'family', 'address']
FORMS = [SignupForm, RefugeeSignUpBasic, FamilyMemberFormset, RefugeeSignUpAddress]
FORM_LIST = zip(KEYS, FORMS)
TEMPLATES = dict(zip(KEYS, ['refugee/' + k + '.html' for k in KEYS]))

class RefugeeSignupWizard(SessionWizardView):
    form_list = FORM_LIST
    file_storage = FileSystemStorage(location='/tmp/')
    instance_dict = {
        'family': FamilyMember.objects.none()
    }

    def done(self, form_list, form_dict, **kwargs):
        # Create the user
        user = form_dict['userena'].save()
        mugshot = form_dict['basic'].cleaned_data.get('mugshot')
        user.my_profile.mugshot = mugshot
        user.my_profile.save()

        # Concatenate all the information from the forms and save.
        refugee = Refugee(user=user)
        family_members = []
        for key in form_dict:
            if key == 'userena': continue
            form = form_dict[key]
            if key == 'family':
                for dataset in form.cleaned_data:
                    family_members.append(FamilyMember(**dataset))

            else:
                for field in form.cleaned_data.keys():
                    if field == 'mugshot': continue
                    setattr(refugee, field, form.cleaned_data[field])

        refugee.save()
        for member in family_members:
            member.refugee = refugee
            member.save()

        return HttpResponseRedirect(reverse('userena_signup_complete', kwargs={'username': user.username}))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
