from django import forms
from userena.forms import EditProfileForm, SignupForm
from django.forms.models import inlineformset_factory, formset_factory
from address.forms import AddressField

from .models import CitizenRefuge, CitizenSpace, DateRange, SpacePhoto, Application
from common.helpers import CITIZEN_SPACE_ADDITIONAL_SHORT


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

class DateCorrectForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

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

    guests = forms.IntegerField()

    class Meta:
        model = Application

        fields = ('start_date', 'end_date', 'guests', )


class ApplicationUpdateForm(forms.ModelForm):

    story = forms.CharField()

    class Meta:
        model = Application

        fields = ('story', )

class ApplicationMessageForm(forms.ModelForm):

    message = forms.CharField()

    class Meta:
        model = Application

        fields = ('message', )