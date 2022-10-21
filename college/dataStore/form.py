
"""
All form class are only for admin custom validation, nothing more, nothing less.
"""


from django import forms
from .models import Faculty, Grad_Student
from django.core.exceptions import ValidationError
from datetime import date
from django.utils.translation import gettext_lazy as _


currentYear = date.today().year
currentMonth = date.today().month
quater = {
  "1": [1, 2, 3],
  "2": [4, 5, 6],
  "3": [7, 8, 9],
  "4": [10, 11, 12]
}



class StudentAdminForm(forms.ModelForm):
  
    """
    Ensure minor and major field don't contain the same department.
    """
      
    def clean(self):
      cleaned_data = super().clean()
      minor = cleaned_data.get('minor')
      major = cleaned_data.get('major')
      
      if not minor or not major:
        return cleaned_data
      elif minor == major:
        text = _("A student can't have same department as minor and major")
        raise ValidationError(text)
      else:
         return cleaned_data
      




    
class GradAdminForm(forms.ModelForm):
  
  """
  Ensure that the year field is between 1900 to the previous year.
  Ensure the level field is always Graduate.
  """
  
  def clean_level(self):
    data = self.cleaned_data['level']
    if data == 'Cls 5':
      return data
    text = _('Field value can only be Graduate')
    raise ValidationError(text)
    
  def clean_year(self):
    data = self.cleaned_data["year"]
    if data <= currentYear-1 and data >= 1900:
      return data
    else:
      text = _("Year can only be between 1900 to")
      warn = "%s %s" % (text, currentYear-1)
      raise ValidationError(warn)
      
      


class ResearcherAdminForm(forms.ModelForm):
  
  """
  Ensure that a researcher is a valid faculty member or graduate student.
  """
  
  def clean(self):
    cleaned_data = super().clean()
    ssn = cleaned_data.get('ssn')
    
    member = Faculty.objects.filter(ssn=ssn) 
    if member:
      return cleaned_data
    
    graduate = Grad_Student.objects.filter(ssn=ssn)
    if graduate:
      return cleaned_data
      
    text = _("A researcher must be a faculty member or a graduate")
    raise ValidationError(text)
  
  
      

class SectionAdminForm(forms.ModelForm):
  
  """
  Ensure that the year field is between 1900 to the current year.
  Ensure that the grade field is always provided even though it has a blank and null attributes set to True.
  """
  
  def clean_year(self):
    data = self.cleaned_data["year"]
    if data <= currentYear and data >= 1900:
      return data
    else:
      text = _("Year can only be between 1900 to")
      warn = "%s %s" % (text, currentYear)
      raise ValidationError(warn)
      
  def clean_grade(self):
    data = self.cleaned_data["grade"]
    if data:
      return data
    else: 
      raise ValidationError("This field is required")
      



class CurrentSectionAdminForm(forms.ModelForm):
  
  """
  Ensure that only section with current year and current quater can be added to CurrentSection table.
  """
  
  def clean_year(self):
    data = self.cleaned_data['year']
    if data == currentYear:
       return data
    text = _("Year can only be current year")
    raise ValidationError(text)
  
  def clean_qtr(self):
    data = self.cleaned_data['qtr']
    if currentMonth in quater[data]:
       return data
    text = _("Quarter can only be current quater")
    raise ValidationError(text)
    

