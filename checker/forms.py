from django import forms


class CheckerForm(forms.Form):
    nickname = forms.CharField(max_length=50)
    siteurl = forms.CharField(max_length=300)
