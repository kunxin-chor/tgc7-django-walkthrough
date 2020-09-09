from allauth.account.forms import SignupForm
from django import forms
from .models import UserProfile


class CustomizedSignupForm(SignupForm):
    address = forms.CharField(required=False)
    gender = forms.CharField(required=False)

    def save(self, request):
        user = super(CustomizedSignupForm, self).save(request)
        profile = UserProfile()
        profile.user = user
        profile.address = self.cleaned_data['address']
        profile.gender = self.cleaned_data['gender']
        profile.save()
        return user
