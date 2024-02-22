
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from .models import Person, Lecturer, Student, Department, Faculty 
from .form import StudentAdminForm
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
      'fields': (('first_name', 'middle_name', 'last_name'), 'birthday', 'sex')
    }),
    
    ('Address', {
      'classes': ('extrapretty',),
      'fields': (('apt_no', 'lane_no'), 'street', ('city', 'state'), 'zipcode')
    }),
    )
    
  date_hierarchy = 'time'

  ordering = ['first_name']
    
  list_display = ('fullName', 'sex', 'address')
  
  list_filter = ('sex',)
  
  preserve_filters = False

  search_fields = ['first_name', 'middle_name', 'last_name']




@admin.register(Lecturer)
class LecturerAdmin(admin.ModelAdmin):
  
  """
    Register the Lecturer model into the admin.
    Add some customization.
  """

  fieldsets = (
    ('Personal Info', {
      'classes': ('extrapretty',),
      'fields': (('first_name', 'middle_name', 'last_name'), 'birthday', 'sex')
    }),
    
    ('Level', {
      'classes': ('extrapretty',),
      'fields': ('rank', 'salary', 'office_phone', 'office_address')
    }),
    
    ('Residential Address', {
      'classes': ('extrapretty',),
      'fields': (('apt_no', 'lane_no'), 'street', ('city', 'state'), 'zipcode')
    }),
    )
    
  date_hierarchy = 'time'

  ordering = ['first_name',]
  
  list_display = ('fullName', 'rank', 'office_address')
  
  list_filter = ('sex', 'rank', 'salary')
  
  preserve_filters = False

  search_fields = ['first_name', 'middle_name', 'last_name']
  




@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
  
  """
    Register the student model into the admin.
    Add some customization.
  """
  
  fieldsets = (
    ('Personal Info', {
      'classes': ('extrapretty',),
      'fields': (('first_name', 'middle_name', 'last_name'), 'birthday', 'sex')
    }),
    
    ('Degree', {
      'classes': ('extrapretty',),
      'fields':('level', ('minor', 'major'))
    }),
    
    ('Residential Address', {
      'classes': ('extrapretty',),
      'fields': (('apt_no', 'lane_no'), 'street', ('city', 'state'), 'zipcode')
    }),
    )
  
  form = StudentAdminForm

  date_hierarchy = 'time'

  ordering = ['first_name',]
  
  list_display = ('fullName', 'level', 'minor', 'major')
  
  list_filter = ('sex', 'level',)
  
  preserve_filters = False

  search_fields = ['first_name', 'middle_name', 'last_name']
  
  autocomplete_fields = ['minor', 'major']
  
  


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
  
  """
    Register the department model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'

  ordering = ['name',]
  
  list_display = ('name', 'faculty', 'phone_no', 'office_no')
  
  list_filter = ('faculty__name',)
  
  preserve_filters = False

  search_fields = ['name',]
  
  autocomplete_fields = ('faculty',)



@admin.register(Faculty)
class FacultyAdmin(admin.ModelAdmin):
  
  """
    Register the faculty model into the admin.
    Add some customization.
  """
  
  date_hierarchy = 'time'

  ordering = ['name',]
  
  list_display = ('name', 'dean', 'phone_no')
  
  search_fields = ['name',]



