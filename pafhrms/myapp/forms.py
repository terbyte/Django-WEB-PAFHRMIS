from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class DateForm(forms.Form):
    date = forms.DateField(
        widget=forms.DateInput(attrs={'class': 'form-control', 'placeholder': 'Select a date'}),
        input_formats=['%d-%b-%Y'],
    )


#unue

# class searchPersonnel(forms.Form):
#     query = forms.CharField(label='Search for a book', max_length=100)



