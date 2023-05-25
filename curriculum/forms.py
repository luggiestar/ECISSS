from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.hashers import make_password
from django.core.validators import RegexValidator
from django.forms import ModelForm
from django_select2.forms import Select2Widget
from .models import *

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)
phone_regex = RegexValidator(regex=r'[0][6-9][0-9]{8}', message="Phone number must be entered in the format: "
                                                                "'0.....'. Up to 10 digits allowed.")


class SubjectForm(ModelForm):
    class Meta:
        model = Subject
        fields = ('name',)


class TermForm(ModelForm):
    class Meta:
        model = Term
        fields = ('name',)


class LevelForm(ModelForm):
    class Meta:
        model = Level
        fields = ('name',)


class RegionForm(ModelForm):
    class Meta:
        model = Region
        fields = ('name',)


class DistrictForm(ModelForm):
    region = forms.ModelChoiceField(queryset=Region.objects.all(), widget=Select2Widget)

    class Meta:
        model = District
        fields = ('name', 'region',)


class UserForm(UserCreationForm):
    password1 = forms.CharField(widget=forms.PasswordInput(), label="password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="confirm password")
    username = forms.CharField(widget=forms.TextInput())

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'sex', 'email', 'username', 'password1', 'password2')


class TopicForm(forms.ModelForm):
    subject = forms.ModelChoiceField(queryset=Subject.objects.all(), widget=Select2Widget)
    level = forms.ModelChoiceField(queryset=Level.objects.all(), widget=Select2Widget)

    class Meta:
        model = Topic
        fields = ('name', 'subject', 'level', 'max_week', 'number')


class UserEditForm(ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'sex', 'email', 'username')


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(widget=forms.PasswordInput(), label='Current Password')
    new_password = forms.CharField(widget=forms.PasswordInput(), label='New Password')
    repeat_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm password')


class StaffForm(forms.Form):
    first_name = forms.CharField()
    last_name = forms.CharField()
    phone = forms.CharField(validators=[phone_regex])  # validators should be a list
    sex = forms.CharField(widget=forms.Select(choices=GENDER))
    email = forms.EmailField(widget=forms.EmailInput)
    username = forms.CharField()
    password1 = forms.CharField(widget=forms.PasswordInput(), label="password")
    password2 = forms.CharField(widget=forms.PasswordInput(), label="confirm password")
    school = forms.ModelChoiceField(queryset=School.objects.all(), widget=Select2Widget)
    role = forms.ModelChoiceField(queryset=Role.objects.all(), widget=Select2Widget)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'sex', 'email', 'username', 'password1', 'password2')

    def save(self):
        # Create and save new User object with form data
        hashed_password = make_password(self.cleaned_data['password1'])
        user = User.objects.create(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            phone=self.cleaned_data['phone'],
            sex=self.cleaned_data['sex'],
            email=self.cleaned_data['email'],
            username=self.cleaned_data['username'],
            password=hashed_password
        )

        staff = Staff.objects.create(
            user=user,
            school=self.cleaned_data['school'],
            role=self.cleaned_data['role'],
        )

        return user, staff


class AcademicYearForm(forms.ModelForm):
    start_date = forms.DateField(widget=forms.DateInput())
    end_date = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = AcademicYear
        fields = ('name', 'start_date', 'end_date')


class AcademicTermForm(forms.ModelForm):
    academic_year = forms.ModelChoiceField(queryset=AcademicYear.objects.all(), widget=Select2Widget)
    term = forms.ModelChoiceField(queryset=Term.objects.all(), widget=Select2Widget)
    start_date = forms.DateField(widget=forms.DateInput())
    end_date = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = AcademicTerm
        fields = ('academic_year', 'term', 'start_date', 'end_date')


class TeachingCalendarForm(forms.ModelForm):
    topic = forms.ModelChoiceField(queryset=Topic.objects.all(), widget=Select2Widget)
    academic_term = forms.ModelChoiceField(queryset=AcademicTerm.objects.all(), widget=Select2Widget)
    start_date = forms.DateField(widget=forms.DateInput())
    end_date = forms.DateField(widget=forms.DateInput())

    class Meta:
        model = TeachingCalendar
        fields = ('topic', 'academic_term', 'start_date', 'end_date')
