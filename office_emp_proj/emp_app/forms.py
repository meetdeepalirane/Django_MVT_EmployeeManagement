from django import forms
from django.core import validators
from .models import Feedback_Model,EmployeeImage,Registration


class Feedbackform(forms.ModelForm):
    class Meta:
        model=Feedback_Model
        fields = "__all__"


class imageForm(forms.ModelForm):
    class Meta:
        model = EmployeeImage
        fields = ['img']

class registrationform(forms.ModelForm):
    class Meta:
        model=Registration
        fields=['first_name','last_name','username','Email','password','renter_password']
