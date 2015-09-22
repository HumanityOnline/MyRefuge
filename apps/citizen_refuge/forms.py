from django import forms
from userena.forms import EditProfileForm, SignupForm
from django.forms.models import inlineformset_factory, formset_factory
from address.forms import AddressField

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

class RequiredFormSet(forms.models.BaseInlineFormSet):
    def __init__(self, *args, **kwargs):
        super(RequiredFormSet, self).__init__(*args, **kwargs)

    def validate_unique(self):
        pass

    """
    ('self.form', [u'Meta', '__class__', '__delattr__', '__dict__', '__doc__', '__format__', '__getattribute__', '__getitem__', '__hash__', '__html__', '__init__', '__iter__', '__module__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__unicode__', '__weakref__', '_clean_fields', '_clean_form', '_get_validation_exclusions', '_html_output', '_meta', '_post_clean', '_raw_value', '_update_errors', 'add_error', 'add_initial_prefix', 'add_prefix', 'as_p', 'as_table', 'as_ul', 'base_fields', 'changed_data', 'clean', u'declared_fields', 'errors', 'full_clean', 'has_changed', 'has_error', 'hidden_fields', 'is_multipart', 'is_valid', 'media', 'non_field_errors', 'save', 'validate_unique', 'visible_fields'])

    """

    form_counter = 0

    def is_valid(self):
        if len(self.forms) > 1:
            if self.forms[0].errors:
                pass
            else:
                # print('_>>>>>>>>>>>>>>>>>>>>>>>>.')
                # setattr(self, '_errors', {})
                return True

        return super(RequiredFormSet, self).is_valid()

# class CitizenRefugeSpaceForm2(forms.ModelForm):
#     additional = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
#                                          choices=CITIZEN_SPACE_ADDITIONAL_SHORT)

#     mugshot = forms.ImageField()
#     headline = forms.CharField(max_length=255)
#     full_description = forms.CharField()
#     address = AddressField()
#     guests = forms.IntegerField()

class CitizenRefugeSpaceForm(forms.ModelForm):
    additional = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple,
                                         choices=CITIZEN_SPACE_ADDITIONAL_SHORT)

    mugshot = forms.ImageField()
    start_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))
    end_date = forms.DateField(widget=forms.DateInput(format='%d/%m/%Y'),
                          input_formats=('%d/%m/%Y',))

    # def __init__(self, *args, **kwargs):
    #     super(CitizenRefugeSpaceForm, self).__init__(*args, **kwargs)

    # class Meta:
    #     model = CitizenSpace
    #     fields = ('headline', 'address', 'guests', 'full_description', 'additional')

CitizenRefugeSpaceFormset = inlineformset_factory(CitizenRefuge, CitizenSpace,
    form=CitizenRefugeSpaceForm,
    formset=RequiredFormSet,
    fields=('headline', 'address', 'guests', 'full_description', 'additional'),
    extra=0, min_num=1, validate_min=True)


CitizenRefugeDatesFormset = inlineformset_factory(
    CitizenSpace,
    DateRange,
    fields=('start_date', 'end_date'),
    extra=0, min_num=1, validate_min=True)

SpacePhotoFormset = inlineformset_factory(CitizenSpace, SpacePhoto, fields=(
    'image',
))

class CitizenRefugeSpaceCombineForm(forms.ModelForm):
    dateForm = CitizenRefugeDatesFormset
    mainForm = CitizenRefugeSpaceFormset