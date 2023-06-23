from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.db import models
from ckeditor.fields import RichTextField

GENDER = (
    ('M', 'Male'),
    ('F', 'Female'),
)

phone_regex = RegexValidator(regex=r'[0][6-9][0-9]{8}', message="Phone number must be entered in the format: "
                                                                "'0.....'. Up to 10 digits allowed.")


# Create your models here.
class CustomUserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, username, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not username:
            raise ValueError(_('The Username must be set'))
        username = username
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(username, password, **extra_fields)


class Region(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = "region"
        verbose_name = "Region"
        verbose_name_plural = "Region"

    def __str__(self):
        return "{0}".format(self.name)


class District(models.Model):
    name = models.CharField(max_length=40, unique=True)
    region = models.ForeignKey(Region, on_delete=models.CASCADE, null=False, related_name="region_districts")

    class Meta:
        db_table = "district"
        verbose_name = "District"
        verbose_name_plural = "District"

    def __str__(self):
        return f"{self.name}"


class School(models.Model):
    name = models.CharField(max_length=60)
    district = models.ForeignKey(District, on_delete=models.CASCADE, null=False, related_name="school_district")

    class Meta:
        db_table = "school"
        verbose_name = "School"
        verbose_name_plural = "School"

    def __str__(self):
        return f"{self.name}"


class User(AbstractUser, PermissionsMixin):
    # username = None

    first_name = models.CharField(max_length=100, null=True, blank=False)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    phone = models.CharField(validators=[phone_regex], max_length=17, blank=True)  # validators should be a list
    email = models.EmailField(null=True, blank=True)
    sex = models.CharField(choices=GENDER, max_length=1, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # a admin user; non super-user
    is_superuser = models.BooleanField(default=False)  # a superuser

    # notice the absence of a "Password field", that is built in.

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []  # Email & Password are required by default.

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    class Meta:
        db_table = 'user'


class Role(models.Model):
    name = models.CharField(max_length=40, unique=True)

    class Meta:
        db_table = "role"
        verbose_name = "Role"
        verbose_name_plural = "Role"

    def __str__(self):
        return "{0}".format(self.name)


class Staff(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False, related_name="user_staff")
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False, related_name="school_staff")
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, related_name="staff_role")
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "staff"
        verbose_name = "Staff"
        verbose_name_plural = "Staff"

    def __str__(self):
        return f"{self.user}"


class Level(models.Model):
    name = models.CharField(max_length=12, unique=True)

    class Meta:
        db_table = "level"
        verbose_name = "Level"
        verbose_name_plural = "Level"

    def __str__(self):
        return f"{self.name}"


class Term(models.Model):
    name = models.CharField(max_length=8, unique=True)

    class Meta:
        db_table = "term"
        verbose_name = "Term"
        verbose_name_plural = "Term"

    def __str__(self):
        return f"{self.name}"


class Subject(models.Model):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        db_table = "subject"
        verbose_name = "Subject"
        verbose_name_plural = "Subject"

    def __str__(self):
        return f"{self.name}"


class AcademicYear(models.Model):
    name = models.IntegerField(unique=True)
    start_date = models.DateField()
    end_date = models.DateField()
    total_week = models.IntegerField(null=True, blank=True)
    is_current = models.BooleanField(default=False)

    # clean() method is overridden to provide the custom validation logic
    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date should be greater than or equal to start date.")

    def save(self, *args, **kwargs):
        # Calculate the total number of weeks between the start and end dates
        delta = self.end_date - self.start_date
        total_week = (delta.days // 7) + 1  # Add 1 to account for the partial week at the start or end
        self.total_week = total_week

        super(AcademicYear, self).save(*args, **kwargs)

    class Meta:
        db_table = "academic_year"
        verbose_name = "Academic Year"
        verbose_name_plural = "Academic Year"

        constraints = [
            models.UniqueConstraint(
                fields=['is_current'],
                condition=models.Q(is_current=True),
                name='one_current_academic_year'
            )
        ]

    def __str__(self):
        return f"{self.name}"


class AcademicTerm(models.Model):
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, related_name="act_acy")
    term = models.ForeignKey(Term, on_delete=models.CASCADE, related_name="academic_year_term")
    start_date = models.DateField()
    end_date = models.DateField()
    total_week = models.IntegerField(null=True, blank=True)

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date should be greater than or equal to start date.")

    def save(self, *args, **kwargs):
        delta = self.end_date - self.start_date
        total_week = (delta.days // 7) + 1
        self.total_week = total_week
        super(AcademicTerm, self).save(*args, **kwargs)

    class Meta:
        db_table = "academic_term"
        verbose_name = "Academic Term"
        verbose_name_plural = "Academic Term"
        unique_together = ['academic_year', 'term']

    def __str__(self):
        return f"{self.academic_year} {self.term}"


class Topic(models.Model):
    name = models.CharField(max_length=60)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False, related_name="topic_subject")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=False, related_name="topic_level")
    max_week = models.IntegerField()
    number = models.IntegerField()

    class Meta:
        db_table = "topic"
        verbose_name = "Topic"
        verbose_name_plural = "Topic"

    def __str__(self):
        return f"{self.name}"


class TeachingCalendar(models.Model):
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE, null=False, related_name="topic_tc")
    academic_term = models.ForeignKey(AcademicTerm, on_delete=models.CASCADE, null=False, related_name="ac_tc")
    start_date = models.DateField()
    end_date = models.DateField()
    total_week = models.IntegerField()

    def clean(self):
        if self.end_date < self.start_date:
            raise ValidationError("End date should be greater than or equal to start date.")

    def save(self, *args, **kwargs):
        delta = self.end_date - self.start_date
        total_week = (delta.days // 7) + 1
        self.total_week = total_week
        super(TeachingCalendar, self).save(*args, **kwargs)

    class Meta:
        db_table = "teaching_calendar"
        verbose_name = "Teaching Calendar"
        verbose_name_plural = "Teaching Calendar"
        unique_together = ['topic', 'academic_term']

    def __str__(self):
        return f"{self.topic} {self.academic_term}"


class TeachingProgressSummary(models.Model):
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False, related_name="subject_progress")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=False, related_name="shool_level_progress")
    school = models.ForeignKey(School, on_delete=models.CASCADE, null=False, related_name="school_progress")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=False,
                                      related_name="school_progress_year")
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

    class Meta:
        db_table = "teaching_progress_summary"
        verbose_name = "Teaching Progress_summary"
        verbose_name_plural = "Teaching Calendar"
        unique_together = ['subject', 'level', 'school', 'academic_year']

    def __str__(self):
        return f"{self.subject} {self.academic_year}"


class Workload(models.Model):
    teacher = models.ForeignKey(Staff, on_delete=models.CASCADE, null=False, related_name="workload_teacher")
    academic_year = models.ForeignKey(AcademicYear, on_delete=models.CASCADE, null=False, related_name="workload_acy")
    level = models.ForeignKey(Level, on_delete=models.CASCADE, null=False, related_name="workload_level")
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, null=False, related_name="workload_subject")

    class Meta:
        db_table = "workload"
        verbose_name = "Workload"
        verbose_name_plural = "Workload"

    def __str__(self):
        return f"{self.teacher} {self.academic_year} {self.level}"


class TeachingReport(models.Model):
    workload = models.ForeignKey(Workload, on_delete=models.CASCADE, null=False, related_name="report_workload")
    verifier = models.ForeignKey(Staff, on_delete=models.CASCADE, null=True, blank=True, related_name="report_verifier")
    calendar = models.ForeignKey(TeachingCalendar, on_delete=models.CASCADE, null=False, related_name="report_tc")
    report = RichTextField()
    created_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(auto_now=True)
    is_verified = models.BooleanField(default=False)

    class Meta:
        db_table = "teaching_report"
        verbose_name = "Teaching Report"
        verbose_name_plural = "Teaching Report"

    def __str__(self):
        return f"{self.workload} {self.verifier}"
