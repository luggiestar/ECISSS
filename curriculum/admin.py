from django.contrib import admin

# Register your models here.
from django import forms

from .models import *


class AcademicYearForm(forms.ModelForm):
    class Meta:
        model = AcademicYear
        exclude = ['total_week']


class AcademicTermForm(forms.ModelForm):
    class Meta:
        model = AcademicTerm
        exclude = ['total_week']


class AcademicYearAdmin(admin.ModelAdmin):
    form = AcademicYearForm


admin.site.register(AcademicYear, AcademicYearAdmin)


class AcademicTermAdmin(admin.ModelAdmin):
    form = AcademicYearForm


admin.site.register(AcademicTerm, AcademicTermAdmin)
admin.site.register(Term)
admin.site.register(Workload)
admin.site.register(User)
admin.site.register(Role)
admin.site.register(Staff)
admin.site.register(Topic)
admin.site.register(TeachingCalendar)
admin.site.register(TeachingReport)
admin.site.register(Subject)
admin.site.register(Level)
admin.site.register(School)
admin.site.register(District)
admin.site.register(Region)
