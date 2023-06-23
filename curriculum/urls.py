from django.urls import path
from .views import *
urlpatterns = [
    path('', login_view, name='login'),
    path('user-logout', user_logout, name='user_logout'),
    path('user-dashboard', dashboard, name='dashboard'),

    # location
    path('regions-and-districts', location, name="location"),
    path('save-district', save_district, name="save_district"),
    path('save-region', save_region, name="save_region"),

    # academic
    path('subjects', subject_list, name="subject_list"),
    path('edit-subject/<subject_id>', edit_subject, name="edit_subject"),
    path('delete-subject', delete_subject, name="delete_subject"),

    path('terms', term_list, name="term_list"),
    path('edit-term/<term_id>', edit_term, name="edit_term"),
    path('delete-term', delete_term, name="delete_term"),

    path('levels', level_list, name="level_list"),
    path('edit-level/<level_id>', edit_level, name="edit_level"),
    path('delete-level', delete_level, name="delete_level"),

    path('topics', topic_list, name="topic_list"),
    path('edit-topic/<topic_id>', edit_topic, name="edit_topic"),
    path('delete-topic', delete_topic, name="delete_topic"),

    path('academic-years', academic_year_list, name="academic_year_list"),
    path('edit-academic-year/<academic_year_id>', edit_academic_year, name="edit_academic_year"),
    path('delete-academic-year', delete_academic_year, name="delete_academic_year"),

    path('academic-terms', academic_term_list, name="academic_term_list"),
    path('edit-academic-term/<academic_term_id>', edit_academic_term, name="edit_academic_term"),
    path('delete-academic-term', delete_academic_term, name="delete_academic_term"),

    # Teaching and workload
    path('teaching-calendars', teaching_calendar_list, name="teaching_calendar_list"),
    path('edit-teaching-calendar/<teaching_calendar_id>', edit_teaching_calendar, name="edit_teaching_calendar"),
    path('delete-teaching-calendar', delete_teaching_calendar, name="delete_teaching_calendar"),
    path('teaching-workload', workload, name="teaching_workload"),
    path('edit-workload/<workload_id>', edit_workload, name="edit_workload"),
    path('delete-workload/', delete_workload, name="delete_workload"),

    path('teacher-workload/', teacher_workload, name="teacher_workload"),
    path('teaching-report/<workload_id>', teaching_report, name="teaching_report"),
    path('teaching-report-verifying', teaching_report_verify, name="verify"),
    path('teaching-report-history', teaching_report_history, name="report_history"),
    path('report-verifying/<report_id>', verify_report, name="verify_report"),

    # users path
    path('users-list', users, name="user_list"),
    path('user-profile', user_profile, name="user_profile"),
    path('change-password', change_password, name="change_password"),
    path('save-user', save_user, name="save_user"),
    path('edit-user/<user_id>', edit_user, name="edit_user"),
    path('set-superuser', set_superuser, name="set_superuser"),
    path('set-staff', set_staff, name="set_staff"),
    path('set-active', set_active, name="set_active"),
    path('delete-user', delete_user, name="delete_user"),
    path('user-role', user_role, name="user_role"),
    path('edit-role/<role_id>', edit_role, name="edit_role"),

    # rating
    path('rating', rating, name="rating"),


    # staff
    path('staffs-list', staffs, name="staff_list"),
    path('staff-entry-template/<templ_name>', staff_entry_template, name="staff_entry_template"),
    path('upload-staff-entry', upload_staff_entry, name="upload_staff_entry"),
]
