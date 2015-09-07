from django import forms
from multiupload.fields import MultiFileField
from userena.forms import SignupForm

class UserenaSignupForm(SignupForm):
    mugshot = forms.ImageField()
    gallery = MultiFileField(min_num=1, max_num=3, max_file_size=1024*1024*5)

    def save(self):
        user = super(UserenaSignupForm, self).save()
        user.my_profile.mugshot = self.cleaned_data['mugshot']
        user.my_profile.save()
        return user

# class CitizenRefugeSpaceForm(forms.ModelForm):

