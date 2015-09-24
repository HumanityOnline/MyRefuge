from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView, FormView, UpdateView, TemplateView
from django.views.generic.edit import ProcessFormView
from formtools.wizard.views import SessionWizardView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required, permission_required

from common.forms import UserenaEditProfileForm
from .forms import *
from .models import (CitizenRefuge, SpacePhoto, DateRange, CitizenSpace, CitizenSpaceManager,
                        Application, Message)
from common.helpers import CITIZEN_SPACE_ADDITIONAL_SHORT, APPLICATION_STATUS, GENDER

from django.http import JsonResponse

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
        if self.request.user.my_profile.type == 'C':
            return self.model._default_manager.filter(citizen=self.request.user.citizenrefuge)

        return self.model._default_manager.none()


class CitizenRefugeSpaceDetail(UpdateView):
    model = CitizenSpace

    form_class = ApplicationForm

    def is_space_booked(self):
        application = Application.objects.filter(
                    refugee__user=self.request.user,
                    space=self.object).first()

        return True if application else False

    @property
    def can_update(self):
        return not self.request.user.is_anonymous() and\
                    self.request.user.my_profile.type == 'R' and\
                    not self.is_space_booked()

    def form_valid(self, form):

        if self.can_update:
            application = Application(**form.cleaned_data)
            application.refugee = self.request.user.refugee
            application.space = self.object
            application.status = 'P'
            application.save()

            return HttpResponseRedirect(
                    reverse('refuge_space_application', kwargs={'pk': application.pk}))

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


class CitizenRefugeSearchView(TemplateView):
    template_name = 'citizen_refuge/search.html'

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeSearchView, self).get_context_data(**kwargs)
        context['form'] = CitizenRefugeeSearchForm()
        return context


class CitizenRefugeSearchResultView(FormView):
    template_name = 'citizen_refuge/search-result.html'
    form_class = CitizenRefugeeSearchForm

    def get(self, request, *args, **kwargs):
        form_class = self.get_form_class()
        kwargs.update({
            'data': self.request.GET,
            'files': self.request.FILES,
        })
        form = form_class(**kwargs)

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        
        spaces = CitizenSpace.objects.search(
                    address=form.cleaned_data.get('address'),
                    date_range=(form.cleaned_data.get('start_date'),
                                    form.cleaned_data.get('end_date')),
                    guests=form.cleaned_data.get('guests'))

        return self.render_to_response(self.get_context_data(
                        form=form,
                        spaces=spaces,
                    ))

class CitizenRefugeSpaceApplication(UpdateView):
    model = Application

    form_class = ApplicationUpdateForm

    @property
    def can_update(self):
        return self.object.refugee.user == self.request.user

    @property
    def can_message(self):
        return self.object.refugee.user == self.request.user or\
                self.object.space.citizen.user == self.request.user


    def form_valid(self, form):

        if self.can_update:

            application = form.save(commit=False)
            application.story = form.cleaned_data.get('story')
            application.save()

            return HttpResponseRedirect(
                    reverse('refuge_space_application', kwargs={'pk': application.pk}))

        return self.render_to_response(self.get_context_data(
                        form=form,
                    ))

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeSpaceApplication, self).get_context_data(**kwargs)
        if self.can_message:
            context['message_form'] = ApplicationMessageForm()
            context['messages'] = Message.objects.get_application_conversation(self.object)

        context['can_update'] = self.can_update

        return context

class CitizenRefugeSpaceMessage(UpdateView):
    model = Application

    form_class = ApplicationMessageForm

    @property
    def can_update(self):
        return self.object.refugee.user == self.request.user or\
                self.object.space.citizen.user == self.request.user

    def form_valid(self, form):
        if self.can_update:
            Message.objects.send_message(self.request.user, self.object, form.cleaned_data.get('message'))

        return HttpResponseRedirect(
                    reverse('refuge_space_application', kwargs={'pk': self.object.pk}))

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeSpaceMessage, self).get_context_data(**kwargs)
        if self.can_update:
            context['message_form'] = kwargs.get('form')
            context['messages'] = Message.objects.get_application_conversation(self.object)
        return context

class CitizenRefugeSpaceStatus(UpdateView):
    model = Application

    form_class = ApplicationStatusForm

    @property
    def can_update(self):
        return self.object.space.citizen.user == self.request.user

    def form_invalid(self, form):
        return JsonResponse({'success': False})

    def form_valid(self, form):
        if self.can_update:
            application = form.save(commit=False)
            application.status = form.cleaned_data.get('status')
            application.save()
            return JsonResponse({'success': True})

        return JsonResponse({'success': False})


class CitizenRefugeSpaceApplicationList(ListView):
    model = Application
    paginate_by = 10
    template_name = 'citizen_refuge/application_requests.html'

    def get_queryset(self):
        print('self.kwargs', self.kwargs['status'])
        if self.request.user.my_profile.type == 'C':
            if self.kwargs.get('status') == 'pending':
                objects = self.model._default_manager.filter(
                            status='P',
                            space__citizen__user=self.request.user).all()
            elif self.kwargs.get('status') == 'declined':
                objects = self.model._default_manager.filter(
                            status='D',
                            space__citizen__user=self.request.user).all()
            else:
                objects = self.model._default_manager.filter(
                            space__citizen__user=self.request.user).all()

            return objects

        return self.model._default_manager.none()

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeSpaceApplicationList, self).get_context_data(**kwargs)
        context['status'] = self.kwargs.get('status')
        context['status_list'] = APPLICATION_STATUS

        return context

class CitizenRefugeDetail(TemplateView):
    template_name = 'citizen_refuge/profile_detail.html'

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeDetail, self).get_context_data(**kwargs)
        context['profile'] = self.request.user.my_profile
        context['citizen'] = self.request.user.citizenrefuge
        context['gender_list'] = GENDER[1:]
        return context

class CitizenRefugeDetailUpdate(ProcessFormView):
    template_name = 'citizen_refuge/profile_detail.html'

    def post(self, request, *args, **kwargs):

        profile_form = CitizenRefugePersonalDetailForm(self.request.POST, instance=self.request.user.citizenrefuge)
        if profile_form.is_valid():
            return self.form_valid(profile_form)
        else:
            return self.form_invalid(profile_form)

    def form_valid(self, profile_form):
        profile_form.save()
        return JsonResponse({'success': True})

    def form_invalid(self, profile_form):
        return JsonResponse({'success': False,'errors': profile_form.errors})

    def get_context_data(self, **kwargs):
        context = super(CitizenRefugeDetailUpdate, self).get_context_data(**kwargs)
        return context

