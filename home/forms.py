from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import *

class CustomUserCreationForm(UserCreationForm):
    is_manager = forms.BooleanField(label='Manager', required=False)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = UserCreationForm.Meta.fields + ('name', 'phone', 'is_manager',)


class BillingForm(forms.Form):
    accommodation = forms.ModelChoiceField(queryset=Accommodation.objects.none())
    food = forms.ModelChoiceField(queryset=Food.objects.none())

    def __init__(self, package_id, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accommodation'].queryset = Accommodation.objects.filter(package_id=package_id)
        self.fields['food'].queryset = Food.objects.filter(package_id=package_id)
