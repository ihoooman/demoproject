# In your accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from .models import CustomUser


# Update your accounts/forms.py file - change this line:
class SignUpForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = CustomUser  # Change from User to CustomUser
        fields = ('username', 'email', 'password1', 'password2', 'phone_number')


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'autofocus': True}))
    password = forms.CharField(widget=forms.PasswordInput())


class PhoneForm(forms.Form):
    phone = forms.CharField(
        max_length=15,
        label='شماره تلفن',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '09XXXXXXXXX',
            'dir': 'ltr'
        })
    )

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        # Basic validation for Iranian phone numbers
        if not (phone.startswith('09') and len(phone) == 11):
            raise forms.ValidationError('لطفا یک شماره تلفن معتبر وارد کنید')
        return phone


class OTPForm(forms.Form):
    otp = forms.CharField(
        max_length=6,
        label='کد تایید',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '۶ رقم',
            'dir': 'ltr'
        })
    )

    def clean_otp(self):
        otp = self.cleaned_data['otp']
        if not otp.isdigit() or len(otp) != 6:
            raise forms.ValidationError('کد تایید باید شامل ۶ رقم باشد')
        return otp