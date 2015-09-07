from django import forms
from multiupload.fields import MultiFileField
from userena.utils import get_profile_model

from .models import Photo

class UserenaEditProfileForm(forms.ModelForm):
    mugshot = forms.ImageField()
    gallery = MultiFileField(
        required=False, min_num=1, max_num=3, max_file_size=1024*1024*5)

    def __init__(self, *args, **kwargs):
        super(UserenaEditProfileForm, self).__init__(*args, **kwargs)
        self.fields['gallery'].initial = [
            i.image for i in self.instance.photo_set.all()]

    def save(self):
        profile = super(UserenaEditProfileForm, self).save()
        profile.mugshot = self.cleaned_data['mugshot']
        profile.save()

        for photo in self.cleaned_data.get('gallery'):
            Photo(image=photo, profile=profile).save()

        return profile

    class Meta:
        model = get_profile_model()
        exclude = ('user',)
