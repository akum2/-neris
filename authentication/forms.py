from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm

from authentication.models import TheUsers, UploadedDocuments


class UserLoginForm(ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput(
        attrs={"class": 'form-control form-control-user'}
    ))
    username = forms.CharField(label='username', widget=forms.TextInput(
        attrs={"class": 'form-control form-control-user', }
    ))

    class Meta:
        model = TheUsers
        fields = ('username', 'password')

    def clean(self):
        if self.is_valid():
            username = self.cleaned_data['username']
            password = self.cleaned_data["password"]

            if not authenticate(username=username, password=password):
                raise forms.ValidationError('Invalid Entries')


class UserRegistrationForm(UserCreationForm):
    password1 = forms.CharField(label="Password", max_length=20,
                                widget=forms.PasswordInput(
                                    attrs={"class": 'form-control form-control-user'
                                           }
                                )
                                )
    password2 = forms.CharField(label="Confirm Password", max_length=20,
                                widget=forms.PasswordInput(
                                    attrs={"class": 'form-control form-control-user'
                                           }
                                )
                                )

    class Meta:
        model = TheUsers
        fields = ('username', 'name', 'email',
                  'phone', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'name': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'email': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
            'phone': forms.TextInput(attrs={'class': 'form-control form-control-user'}),
        }


class UpdateUserForm(forms.ModelForm):
    name = forms.CharField(max_length=100,
                           required=True,
                           widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    profile = forms.ImageField(required=False, )

    class Meta:
        model = TheUsers
        fields = ['name', 'email', 'phone']


class UploadedDocumentsForm(forms.ModelForm):
    class Meta:
        model = UploadedDocuments
        fields = "__all__"
        widgets = {
            'document': forms.FileInput(
                attrs={
                    'class': 'drop-zone__input',
                    'id': 'file',
                    'accepts': 'application/pdf,\
                    application/msword, \
                        application/vnd.openxmlformats-officedocument\
                            .wordprocessingml.document',
                    'required': True,
                }
            ),
        }
