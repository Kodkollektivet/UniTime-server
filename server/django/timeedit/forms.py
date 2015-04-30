
from django import forms

# Form for searching
class EventForm(forms.Form):
    course = forms.CharField(min_length=4, max_length=7)
