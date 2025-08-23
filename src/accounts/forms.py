import re
from django import forms 
from .models import CustomUser
from django.contrib.auth.forms import AuthenticationForm

class RegistrationUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Enter Password'}), required=True)
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder':'Confirm Password'}), required=True)
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email']
        
    def __init__(self,*args, **kwargs):
        super(RegistrationUserForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'Your First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Your Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Your Email Address'


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'  

    def clean(self):
        super(RegistrationUserForm,self).clean()
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        email = self.cleaned_data.get('email')
        
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This Email is already has been token.")
        
        
        if password and not re.search(r'[A-Za-z]', password):  # checks for letters
            raise forms.ValidationError("Password must contain at least one letter.")
        
        if password and not re.search(r'\d', password):  # checks for digits
            raise forms.ValidationError("Password must contain at least one number.")
        
        if password and not re.search(r'[!@#$%^&*]', password):
            raise forms.ValidationError("The password must contain at least one special character.")

        if password != confirm_password:
            raise forms.ValidationError('password did not match')
        
        if password and len(password) < 6 :
            raise forms.ValidationError('password length must be greater then {6} character')
        

        

class LoginForm(forms.Form):
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'class': 'form-control',
            'placeholder': 'email@example.com'
    }))


    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Password'
        })
    )
    
   