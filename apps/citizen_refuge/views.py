from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
from formtools.wizard.views import SessionWizardView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from common.forms import UserenaEditProfileForm
from .forms import *
from .models import CitizenRefuge, SpacePhoto, DateRange, CitizenSpace
from common.helpers import CITIZEN_SPACE_ADDITIONAL_SHORT

KEYS = ['userena', 'about', 'space']
FORMS = [CitizenSignupBasicForm, CitizenRefugeAboutForm, CitizenRefugeSpaceCombineForm]
FORM_LIST = zip(KEYS, FORMS)
TEMPLATES = dict(zip(KEYS, ['citizen_refuge/' + k + '.html' for k in KEYS]))

class CitizenRefugeSignupWizard(SessionWizardView):
    form_list = FORM_LIST
    file_storage = FileSystemStorage(location='/tmp/')

    # instance_dict = {
    #     'space': CitizenSpace.objects.none()
    # }
    """
    ('space_form', ['__bool__', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__html__', '__init__', '__iter__', '__len__', '__module__', '__new__', '__nonzero__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_construct_form', '_errors', '_existing_object', '_get_to_python', '_non_form_errors', '_pk_field', '_should_delete_form', u'absolute_max', 'add_fields', 'add_prefix', 'as_p', 'as_table', 'as_ul', 'auto_id', u'can_delete', u'can_order', 'clean', 'cleaned_data', 'data', 'deleted_forms', 'empty_form', 'error_class', 'errors', u'extra', 'extra_forms', 'files', 'fk', u'form', 'forms', 'full_clean', 'get_date_error_message', 'get_default_prefix', 'get_form_error', 'get_queryset', 'get_unique_error_message', 'has_changed', 'initial', 'initial_extra', 'initial_form_count', 'initial_forms', 'instance', 'is_bound', 'is_multipart', 'is_valid', 'management_form', u'max_num', 'media', u'min_num', 'model', 'non_form_errors', 'ordered_forms', 'prefix', 'queryset', 'save', 'save_as_new', 'save_existing', 'save_existing_objects', 'save_new', 'save_new_objects', 'total_error_count', 'total_form_count', u'validate_max', u'validate_min', 'validate_unique'])
, 'total_form_count', u'validate_max', u'validate_min', 'validate_unique'])

('space_form', <MultiValueDict: {u'space-0-headline': [u'DD'], u'space-0-start_date': [u'01/02/2114'], u'space-0-end_date_[month]': [u'04'], u'space-1-end_date_[month]': [u'07'], u'space-0-additional': [u'3', u'4'], u'space-MAX_NUM_FORMS': [u'1000'], u'space-1-start_date_[month]': [u'02'], u'space-0-start_date_[year]': [u'2114'], u'space-0-full_description': [u'DSFSD'], u'space-0-guests': [u'2'], u'space-0-end_date': [u'02/04/2113'], u'space-1-end_date_[year]': [u'2102'], u'space-1-start_date_[year]': [u'2101'], u'space-1-start_date': [u'16/02/2101'], u'space-1-end_date_[day]': [u'12'], u'space-0-start_date_[month]': [u'02'], u'space-1-start_date_[day]': [u'16'], u'space-TOTAL_FORMS': [u'2'], u'space-0-end_date_[day]': [u'02'], u'space-0-start_date_[day]': [u'01'], u'space-0-end_date_[year]': [u'2113'], u'space-MIN_NUM_FORMS': [u'1'], u'citizen_refuge_signup_wizard-current_step': [u'space'], u'space-INITIAL_FORMS': [u'0'], u'space-0-address': [u'FFF'], u'csrfmiddlewaretoken': [u'dxUEOxEyFFBRnKVuJcBmyNySwfPoBQqx'], u'space-1-end_date': [u'12/07/2102']}>)


    """
    def done(self, form_list, form_dict, **kwargs):
        space_form = form_dict['space']
        
        print('space_form', space_form.is_valid())
        dr = DateRange(start_date=space_form.cleaned_data.get('start_date'),
                end_date=space_form.cleaned_data.get('end_date'), space=space)

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



        raise Exception
        user = form_dict['userena'].save()
        user.my_profile.type = 'C'
        mugshot = form_dict['about'].cleaned_data.get('mugshot')
        user.my_profile.mugshot = mugshot
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


    # def get_context_data(self, form, **kwargs):
    #     context = super(CitizenRefugeSignupWizard, self).get_context_data(form=form, **kwargs)
    #     if (self.steps.current == 'space'):
    #         context['spacePhoto'] = {
    #             'form': SpacePhotoFormset(),
    #         }

    #     return context

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

class CitizenRefugeSpaceList(ListView):
    model = CitizenSpace

    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super(CitizenRefugeSpaceList, self).dispatch(request, *args, **kwargs)

    def get_queryset(self):
        return self.model._default_manager.filter(citizen=self.request.user.citizenrefuge)

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeSpaceList, self).get_context_data(**kwargs)
        context['space_list'] = CITIZEN_SPACE_ADDITIONAL_SHORT
        return context


class CitizenRefugeSpaceDetail(DetailView):
    model = CitizenSpace

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeSpaceDetail, self).get_context_data(**kwargs)
        context['space_list'] = CITIZEN_SPACE_ADDITIONAL_SHORT
        context['space_list_icon'] = {
            '1': 'wifi',
            '2': 'spoon',
            '3': 'life-saver',
            '4': 'group',

        }
        return context


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
