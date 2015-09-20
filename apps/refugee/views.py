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
    instance_dict = {
        'family': FamilyMember.objects.none()
    }

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
    return render(request, 'refugee/profile_detail.html', {'profile': request, 'countries_list': countries})

"""
['DoesNotExist', 'MultipleObjectsReturned', '__class__', '__delattr__', '__dict__', '__doc__', '__eq__', '__format__', '__getattribute__', '__hash__', '__init__', u'__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__setstate__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_base_manager', '_check_column_name_clashes', '_check_field_name_clashes', '_check_fields', '_check_id_field', '_check_index_together', '_check_local_fields', '_check_long_column_names', '_check_m2m_through_same_relationship', '_check_managers', '_check_model', '_check_ordering', '_check_swappable', '_check_unique_together', '_default_manager', '_deferred', '_do_insert', '_do_update', '_get_FIELD_display', '_get_next_or_previous_by_FIELD', '_get_next_or_previous_in_order', '_get_pk_val', '_get_unique_checks', '_meta', '_perform_date_checks', '_perform_unique_checks', '_save_parents', '_save_table', '_set_pk_val', '_state', '_user_cache', 'application', 'check', 'clean', 'clean_fields', 'countries', 'current_address', 'current_address_id', 'date_error_message', 'delete', 'dob', 'familymember_set', 'from_db', 'full_address', 'full_clean', 'gender', 'get_countries_display', 'get_deferred_fields', 'get_gender_display', 'get_next_by_dob', 'get_previous_by_dob', 'hometown', 'id', 'objects', 'pk', 'prepare_database_save', 'refresh_from_db', 'save', 'save_base', 'serializable_value', 'story', 'unique_error_message', 'user', 'user_id', 'validate_unique']

"""