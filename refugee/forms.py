from django import forms
from django.forms.models import modelformset_factory
from refugee.models import Refugee, FamilyMember


class RefugeeSignUpBasic(forms.ModelForm):
    mugshot = forms.ImageField()

    class Meta:
        model = Refugee
        fields = ('name', 'dob', 'gender',)

FamilyMemberFormset = modelformset_factory(FamilyMember, fields=(
    'name', 'dob', 'gender', 'relationship',
))

class RefugeeSignUpAddress(forms.ModelForm):
    class Meta:
        model = Refugee
        fields = ('hometown', 'current_address', 'story')

class RefugeeSignUpPreferences(forms.ModelForm):
    class Meta:
        model = Refugee
        fields = ('countries',)
