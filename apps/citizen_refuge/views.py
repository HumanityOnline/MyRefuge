from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from common.forms import UserenaEditProfileForm
from .forms import *
from .models import CitizenRefuge, SpacePhoto, DateRange
from common.helpers import CITIZEN_SPACE_ADDITIONAL_SHORT

KEYS = ['userena', 'about', 'space']
FORMS = [CitizenSignupBasicForm, CitizenRefugeAboutForm, CitizenRefugeSpaceForm]
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

        # Create a citizen space
        space_form = form_dict['space']
        space = space_form.save(commit=False)
        space.citizen = citizen
        space.save()

        sp = SpacePhoto(image=space_form.cleaned_data.get('mugshot'), space=space)
        sp.save()


        dr = DateRange(start_date=space_form.cleaned_data.get('start_date'),
                end_date=space_form.cleaned_data.get('end_date'), space=space)
        dr.save()

        return HttpResponseRedirect(reverse('userena_signup_complete', kwargs={'username': user.username}))

    # def post(self, *args, **kwargs):
    #     if self.steps.current == 'space':
    #         form = SpacePhotoFormset(self.request.POST, self.request.FILES)
    #         print ('form.is_valid()', form.is_valid())
    #         raise Exception('asf')
    #     return super(CitizenRefugeSignupWizard, self).post(*args, **kwargs)


    def get_context_data(self, form, **kwargs):
        context = super(CitizenRefugeSignupWizard, self).get_context_data(form=form, **kwargs)
        if (self.steps.current == 'space'):
            context['spacePhoto'] = {
                'form': SpacePhotoFormset(),
            }

        return context

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

"""


"""

def edit_profile(request):
    forms = {
        'about': CitizenRefugeAboutForm,
        'profile': UserenaEditProfileForm,
        'space': CitizenRefugeSpaceForm,
        #'dates': CitizenRefugeDatesFormset,
    }

    instances = {
        'about': request.user.citizenrefuge,
        'profile': request.user.my_profile,
        'space': request.user.citizenrefuge,
        #'dates': request.user.citizenrefuge,
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

def profile_detail(request):
    citizen = request.user.citizenrefuge
    spaces = citizen.citizenspace_set.all()
    return render(request, 'citizen_refuge/profile_detail.html', {
                      'profile': request.user.my_profile,
                      'citizen': citizen,
                      'space_list': CITIZEN_SPACE_ADDITIONAL_SHORT,
                      'spaces': spaces
                  })
