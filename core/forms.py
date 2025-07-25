from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, TutorProfile, StudentProfile
from .models import Message
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
from .models import TutorPayment
from .models import StudentProfile
import pytz
from django_countries.widgets import CountrySelectWidget

class TutorRegistrationForm(UserCreationForm):
    experience = forms.CharField(widget=forms.Textarea)
    skills = forms.CharField(widget=forms.Textarea)
    interests = forms.CharField(widget=forms.Textarea)
    location = forms.CharField()
    timezone = forms.CharField()

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'tutor'
        if commit:
            user.save()
            TutorProfile.objects.create(
                user=user,
                experience=self.cleaned_data['experience'],
                skills=self.cleaned_data['skills'],
                interests=self.cleaned_data['interests'],
                location=self.cleaned_data['location'],
                timezone=self.cleaned_data['timezone']
            )
        return user


class StudentRegistrationForm(UserCreationForm):
    academic_needs = forms.CharField(widget=forms.Textarea)
    program_details = forms.CharField()
    preferred_format = forms.CharField()
    required_hours = forms.IntegerField()

    class Meta:
        model = CustomUser
        fields = ['email', 'full_name', 'phone', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.role = 'student'
        if commit:
            user.save()
            StudentProfile.objects.create(
                user=user,
                academic_needs=self.cleaned_data['academic_needs'],
                program_details=self.cleaned_data['program_details'],
                preferred_format=self.cleaned_data['preferred_format'],
                required_hours=self.cleaned_data['required_hours']
            )
        return user

class EmailLoginForm(AuthenticationForm):
    username = forms.EmailField(label="Email", widget=forms.EmailInput(attrs={'autofocus': True}))

class TutorPaymentForm(forms.ModelForm):
    class Meta:
        model = TutorPayment
        fields = ['tutor', 'hours_worked', 'amount_paid']

class StudentProfileEditForm(forms.ModelForm):
    class Meta:
        model = StudentProfile
        fields = ['academic_needs', 'program_details', 'preferred_format', 'required_hours']
        widgets = {
            'academic_needs': forms.Textarea(attrs={'class': 'form-control'}),
            'program_details': forms.TextInput(attrs={'class': 'form-control'}),
            'preferred_format': forms.TextInput(attrs={'class': 'form-control'}),
            'required_hours': forms.NumberInput(attrs={'class': 'form-control'}),
        }

User = get_user_model()

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['recipient', 'subject', 'body']
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'body': forms.Textarea(attrs={'class': 'form-control'}),
        }




class TutorProfileEditForm(forms.ModelForm):
    class Meta:
        model = TutorProfile
        fields = ['experience', 'skills', 'interests', 'location', 'timezone', 'hourly_rate']
        widgets = {
            'location': CountrySelectWidget(attrs={'class': 'form-control'}),
            'timezone': forms.Select(choices=[(tz, tz) for tz in pytz.common_timezones], attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(TutorProfileEditForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field.widget.attrs.get('class') is None:
                field.widget.attrs['class'] = 'form-control'
