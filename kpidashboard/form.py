from django import forms
import datetime

class CustomReportRange(forms.Form):

    startDateTime = forms.DateTimeField(initial=datetime.datetime.now)
    # endDateTime = forms.DateTimeField(initial=datetime.datetime.now)