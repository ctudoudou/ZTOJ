from django import forms

class UserForm(forms.Form):
    email = forms.EmailField(max_length=45)
    username = forms.CharField(max_length=45)
    password = forms.CharField(max_length=45)
