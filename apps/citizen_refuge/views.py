from django.core.files.storage import FileSystemStorage
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import render
from formtools.wizard.views import SessionWizardView

from common.form_container import FormContainer
from .forms import UserenaSignupForm

KEYS = ['userena']
FORMS = [UserenaSignupForm]
FORM_LIST = zip(KEYS, FORMS)
TEMPLATES = dict(zip(KEYS, ['citizen_refuge/' + k + '.html' for k in KEYS]))

class CitizenRefugeSignupWizard(SessionWizardView):
    form_list = FORM_LIST
    file_storage = FileSystemStorage(location='/tmp/')

    def done(self, form_list, form_dict, **kwargs):
        user = form_dict['userena'].save()
        return HttpResponseRedirect(reverse('userena_signup_complete', kwargs={'username': user.username}))

    def get_template_names(self):
        return [TEMPLATES[self.steps.current]]
