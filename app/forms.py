from django import forms
from app.models import *


class Userforms(forms.ModelForm):
    class Meta:
        model=User
        fields=['username','email','password']
        widgets={'password':forms.PasswordInput}
        help_texts={'password':'password can 8 character minimum '}
        labels={'username':'USERNAME','email':'E-mail'}
        
class Profileforms(forms.ModelForm):
    class Meta:
        model=Profile
        fields=['address','profile_pic']