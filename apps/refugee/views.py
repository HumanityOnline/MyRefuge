import os
from formtools.wizard.views import SessionWizardView
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django_countries import countries

from userena.forms import SignupForm
from userena.models import UserenaSignup
from userena import signals as userena_signals
from common.forms import UserenaEditProfileForm
from .forms import *
from .models import Refugee, FamilyMember


KEYS = ['userena', 'basic', 'family', 'address', 'country']
FORMS = [SignupForm, RefugeeSignUpBasic, FamilyMemberFormset, RefugeeSignUpAddress, RefugeeSignUpPreferences]
FORM_LIST = zip(KEYS, FORMS)
TEMPLATES = dict(zip(KEYS, ['refugee/' + k + '.html' for k in KEYS]))

def skip_family(wizard):
    """Return true if user opts to pay by credit card"""
    cleaned_data = wizard.storage.get_step_data('basic') or {'skip_family': '0'}
    return cleaned_data.get('skip_family', '0') != '1'

class RefugeeSignupWizard(SessionWizardView):
    form_list = FORM_LIST
    file_storage = FileSystemStorage(location='/tmp/')

    condition_dict = {
        'family': skip_family
    }

    def __init__(self, *args, **kwargs):
        super(RefugeeSignupWizard, self).__init__(*args, **kwargs)

    def done(self, form_list, form_dict, **kwargs):
        # Create the user
        user = form_dict['userena'].save()
        mugshot = form_dict['basic'].cleaned_data.get('mugshot')
        user.my_profile.mugshot = mugshot
        user.my_profile.type = 'R'
        user.my_profile.save()

        # Set first and last name on user
        basic = form_dict['basic']
        user.first_name = basic.cleaned_data.get('first_name')
        user.last_name = basic.cleaned_data.get('last_name')
        user.save()

        # Concatenate all the information from the forms and save.
        refugee = Refugee(user=user)
        family_members = []
        for key in form_dict:
            if key == 'userena': continue
            form = form_dict[key]
            if key == 'family':
                for dataset in form.cleaned_data:
                    if len(dataset):
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


def edit_profile(request):
    forms = {
        'about': RefugeeAboutForm,
        'profile': UserenaEditProfileForm,
        'family': InlineFamilyMemberFormset,
        # 'dates': CitizenRefugeDatesFormset,
    }

    instances = {
        'about': request.user.refugee,
        'profile': request.user.my_profile,
        'family': request.user.refugee,
    #     'dates': request.user.citizenrefuge,
    }

    ret = {}
    if request.method == 'POST':
        form = None
        for key in forms.keys():
            if key + '-button' in request.POST:
                form = forms[key]
                break

        if form is None:
            raise Exception

        form = form(request.POST, request.FILES, instance=instances[key])

        if form.is_valid():
            form.save()
            return HttpResponseRedirect(
                reverse('userena_profile_edit', kwargs={'username': request.user.username}))

        for k in forms.keys():
            name = k + '_form'
            if key == k:
                ret[name] = form
            else:
                ret[name] = forms[k](instance=instances[k])

    else:
        for k in forms.keys():
            ret[k + '_form'] = forms[k](instance=instances[k])

    return render(request, 'refugee/edit_profile.html', ret)


def profile_detail(request):
    request.family_members = request.user.refugee.familymember_set.all()
    return render(request, 'refugee/profile_detail.html', {'profile': request.user.my_profile,
                                                           'countries_list': countries})

