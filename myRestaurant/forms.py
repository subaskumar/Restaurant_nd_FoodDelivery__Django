from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import UserAccount
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator


# def password_validate(value):
#     if len(value) < 4 :
#         raise ValidationError('password must be contain 8 character')

class SignUpForm(forms.ModelForm):
    password_validate = RegexValidator( regex   =r'^(?=.{8,20})(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@#$%^&!*?]).*$', message ="Password Must be contain 8 Characters, Capital letter, Lower letter, Number, Special Symbol")
    ## (?= pattern) is a zero-width positive lookahead assertion. means'.' (means for every character) followed by *[a-z] , *[0-9].... 
    
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(validators=[password_validate],label='Password confirmation', widget=forms.PasswordInput)
    email = forms.EmailField(max_length=150,required=True, help_text='Email')
    class Meta:
        model = UserAccount
        fields = ['email','password1','password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        query = UserAccount.objects.filter(email__iexact = email)

        if query.exists():
            raise forms.ValidationError('That Email is already taken. Please choose another!')
        return email
    
    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



from django.contrib.auth import login,authenticate
class UserLoginForm(forms.Form):
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    # clean() validation errors added to 'non_field_errors'
    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')   
        if email and password:
            query = UserAccount.objects.filter(email__iexact = email)
            
            if not query.exists():
                self.add_error('email',"This Email is not Registred")
                    
        return super(UserLoginForm, self).clean(*args, **kwargs)