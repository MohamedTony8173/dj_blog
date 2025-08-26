import re
from django import forms 
from .models import CustomUser, UserProfile


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
    
   
class ProfileUserForm(forms.ModelForm) :
    profile_picture = forms.ImageField(widget=forms.FileInput(attrs={'class': 'form-control-file'}), required=False)
    class Meta:
        model = UserProfile
        fields = ['profile_picture','city','country','phone_number','address_line_1','address_line_2','state','pin_code']
        
    def __init__(self,*args, **kwargs):
        super(ProfileUserForm,self).__init__(*args, **kwargs)


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'  
            
class UserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name']
        
    def __init__(self,*args, **kwargs):
        super(UserForm,self).__init__(*args, **kwargs)


        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'            