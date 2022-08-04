
from django.contrib import admin
from django.contrib.admin.models import LogEntry,DELETION
from .models import Person, Lecturer, Student, Grad_Student, Degree, Researcher, Grant, Support, Department, College, Course, Session, CurrentSession, OldSession
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
from .form import LecturerAdminForm, StudentAdminForm, DegreeAdminForm, SessionAdminForm, ResearcherAdminForm, CurrentSessionAdminForm, OldSessionAdminForm, Grad_StudentAdminForm
from django.utils.translation import gettext_lazy as _


# Register your models here.

admin.site.empty_value_display = '(None)'
admin.site.list_per_page = 50
admin.site.site_header = _('College Data Store')
admin.site.index_title = _("Data Store Management")
admin.site.site_title = _("Data Admin")
#admin.site.site_url = None

@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]


    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'object_link',
        'action_flag',
    ]
    
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def has_view_permission(self, request, obj=None):
        return request.user.is_superuser

    def object_link(self, obj):
        if obj.action_flag == DELETION:
            link = escape(obj.object_repr)
        else:
            ct = obj.content_type
            link = '<a href="%s">%s</a>' % (
                reverse('admin:%s_%s_change' % (ct.app_label, ct.model), args=[obj.object_id]),
                escape(obj.object_repr),
            )
        return mark_safe(link)
    object_link.admin_order_field = "object_repr"
    object_link.short_description = "object"
    
    
    

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
  fieldsets = (
    (None, {
      'classes': ('extrapretty'),
      'fields': ('ssn', ('firstName', 'middleName', 'lastName'), 'birthday', 'category', 'sex')
    }),
    
    ('Address', {
      'classes': ('extrapretty'),
      'fields': (('aptNo', 'laneNo'), 'street', ('city', 'state'), 'zipcode')
    }),
    )
    
  list_display = ('fullName', 'category', 'address')
  
  list_filter = ('category', 'sex')
  
  preserve_filters = False

  search_fields = ['firstName', 'middleName', 'lastName']




@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
  form = LecturerAdminForm
  list_display = ('fullName', 'rank', 'officeAddress')
  list_filter = ('rank', 'salary')
  preserve_filters = False
  search_fields = ['person__firstName', 'person__middleName', 'person__lastName']
  autocomplete_fields = ['person']
  




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  form = StudentAdminForm
  fields = ('person', 'level', ('minor', 'major'), ('Reg', 'trspt'))
  filter_vertical = ('Reg', 'trspt')
  list_display = ('fullName', 'level', 'minor','major')
  list_filter = ('level', 'minor__college__name', 'major__college__name')
  preserve_filters = False
  search_fields = ['person__firstName', 'person__middleName', 'person__lastName']
  autocomplete_fields = ['person', 'minor', 'major', 'Reg', 'trspt']
  


@admin.register(Grad_Student)
class Grad_StudentAdmin(admin.ModelAdmin):
  form = Grad_StudentAdminForm
  filter_vertical = ('degrees', 'committee')
  list_display = ('fullName', 'advisor')
  list_filter = ('degrees__college', 'degrees__degree')
  preserve_filters = False
  search_fields = ['student__person__firstName', 'student__person__middleName', 'student__person__lastName']
  autocomplete_fields = ['student', 'degrees', 'advisor', 'committee']



@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
  form = DegreeAdminForm
  list_display = ('degree', 'college', 'year')
  list_filter = ('college', 'degree')
  preserve_filters = False
  search_fields = ['college, degree']



@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
  form = ResearcherAdminForm
  filter_vertical = ('support',)
  list_display = ('fullName',)
  list_filter = ('support__date', 'support__end')
  preserve_filters = False
  search_fields = ['person__firstName', 'person__middleName', 'person__lastName']
  autocomplete_fields = ['person', 'support']
  


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
  list_display = ('title', 'agency', 'investigator')
  search_fields = ['title', 'agency']
  autocomplete_fields = ['investigator']



@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
  list_display = ('agency', 'date', 'end', 'time')
  list_filter = ('date', 'end')
  preserve_filters = False
  search_fields = ['grant__agency',]
  autocomplete_fields = ['grant']



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
  filter_vertical = ('lecturers',)
  list_display = ('Name', 'HOD', 'college')
  list_filter = ('college__name',)
  preserve_filters = False
  search_fields = ['Name',]
  autocomplete_fields = ['HOD', 'lecturers', 'college']



@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
  list_display = ('name', 'dean')
  list_filter = ('name',)
  preserve_filters = False
  search_fields = ['name',]



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  list_display = ('name', 'Dept', 'des')
  search_fields = ['name',]
  autocomplete_fields = ['Dept']



@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
  form = SessionAdminForm
  fields = ('no', ('year', 'qtr'), ('course', 'teacher'))
  
  list_display  = ('name', 'year', 'qtr', 'teacher')
  
  list_filter = ('qtr',)
  preserve_filters = False
  search_fields = ['course__name']
  autocomplete_fields = ['course', 'teacher']
  


@admin.register(CurrentSession)
class CurrentSessionAdmin(admin.ModelAdmin):
  form = CurrentSessionAdminForm
  list_display = ('course', 'teacher')
  search_fields = ['session__course__name']
  autocomplete_fields = ['session']
  


@admin.register(OldSession)
class OldSessionAdmin(admin.ModelAdmin):
  form = OldSessionAdminForm
  list_display = ('course', 'teacher', 'year', 'quarter', 'grade')
  search_fields = ['session__course__name']
  autocomplete_fields = ['session']
