from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from common.forms import UserenaEditProfileForm
from .forms import *
from .models import CitizenRefuge

KEYS = ['userena', 'about',]
FORMS = [CitizenSignupBasicForm, CitizenRefugeAboutForm]
FORM_LIST = zip(KEYS, FORMS)
TEMPLATES = dict(zip(KEYS, ['citizen_refuge/' + k + '.html' for k in KEYS]))

class CitizenRefugeSignupWizard(SessionWizardView):
    form_list = FORM_LIST
    file_storage = FileSystemStorage(location='/tmp/')

    def done(self, form_list, form_dict, **kwargs):
        user = form_dict['userena'].save()
        user.my_profile.type = 'C'
        user.my_profile.save()

        # Create a citizen refuge
        about = form_dict['about']
        citizen = about.save(commit=False)
        citizen.user = user
        citizen.save()

        # Set first and last name on user
        user.first_name = about.cleaned_data.get('first_name')
        user.last_name = about.cleaned_data.get('last_name')
        user.save()

        return HttpResponseRedirect(reverse('userena_signup_complete', kwargs={'username': user.username}))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]


def edit_profile(request):
    forms = {
        'about': CitizenRefugeAboutForm,
        'profile': UserenaEditProfileForm,
        'space': CitizenRefugeSpaceForm,
        'dates': CitizenRefugeDatesFormset,
    }

    instances = {
        'about': request.user.citizenrefuge,
        'profile': request.user.my_profile,
        'space': request.user.citizenrefuge,
        'dates': request.user.citizenrefuge,
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
        formset = None
        if key == 'space':
            formset = CitizenRefugeDatesFormset(request.POST, request.FILES, instance=instances[key])

        if form.is_valid() and (not formset or formset.is_valid()):
            form.save()
            if formset: formset.save()

            return HttpResponseRedirect(
                reverse('userena_profile_edit', kwargs={'username': request.user.username}))

        for k in forms.keys():
            name = k + '_form'
            if key == k:
                ret[name] = form
            elif key == 'dates' and formset:
                ret[name] = formset
            else:
                ret[name] = forms[k](instance=instances[k])

    else:
        for k in forms.keys():
            ret[k + '_form'] = forms[k](instance=instances[k])

    return render(request, 'citizen_refuge/edit_profile.html', ret)
