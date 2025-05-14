from django import forms
from .models import Vendor, VendorDocument, ShortfallDocument
from django.contrib.auth.models import User

class RegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label="Password")
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password and confirm_password and password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        

class VendorForm(forms.ModelForm):
    class Meta:
        model = Vendor
        fields = ['name']

class VendorDocumentForm(forms.ModelForm):
    class Meta:
        model = VendorDocument
        fields = ['file']

class ShortfallDocumentForm(forms.ModelForm):
    class Meta:
        model = ShortfallDocument
        fields = ['shortfall_stage', 'file', 'reason']
