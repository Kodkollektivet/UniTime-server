# -*- coding:utf-8 -*-

import re

from django import forms
from django.core.validators import RegexValidator

# Form for searching
class EventForm(forms.Form):
    event = forms.CharField(
        min_length=4, 
        max_length=7
    )
    
class CourseForm(forms.Form):
    course = forms.CharField(
        min_length=6,
        max_length=6,
           validators=[
            RegexValidator(
                regex=re.compile(r'(^\d\w{2}\d{3}$)'),
                message='Search term must be a course code!',
                code='invalid_search'
            ),
        ]
    )
