
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import Person, Faculty, Student, Grad_Student, Degree, Researcher, Grant, Support, Department, College, Course, Section, CurrentSection
from .form import StudentAdminForm, GradAdminForm, SectionAdminForm, CurrentSectionAdminForm, ResearcherAdminForm
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
        return False

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
      'classes': ('extrapretty',),
      'fields': ('ssn', ('firstName', 'middleName', 'lastName'), 'birthday', 'sex')
    }),
    
    ('Address', {
      'classes': ('extrapretty',),
      'fields': (('aptNo', 'laneNo'), 'street', ('city', 'state'), 'zipcode')
    }),
    )
    
  date_hierarchy = 'time'

  ordering = ['fullName']
    
  list_display = ('ssn', 'fullName', 'sex', 'address')
  
  list_filter = ('sex',)
  
  preserve_filters = False

  search_fields = ['ssn', 'firstName', 'middleName', 'lastName']




@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
  
  """
    Register the Faculty model into the admin.
    Add some customization.
  """

  fieldsets = (
    ('Personal Info'', {
      'classes': ('extrapretty',),
      'fields': ('ssn', ('firstName', 'middleName', 'lastName'), 'birthday', 'sex')
    }),
    
    (None, {
      'classes': ('extrapretty',),
      'fields': ('rank', 'salary', 'officePhone', 'officeAddress')
    }),
    
    ('Residential Address', {
      'classes': ('extrapretty',),
      'fields': (('aptNo', 'laneNo'), 'street', ('city', 'state'), 'zipcode')
    }),
    )
    
  date_hierarchy = 'time'

  ordering = ['fullName',]
  
  list_display = ('ssn', 'fullName', 'rank', 'officeAddress')
  
  list_filter = ('sex', 'rank', 'salary')
  
  preserve_filters = False

  search_fields = ['ssn', 'firstName', 'middleName', 'lastName']
  




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  
  """
    Register the student model into the admin.
    Add some customization.
  """
  
  fieldsets = (
    ('Personal Info'', {
      'classes': ('extrapretty',),
      'fields': ('ssn', ('firstName', 'middleName', 'lastName'), 'birthday', 'sex')
    }),
    
    (None, {
      'classes': ('extrapretty',),
      'fields':('level', ('minor', 'major'), ('Reg', 'trspt'))
    }),
    
    ('Residential Address', {
      'classes': ('extrapretty',),
      'fields': (('aptNo', 'laneNo'), 'street', ('city', 'state'), 'zipcode')
    }),
    )
  
  form = StudentAdminForm

  date_hierarchy = 'time'

  ordering = ['fullName',]
  
  filter_vertical = ('Reg', 'trspt')
  
  list_display = ('ssn', 'fullName', 'level', 'minor', 'major')
  
  list_filter = ('sex', 'level',)
  
  preserve_filters = False

  search_fields = ['ssn', 'firstName', 'middleName', 'lastName']
  
  autocomplete_fields = ['minor', 'major', 'Reg', 'trspt']
  


@admin.register(Grad_Student)
class Grad_StudentAdmin(admin.ModelAdmin):
  
  """
    Register the graduate model into the admin.
    Add some customization.
  """
  
  fieldsets = (
    ('Personal Info'', {
      'classes': ('extrapretty',),
      'fields': ('ssn', ('firstName', 'middleName', 'lastName'), 'birthday', 'sex')
    }),
    
    (None, {
      'classes': ('extrapretty',),
      'fields':('level', 'college', 'degree', 'year', 'advisor', 'committee')
    }),
    
    ('Residential Address', {
      'classes': ('extrapretty',),
      'fields': (('aptNo', 'laneNo'), 'street', ('city', 'state'), 'zipcode')
    }),
    )
   
  form = GradAdminForm

  date_hierarchy = 'time'

  ordering = ['fullName',]
  
  filter_vertical = ('committee',)
  
  list_display = ('ssn', 'fullName', 'Degree', 'advisor')
  
  list_filter = ('sex', 'degree', 'college')
  
  preserve_filters = False

  search_fields = ['ssn', 'firstName', 'middleName', 'lastName']
  
  autocomplete_fields = ['advisor', 'committee']







@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
  
  """
    Register the researcher model into the admin.
    Add some customization.
  """
  
  form = ResearcherAdminForm
  
  date_hierarchy = 'time'

  ordering = ['fullName',]

  filter_vertical = ('support',)
  
  list_display = ('ssn', 'fullName')
  
  search_fields = ['ssn', 'firstName', 'middleName', 'lastName']
  
  autocomplete_fields = ['support',]
  




@admin.register(Grant)
class GrantAdmin(admin.ModelAdmin):
  
  """
    Register the grant model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'

  ordering = ['title',]

  list_display = ('title', 'agency', 'investigator', 'start', 'end', 'spend')
  
  list_filter = ('start', 'end')
  
  search_fields = ['title', 'agency']
  
  autocomplete_fields = ['investigator']





@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
  
  """
    Register the department model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'

  ordering = ['name',]

  filter_vertical = ('belongs',)
  
  list_display = ('name', 'HOD', 'college')
  
  list_filter = ('college__name',)
  
  preserve_filters = False

  search_fields = ['name',]
  
  autocomplete_fields = ('HOD', 'belongs', 'college')



@admin.register(College)
class CollegeAdmin(admin.ModelAdmin):
  
  """
    Register the college model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'

  ordering = ['name',]
  
  list_display = ('name', 'dean', 'office')
  
  search_fields = ['name',]



@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
  
  """
    Register the course model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'

  ordering = ['code',]

  list_display = ('name', 'code', 'dept', 'des')
  
  list_filter = ('dept__college__name',)
  
  preserve_filters = False
  
  search_fields = ('name', 'code',)
  
  autocomplete_fields = ['dept']



@admin.register(Section)
class SectionAdmin(admin.ModelAdmin):
  
  """
    Register the session model into the admin.
    Add some customization.
  """
  
  form = SectionAdminForm

  ordering = ['year',]

  fields = (('course', 'grade', 'teacher'), ('year', 'qtr'),)
  
  date_hierarchy = 'time'
  
  list_display  = ('name', 'grade', 'year', 'qtr', 'teacher')
  
  autocomplete_fields = ['course', 'teacher']
  


@admin.register(CurrentSection)
class CurrentSectionAdmin(admin.ModelAdmin):
  
  """
    Register the currentSession model into the admin.
    Add some customization.
  """
  
  form = CurrentSectionAdminForm
  
  ordering = ['year',]

  fields = (('course', 'teacher'), ('year', 'qtr'),)
  
  date_hierarchy = 'time'
  
  list_display  = ('name', 'year', 'qtr', 'teacher')
  
  autocomplete_fields = ['course', 'teacher']
  