from django import forms
from userena.forms import EditProfileForm, SignupForm
from django.forms.models import inlineformset_factory, formset_factory

from .models import CitizenRefuge, CitizenSpace, DateRange, SpacePhoto
from common.helpers import CITIZEN_SPACE_ADDITIONAL_SHORT


class CitizenSignupBasicForm(SignupForm):
    # mugshot = forms.ImageField()

    # def save(self):
    #     user = super(CitizenSignupBasicForm, self).save()
    #     user.my_profile.mugshot = self.cleaned_data['mugshot']
    #     user.my_profile.save()
    #     return user
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

CitizenRefugeDatesFormset = inlineformset_factory(
    CitizenSpace,
    DateRange,
    fields=('start_date', 'end_date'),
    extra=1)

SpacePhotoFormset = inlineformset_factory(CitizenSpace, SpacePhoto, fields=(
    'image',
))


class CitizenRefugeSpaceForm(forms.ModelForm):
    additional = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=CITIZEN_SPACE_ADDITIONAL_SHORT)

    mugshot = forms.ImageField()
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))


    def __init__(self, *args, **kwargs):
        super(CitizenRefugeSpaceForm, self).__init__(*args, **kwargs)

    class Meta:
        model = CitizenSpace
        fields = ('headline', 'address', 'guests', 'full_description', 'additional')
