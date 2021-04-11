from django import forms

class LogEntry(forms.Form):
    file = forms.FileField()