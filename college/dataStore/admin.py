
from django.contrib import admin
from django.contrib.admin.models import LogEntry,DELETION
from .models import Person, Lecturer, Student, Grad_Student, Degree, Researcher, Grant, Support, Department, College, Course, Session, CurrentSession, OldSession
from django.utils.html import escape
from django.urls import reverse
from django.utils.safestring import mark_safe
from .form import LecturerAdminForm, StudentAdminForm, DegreeAdminForm, SessionAdminForm, ResearcherAdminForm, CurrentSessionAdminForm, OldSessionAdminForm, Grad_StudentAdminForm
from django.utils.translation import gettext_lazy as _



# customized the admin interface
admin.site.empty_value_display = _('(None)')
admin.site.list_per_page = 50
admin.site.site_header = _('College Data Store')
admin.site.index_title = _("Data Store Management")
admin.site.site_title = _("Data Admin")



@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
  
    """
    Register the django log table into the admin.
    Add some customization and also define user access permission.
    """
    
    date_hierarchy = 'action_time'

    list_filter = [
        'user',
        'content_type',
        'action_flag',
        'action_time'
    ]


    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
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

    
    
    

@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
  
  """
    Register the person model into the admin.
    Add some customization.
  """
    
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
    
  date_hierarchy = 'time'
    
  list_display = ('fullName', 'category', 'address')
  
  list_filter = ('category', 'sex')
  
  preserve_filters = False

  search_fields = ['firstName', 'middleName', 'lastName']




@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
  
  """
    Register the lecturer model into the admin.
    Add some customization.
  """
  
  form = LecturerAdminForm

  date_hierarchy = 'time'
  list_display = ('fullName', 'rank', 'officeAddress')
  list_filter = ('rank', 'salary')
  preserve_filters = False
  search_fields = ['person__firstName', 'person__middleName', 'person__lastName']
  autocomplete_fields = ['person']
  




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  
  """
    Register the student model into the admin.
    Add some customization.
  """
  
  form = StudentAdminForm

  date_hierarchy = 'time'
  fields = ('person', 'level', ('minor', 'major'), ('Reg', 'trspt'))
  filter_vertical = ('Reg', 'trspt')
  list_display = ('fullName', 'level', 'minor','major')
  list_filter = ('level',)
  preserve_filters = False
  search_fields = ['person__firstName', 'person__middleName', 'person__lastName']
  autocomplete_fields = ['person', 'minor', 'major', 'Reg', 'trspt']
  


@admin.register(Grad_Student)
class Grad_StudentAdmin(admin.ModelAdmin):
  
  """
    Register the graduate model into the admin.
    Add some customization.
  """
  
  form = Grad_StudentAdminForm
  
  date_hierarchy = 'time'
  list_display = ('fullName', 'advisor')
  list_filter = ('degrees__degree',)
  preserve_filters = False
  search_fields = ['student__person__firstName', 'student__person__middleName', 'student__person__lastName']
  autocomplete_fields = ['student', 'advisor', 'committee']



@admin.register(Degree)
class DegreeAdmin(admin.ModelAdmin):
  
  """
    Register the degree model into the admin.
    Add some customization.
  """
  
  form = DegreeAdminForm

  date_hierarchy = 'time'
  list_display = ('degree', 'college', 'year')
  list_filter = ('college', 'degree')
  preserve_filters = False



@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
  
  """
    Register the researcher model into the admin.
    Add some customization.
  """
  
  form = ResearcherAdminForm

  date_hierarchy = 'time'
  filter_vertical = ('support',)
  list_display = ('fullName',)
  search_fields = ['person__firstName', 'person__middleName', 'person__lastName']
  autocomplete_fields = ['person', 'support']
  


@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
  
  """
    Register the grant model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'
  list_display = ('title', 'agency', 'investigator')
  search_fields = ['title', 'agency']
  autocomplete_fields = ['investigator']



@admin.register(Support)
class SupportAdmin(admin.ModelAdmin):
  
  """
    Register the support model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'
  list_display = ('agency', 'start', 'end', 'spend')
  list_filter = ('start', 'end')
  preserve_filters = False
  search_fields = ['grant__agency',]
  autocomplete_fields = ['grant']



@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
  
  """
    Register the department model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'
  filter_vertical = ('lecturers',)
  list_display = ('Name', 'HOD', 'college')
  list_filter = ('college__name',)
  preserve_filters = False
  search_fields = ['Name',]
  autocomplete_fields = ('HOD', 'lecturers')



@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
  
  """
    Register the college model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'
  list_display = ('name', 'dean', 'office')
  list_filter = ('name',)
  preserve_filters = False



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  
  """
    Register the course model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'
  list_display = ('name', 'code', 'Dept', 'des')
  search_fields = ('name', 'code',)
  autocomplete_fields = ['Dept']



@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
  
  """
    Register the session model into the admin.
    Add some customization.
  """
  
  form = SessionAdminForm
  fields = (('year', 'qtr'), ('course', 'teacher'))
  
  list_display  = ('name', 'year', 'qtr', 'teacher')
  
  date_hierarchy = 'time'
  list_filter = ('qtr',)
  preserve_filters = False
  search_fields = ['course__name']
  autocomplete_fields = ['course', 'teacher']
  


@admin.register(CurrentSession)
class CurrentSessionAdmin(admin.ModelAdmin):
  
  """
    Register the currentSession model into the admin.
    Add some customization.
  """
  
  form = CurrentSessionAdminForm

  date_hierarchy = 'time'
  list_display = ('course', 'teacher')
  search_fields = ['session__course__name']
  autocomplete_fields = ['session']
  


@admin.register(OldSession)
class OldSessionAdmin(admin.ModelAdmin):
  
  """
    Register the oldSession model into the admin.
    Add some customization.
  """
  
  form = OldSessionAdminForm

  date_hierarchy = 'time'
  list_display = ('course', 'teacher', 'year', 'quarter', 'grade')
  search_fields = ['session__course__name']
  autocomplete_fields = ['session']
