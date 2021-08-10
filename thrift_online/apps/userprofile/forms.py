import phonenumbers

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    address = forms.CharField(max_length=100,
        label="Адрес",
        strip=False,     
        required=False
    )
    zip_code = forms.CharField(max_length=33,
        label="Пощенски код",
        strip=False,     
        required=False
    )
    city = forms.CharField(max_length=33,
        label="Град",
        strip=False,     
        required=False
    )
    phone = forms.CharField(max_length=33,
        label="Телефон",
        strip=False,     
        required=True
    )

    def clean_phone(self):
        phone = self.cleaned_data.get("phone")
        z = phonenumbers.parse(phone, "BG")
        if not phonenumbers.is_valid_number(z):
            raise forms.ValidationError("Невалиден телефон!")
        return phone

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs['class'] = 'input'
        self.fields['zip_code'].widget.attrs['class'] = 'input'
        self.fields['city'].widget.attrs['class'] = 'input'
        self.fields['phone'].widget.attrs['class'] = 'input'

    def save(self, commit=True):
        userprofile = super(UserProfileForm, self).save(commit=False)
        userprofile.phone = self.cleaned_data['phone']
        userprofile.address = self.cleaned_data['address']
        userprofile.zip_code = self.cleaned_data['zip_code']
        userprofile.city = self.cleaned_data['city']

        if commit:
            userprofile.save()

        return userprofile

    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ('user',)

class SignUpForm(UserCreationForm):
    username = forms.CharField(max_length=33,
        label="Никнейм",
        strip=False,     
        required=True
    )
    first_name = forms.CharField(max_length=33,
        label="Име",
        strip=False,     
        required=True
    )
    last_name = forms.CharField(max_length=33,
        label="Фамилия",
        strip=False,     
        required=True
    )
    email = forms.EmailField(max_length=100, required=True)
    password1 = forms.CharField(
        label="Парола",
        strip=False,
        widget=forms.PasswordInput,
        required=True,
    )
    password2 = forms.CharField(
        label="Парола - потвърждение",
        strip=False,
        widget=forms.PasswordInput,
        required=True,
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['email'].widget.attrs['class'] = 'input'
        self.fields['password1'].widget.attrs['class'] = 'input'
        self.fields['password2'].widget.attrs['class'] = 'input'
        self.fields['first_name'].widget.attrs['class'] = 'input'
        self.fields['last_name'].widget.attrs['class'] = 'input'
    
    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and User.objects.filter(email=email).exclude(username=username).count():
            raise forms.ValidationError('Този имейл вече се използва, пробвайте с друг.')
        return email

    def save(self, commit=True):
        user = super(SignUpForm, self).save(commit=False)
        user.email = self.cleaned_data['email']

        user.save()

        return user


class EditUserForm(forms.ModelForm):
    username = forms.CharField(max_length=33,
        label="Никнейм",
        strip=False,     
        required=True
    )
    email = forms.EmailField()
    first_name = forms.CharField(max_length=33,
        label="Име",
        strip=False,     
        required=True
    )
    last_name = forms.CharField(max_length=33,
        label="Фамилия",
        strip=False,     
        required=True
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email',]

    def __init__(self, *args, **kwargs):
        super(EditUserForm, self).__init__(*args, **kwargs)

        self.fields['username'].widget.attrs['class'] = 'input'
        self.fields['email'].widget.attrs['class'] = 'input'
        self.fields['first_name'].widget.attrs['class'] = 'input'
        self.fields['last_name'].widget.attrs['class'] = 'input'
    
    def clean_email(self):
        username = self.cleaned_data.get('username')
        email = self.cleaned_data.get('email')

        if email and (User.objects.filter(email=email).exclude(username=username).count() >= 1):
            raise forms.ValidationError('Този имейл вече се използва, пробвайте с друг.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        try:
            user = User.objects.exclude(pk=self.instance.pk).get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Този никнейм вече се използва.')

    def save(self, commit=True):
        user = super(EditUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.username = self.cleaned_data['username']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']

        if commit:
            user.save()

        return user

class EditUserprofileForm(forms.ModelForm):
    address = forms.CharField(max_length=100,
        label="Адрес",
        strip=False,     
        required=True
    )
    zip_code = forms.CharField(max_length=33,
        label="Пощенски код",
        strip=False,     
        required=True
    )
    city = forms.CharField(max_length=33,
        label="Град",
        strip=False,     
        required=True
    )
    phone = forms.CharField(max_length=33,
        label="Телефон",
        strip=False,     
        required=True
    )

    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ('user',)

        
    def __init__(self, *args, **kwargs):
        super(EditUserprofileForm, self).__init__(*args, **kwargs)

        self.fields['address'].widget.attrs['class'] = 'input'
        self.fields['zip_code'].widget.attrs['class'] = 'input'
        self.fields['city'].widget.attrs['class'] = 'input'
        self.fields['phone'].widget.attrs['class'] = 'input'
