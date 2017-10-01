from django import forms

class PostForm(forms.Form):
		email = forms.CharField(max_length=256)
		password = forms.CharField(max_length=256)