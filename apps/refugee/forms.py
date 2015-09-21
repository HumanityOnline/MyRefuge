from django import forms
from django.forms.models import inlineformset_factory, modelformset_factory
from refugee.models import Refugee, FamilyMember


class RefugeeSignUpBasic(forms.ModelForm):
    first_name = forms.CharField(max_length=255)
    last_name = forms.CharField(max_length=255)
    mugshot = forms.ImageField()
    dob = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    def __init__(self, *args, **kwargs):
        super(RefugeeSignUpBasic, self).__init__(*args, **kwargs)
        print(dir(self.fields['first_name']))

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

FamilyMemberFormset = modelformset_factory(FamilyMember, fields=(
    'name', 'dob', 'gender', 'relationship', 'image',
))
InlineFamilyMemberFormset = inlineformset_factory(Refugee, FamilyMember, fields=(
    'name', 'dob', 'gender', 'relationship', 'image',
), extra=1)

class RefugeeSignUpAddress(forms.ModelForm):
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
