from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, UpdateView
from formtools.wizard.views import SessionWizardView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from common.forms import UserenaEditProfileForm
from .forms import *
from .models import (CitizenRefuge, SpacePhoto, DateRange, CitizenSpace, CitizenSpaceManager,
                        Application)
from common.helpers import CITIZEN_SPACE_ADDITIONAL_SHORT

KEYS = ['userena', 'about', 'space']
FORMS = [CitizenSignupBasicForm, CitizenRefugeAboutForm, CitizenRefugeSpaceForm]
FORM_LIST = zip(KEYS, FORMS)
TEMPLATES = dict(zip(KEYS, ['citizen_refuge/' + k + '.html' for k in KEYS]))

class CitizenRefugeSignupWizard(SessionWizardView):
    form_list = FORM_LIST
    file_storage = FileSystemStorage(location='/tmp/')
    date_form = None
    image_form = None

    def __init__(self, **kwargs):
        super(CitizenRefugeSignupWizard, self).__init__(**kwargs)
        self.date_form = CitizenRefugeDatesFormset()
        self.image_form = SpacePhotoFormset()


    def done(self, form_list, form_dict, **kwargs):

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

        for dataset in self.image_form.cleaned_data:
            if len(dataset):
                sp = SpacePhoto(image=dataset.get('image'), space=space)
                sp.save()

        for dataset in self.date_form.cleaned_data:
            if len(dataset):
                daterage = DateRange(start_date=dataset.get('start_date'),
                    end_date=dataset.get('end_date'), space=space)
                daterage.save()

        return HttpResponseRedirect(reverse('userena_signup_complete', kwargs={'username': user.username}))

    def post(self, *args, **kwargs):
        if self.request.POST.get('citizen_refuge_signup_wizard-current_step', None) == 'space':
            self.date_form = CitizenRefugeDatesFormset(self.request.POST, self.request.FILES)
            self.image_form = SpacePhotoFormset(self.request.POST, self.request.FILES)
            print('self.image_form.is_valid()', self.image_form.is_valid())
            if not self.date_form.is_valid() or not self.image_form.is_valid():
                return self.render(self.get_form(data=self.request.POST, files=self.request.FILES))

        return super(CitizenRefugeSignupWizard, self).post(*args, **kwargs)


    def get_context_data(self, form, **kwargs):
        context = super(CitizenRefugeSignupWizard, self).get_context_data(form=form, **kwargs)
        if (self.steps.current == 'space'):
            context['date_form'] = self.date_form
            context['image_form'] = self.image_form

        return context

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]

class CitizenRefugeSpaceList(ListView):
    model = CitizenSpace
    paginate_by = 10

    def get_queryset(self):
        return self.model._default_manager.all()

class CitizenRefugeMySpaceList(ListView):
    model = CitizenSpace
    paginate_by = 10

    def get_queryset(self):
        if hasattr(self.request.user, 'citizenrefuge'):
            return self.model._default_manager.filter(citizen=self.request.user.citizenrefuge)

        return self.model._default_manager.none()


class CitizenRefugeSpaceDetail(UpdateView):
    model = CitizenSpace

    form_class = ApplicationForm

    def is_space_booked(self):
        booker = Application.objects.filter(
                    refugee__user=self.request.user,
                    space=self.object).first()

        return True if booker else False

    @property
    def can_update(self):
        return not self.request.user.is_anonymous() and\
                    self.request.user.my_profile.type == 'R' and\
                    not self.is_space_booked()

    def form_valid(self, form):

        if self.can_update:
            bookee = Application(**form.cleaned_data)
            bookee.refugee = self.request.user.refugee
            bookee.space = self.object
            bookee.status = 'P'
            bookee.save()

            return HttpResponseRedirect(
                    reverse('refuge_space_application', kwargs={'pk': bookee.pk}))

        return self.render_to_response(self.get_context_data(
                        form=form,
                    ))

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = None
        if self.can_update:
            form = self.get_form(self.get_form_class())

        return self.render_to_response(self.get_context_data(form=form))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form(self.get_form_class())
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

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



class CitizenRefugeSearchView(FormView):

    template_name = 'citizen_refuge/search.html'
    form_class = CitizenRefugeeSearchForm

    def form_valid(self, form):
        
        spaces = CitizenSpace.objects.search(
                    address=form.cleaned_data.get('address'),
                    date_range=(form.cleaned_data.get('start_date'),
                                    form.cleaned_data.get('end_date')),
                    guests=form.cleaned_data.get('guests'))

        return self.render_to_response(self.get_context_data(
                        form=form,
                        spaces=spaces,
                        searched=True,
                    ))


class CitizenRefugeSpaceApplication(UpdateView):
    model = Application

    form_class = ApplicationUpdateForm

    @property
    def can_update(self):
        return self.object.refugee.user == self.request.user

    def form_valid(self, form):

        if self.can_update:

            bookee = form.save(commit=False)
            bookee.story = form.cleaned_data.get('story')
            bookee.save()

            return HttpResponseRedirect(
                    reverse('refuge_space_application', kwargs={'pk': bookee.pk}))

        return self.render_to_response(self.get_context_data(
                        form=form,
                    ))

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeSpaceApplication, self).get_context_data(**kwargs)
        context['can_update'] = self.can_update
        return context
