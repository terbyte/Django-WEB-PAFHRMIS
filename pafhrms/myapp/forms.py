from django import forms
from .models import PersonnelItem
from .fields import CustomDateField, CustomDateInput




class UploadFileForm(forms.Form):
    file = forms.FileField()


class PersonnelItemForm(forms.ModelForm):
    BIRTHDAY = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'], required=False)
    EFFECTIVE_DATE_APPOINTMENT = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'])
    EFFECTIVE_DATE_ENTERED = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'])
    DATE_LAST_PROMOTION_APPOINTMENT = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'], required=False)
    DATE_FIRST_TRANCHE_REENLISTMENT = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'], required=False)
    DATE_SECOND_TRANCHE_REENLISTMENT = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'], required=False)

    class Meta:
        model = PersonnelItem
        fields = '__all__'


class MyForm(forms.Form):
    field1 = forms.CharField(label='Field 1', max_length=100)
    field2 = forms.CharField(label='Field 2', max_length=100)
    field3 = forms.CharField(label='Field 3', max_length=100)
    field4 = forms.CharField(label='Field 4', max_length=100)