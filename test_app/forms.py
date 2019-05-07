from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import ReadOnlyPasswordHashField

User = get_user_model()

class EditUserProfileForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    birthday = forms.DateField(widget=forms.SelectDateWidget(years=range(1920, 2040)))

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'biography',
            'birthday',
            'contacts',
            'password',
            )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        f = self.fields.get('user_permissions')
        if f is not None:
            f.queryset = f.queryset.select_related('content_type')

    def clean_password(self):
        return self.initial["password"]


class LoginForm(forms.Form):
    username = forms.CharField(max_length=40,
                widget=forms.TextInput(attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Username',
            }
        ),
    )

    password = forms.CharField(max_length=40,
                widget=forms.PasswordInput(attrs={
                'autofocus': True,
                'class': 'form-control',
                'placeholder': 'Password',
            }
        ),
    )


class UserAdminCreationForm(forms.ModelForm): 
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username',)

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super(UserAdminCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserAdminChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('username', 'password', 'active', 'admin')

    def clean_password(self):
        return self.initial['password']