from django import forms
from django.forms.models import (inlineformset_factory, modelformset_factory, BaseInlineFormSet,
    formset_factory)
from refugee.models import Refugee, FamilyMember
from address.forms import AddressField


class RefugeeSignUpBasic(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    mugshot = forms.ImageField()
    dob = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    def __init__(self, *args, **kwargs):
        super(RefugeeSignUpBasic, self).__init__(*args, **kwargs)

    def save(self, *args, **kwargs):
        refugee = super(RefugeeSignUpBasic, self).save(commit=False)
        user = refugee.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return refugee

    class Meta:
        model = Refugee
        fields = ('dob', 'gender',)

class RefugePersonalImageForm(forms.ModelForm):
    mugshot = forms.ImageField()

    def save(self, *args, **kwargs):
        refugee = super(RefugePersonalImageForm, self).save(commit=False)
        if self.cleaned_data.get('mugshot'):
            user = refugee.user
            user.my_profile.mugshot = self.cleaned_data.get('mugshot')
            user.my_profile.save()

        return refugee

    class Meta:
        model = Refugee
        fields = ('mugshot', )

class RefugePersonalDetailForm(RefugeeSignUpBasic):
    mugshot = forms.ImageField(required=False)
    hometown = forms.CharField(max_length=255)
    current_address = AddressField()
    story = forms.CharField()

    class Meta:
        model = Refugee
        fields = ('dob', 'gender', 'hometown', 'current_address', 'story')

class RefugeFamilyImageForm(forms.ModelForm):
    image = forms.ImageField()

    class Meta:
        model = FamilyMember
        fields = ('image',)

class RefugeFamilyDetailForm(forms.ModelForm):
    image = forms.ImageField(required=False)
    dob = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))


    class Meta:
        model = FamilyMember
        fields = ('name', 'dob', 'gender', 'relationship')

class RefugeFamilyCreateForm(RefugeFamilyDetailForm):
    image = forms.ImageField()

    class Meta:
        model = FamilyMember
        fields = ('name', 'dob', 'gender', 'relationship', 'image')

class CustomFamilyMemberFormset(forms.ModelForm):
    dob = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

FamilyMemberFormset = modelformset_factory(FamilyMember,
    form=CustomFamilyMemberFormset,
    fields=(
    'name', 'dob', 'gender', 'relationship', 'image',
))
InlineFamilyMemberFormset = inlineformset_factory(Refugee, FamilyMember, fields=(
    'name', 'dob', 'gender', 'relationship', 'image',
), extra=1)

class RefugeeSignUpAddress(forms.ModelForm):
    full_address = AddressField()

    def __init__(self, *args, **kwargs):
        super(RefugeeSignUpAddress, self).__init__(*args, **kwargs)

        print(dir(self.fields['full_address']))

    class Meta:
        model = Refugee
        fields = ('hometown', 'full_address', 'current_address', 'story')

class RefugeeSignUpPreferences(forms.ModelForm):
    agree = forms.BooleanField()

    def __init__(self, *args, **kwargs):
        super(RefugeeSignUpPreferences, self).__init__(*args, **kwargs)
        self.fields['agree'].initial = False

    def save():
        raise forms.ValidationError('Passwords do not match.')

    class Meta:
        model = Refugee
        fields = ('countries',)

class RefugeeAboutForm(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    dob = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    def __init__(self, *args, **kwargs):
        super(RefugeeAboutForm, self).__init__(*args, **kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name

    def save(self, *args, **kwargs):
        # If we're creating an entirely new refugee, there's logic elsewhere
        # to deal with first and last name.
        refugee = super(RefugeeAboutForm, self).save(*args, **kwargs)
        if self.instance.pk is None:
            return refugee

        user = refugee.user
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return refugee

    class Meta:
        model = Refugee

        fields = ('dob', 'gender', 'full_address', 'hometown', 'current_address', 'story', 
            'countries')
