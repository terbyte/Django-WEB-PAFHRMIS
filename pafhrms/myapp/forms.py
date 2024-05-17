from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField()

class searchPersonnel(forms.Form):
    query = forms.CharField(label='Search for a book', max_length=100)



