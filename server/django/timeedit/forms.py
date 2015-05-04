# -*- coding:utf-8 -*-

from django import forms

# Form for searching
class EventForm(forms.Form):
    event = forms.CharField(min_length=4, max_length=7)

class CourseForm(forms.Form):
    course = forms.CharField(min_length=4, max_length=7)
