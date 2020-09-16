from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from .models import *


class StockForm(forms.ModelForm):
    class Meta:
        model = Stock
        fields = '__all__'


class CatgoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_name']


class SaleRegisterForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = '__all__'


class RefundForm(forms.ModelForm):
    class Meta:
        model = Refund
        fields = '__all__'


class WorkersForm(forms.ModelForm):
    class Meta:
        model = SalesPerson
        fields = '__all__'


class SignUpUserForm(UserCreationForm):
    GENDER = [
        ('M','Male'),
        ('F','Female'),
    ]
    nrc = forms.CharField(max_length=20)
    phone = forms.CharField(max_length=30)
    location = forms.CharField(max_length=50)
    gender = forms.ChoiceField(choices=GENDER)


    class Meta:
        model = User
        fields = ('first_name','last_name','username','email','gender','password1','password2','nrc','phone','location',)


class LoginUserForm(AuthenticationForm):

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise forms.ValidationError('Not allowed')