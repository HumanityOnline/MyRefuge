from django import forms
from userena.forms import EditProfileForm, SignupForm
from django.forms.models import inlineformset_factory, formset_factory
from address.forms import AddressField

from .models import CitizenRefuge, CitizenSpace, DateRange, SpacePhoto, Application, Launch
from common.helpers import CITIZEN_SPACE_ADDITIONAL_SHORT, APPLICATION_STATUS


class CitizenSignupBasicForm(SignupForm):
    pass

class CitizenRefugeAboutForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    dob = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))
    mugshot = forms.ImageField()
    agree = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(CitizenRefugeAboutForm, self).__init__(*args, **kwargs)
        self.fields['agree'].initial = False
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kwargs):
        # If we're creating an entirely new citizen, there's logic elsewhere
        # to deal with first and last name.
        citizen = super(CitizenRefugeAboutForm, self).save(*args, **kwargs)
        if self.instance.pk is None:
            return citizen

        user = citizen.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return citizen

    class Meta:
        model = CitizenRefuge
        fields = ('dob', 'gender', 'address')

class CitizenRefugePersonalDetailForm(CitizenRefugeAboutForm):
    mugshot = forms.ImageField(required=False)
    agree = forms.BooleanField(required=False)
    address = AddressField(required=False)

class CitizenRefugePersonalImageForm(forms.ModelForm):
    mugshot = forms.ImageField()

    def save(self, *args, **kwargs):
        citizen = super(CitizenRefugePersonalImageForm, self).save(commit=False)
    
        if self.instance.pk is None:
            return citizen

        if self.cleaned_data.get('mugshot'):
            user = citizen.user
            user.my_profile.mugshot = self.cleaned_data.get('mugshot')
            user.my_profile.save()

        return citizen

    class Meta:
        model = CitizenRefuge
        fields = ('mugshot', )


class DateCorrectForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))


from django.forms.widgets import ClearableFileInput

class CustomImageFieldWidget(ClearableFileInput):
    template_with_clear = '%(clear)s <label class="sr-only" for="%(clear_checkbox_id)s">%(clear_checkbox_label)s</label>'

class CitizenRefugeImageForm(forms.Form):
    image = forms.ImageField()


CitizenRefugeSpaceFormset = inlineformset_factory(CitizenRefuge, CitizenSpace,
    fields=('headline', 'address', 'guests', 'full_description', 'additional'),
    extra=0, min_num=1, validate_min=True)

CitizenRefugeDatesFormset = inlineformset_factory(
    CitizenSpace,
    DateRange,
    form=DateCorrectForm,
    fields=('start_date', 'end_date'),
    extra=0, min_num=1, validate_min=True)

SpacePhotoFormset = inlineformset_factory(
    CitizenSpace,
    SpacePhoto,
    fields=('image',),
    extra=0, min_num=1, validate_min=True, max_num=20)


class CitizenRefugeSpaceForm(forms.ModelForm):
    additional = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=CITIZEN_SPACE_ADDITIONAL_SHORT)
    guests = forms.IntegerField(min_value=0)


    class Meta:
        model = CitizenSpace
        fields = ('headline', 'address', 'guests', 'full_description', 'additional')


class CitizenRefugeeSearchForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',), required=False)

    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',), required=False)

    class Meta:
        model = CitizenSpace

        fields = ('address', 'guests')

class ApplicationForm(forms.ModelForm):

    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    guests = forms.IntegerField(initial=1)

    class Meta:
        model = Application

        fields = ('start_date', 'end_date', 'guests', )


class ApplicationUpdateForm(forms.ModelForm):

    story = forms.CharField()

    def clean_story(self):
        val = self.cleaned_data.get('story', '').strip()
        if val == "":
            raise forms.ValidationError('Story must not empty')
        return val

    class Meta:
        model = Application

        fields = ('story', )

class ApplicationMessageForm(forms.ModelForm):

    message = forms.CharField()

    def clean_message(self):
        val = self.cleaned_data.get('message', '').strip()
        if val == "":
            raise forms.ValidationError('Message must not empty')
        return val

    class Meta:
        model = Application

        fields = ('message', )

class ApplicationStatusForm(forms.ModelForm):

    status = forms.ChoiceField(choices=APPLICATION_STATUS)

    class Meta:
        model = Application

        fields = ('status', )


class LaunchForm(forms.ModelForm):
    class Meta:
        model = Launch

        fields = ('start_date', )

