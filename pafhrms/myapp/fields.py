from django import forms
from datetime import datetime

class CustomDateField(forms.DateField):
    def __init__(self, *args, **kwargs):
        kwargs['input_formats'] = ['%d-%b-%Y']
        super().__init__(*args, **kwargs)

    def clean(self, value):
        try:
            # Attempt to convert the string to a datetime object
            parsed_date = datetime.strptime(value, '%d-%b-%Y')
            # Return the datetime object in the default format
            return parsed_date
        except ValueError:
            raise forms.ValidationError('Enter a date in the format dd-mmm-yyyy.')

class CustomDateInput(forms.DateInput):
    input_type = 'text'
    
    def format_value(self, value):
        if value is None:
            return ''
        if isinstance(value, str):
            try:
                # Attempt to parse and format the date string
                value = datetime.strptime(value, '%Y-%m-%d')
            except ValueError:
                return value
        return value.strftime('%d-%b-%Y')
