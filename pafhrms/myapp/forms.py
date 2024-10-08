from django import forms
from .models import tbl_Personnel
from .fields import CustomDateField, CustomDateInput

from myapp.models import Placement  #models.py





class UploadFileForm(forms.Form):
    file = forms.FileField()

class UploadOrderForm(forms.Form):
    uploadOrder = forms.FileField()







#class aint working beyond this point 

class tbl_PersonnelForm(forms.ModelForm):
    BIRTHDAY = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'], required=False)
    EFFECTIVE_DATE_APPOINTMENT = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'])
    EFFECTIVE_DATE_ENTERED = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'])
    DATE_LAST_PROMOTION_APPOINTMENT = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'], required=False)
    DATE_LASTFULL_REENLISTMENT = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'], required=False)
    DATE_LASTFULL_REENLISTMENT = forms.DateField(widget=CustomDateInput(), input_formats=['%d-%b-%Y'], required=False)

    class Meta:
        model = tbl_Personnel
        fields = '__all__'

# this class aint working
class Placement(forms.ModelForm):  
    class Meta:  
        model = Placement  
        fields = "__all__"
 
    def __init__(self, *args, **kwargs):
            super(Placement, self).__init__(*args, **kwargs)
            for field_name, field in self.fields.items():
                field.widget.attrs['class'] = 'form-control'   


