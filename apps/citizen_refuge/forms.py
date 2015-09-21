from django import forms
from userena.forms import EditProfileForm, SignupForm
from django.forms.models import inlineformset_factory

from .models import CitizenRefuge, CitizenSpace, DateRange


class CitizenSignupBasicForm(SignupForm):
    mugshot = forms.ImageField()

    def save(self):
        user = super(CitizenSignupBasicForm, self).save()
        user.my_profile.mugshot = self.cleaned_data['mugshot']
        user.my_profile.save()
        return user


class CitizenRefugeAboutForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    dob = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    def __init__(self, *args, **kwargs):
        super(CitizenRefugeAboutForm, self).__init__(*args, **kwargs)
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


class CitizenRefugeSpaceForm(forms.ModelForm):
    class Meta:
        model = CitizenSpace
        fields = ('headline', 'address', 'guests', 'additional', 'full_description')

CitizenRefugeDatesFormset = inlineformset_factory(
    CitizenSpace,
    DateRange,
    fields=('start_date', 'end_date'),
    extra=1)
