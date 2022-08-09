from django import forms
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

"""
All form class are only for admin form custom validation, nothing more, nothing less
"""

class LecturerAdminForm(forms.ModelForm):
    """
    ensure that only person object with lecturer category are added to the lecturer table.
    """
    
    def clean_person(self):
      data = self.cleaned_data["person"]
      if data.category != "Lect":
        text= _("only lecturer can be added to this table")
        raise ValidationError(text)
  
      return data


class StudentAdminForm(forms.ModelForm):
    """
    ensure that only person object with student or graduate category can be added to the student table.
    
    ensure the level of person object with graduate category is 5.
    
    ensure the level of person object with student category is not 5.
    
    ensure minor and major field don't contain the same department.
    """
    
    def clean(self):
      cleaned_data = super().clean()
      catg = cleaned_data.get('person').category
      minor = cleaned_data.get('minor')
      major = cleaned_data.get('major')
      level = cleaned_data.get('level')
      if catg == "Std" or catg == "grad":
        if catg == "grad" and level != "Cls 5":
          text = _('graduate must belong to level 5')
          raise ValidationError(text)
        elif catg == "std" and self.level == "Cls 5":
           text = _("student cannot belong to level 5")
           raise ValidationError(text)
        elif self.minor == self.major:
          text = _("a student can't have same department as minor and major")
          raise ValidationError(text)
        else:
           return cleaned_data
      else:
        text = _("only students and graduates can be added to this table")
        raise ValidationError(text)



class Grad_StudentAdminForm(forms.ModelForm):
  """
  ensure that only graduate student are added to this table.
  """
  
  def clean_student(self):
    data = self.cleaned_data["student"]
    if data.level != "Cls 5":
      text = _("only graduate student can be added to this table")
      raise ValidationError(text)
    
    return data
    
    
class DegreeAdminForm(forms.ModelForm):
  """
  ensure that the year field is between 1900 to the previous year.
  """
  
  def clean_year(self):
    data = self.cleaned_data["year"]
    if data <= currentYear-1 and data >= 1900:
      return data
    else:
      text = _("year can only be between 1900 to")
      warn = "%s %s" % (text, currentYear-1)
      raise ValidationError(warn)
      


class ResearcherAdminForm(forms.ModelForm):
  """
  ensure the person field actually contain a valid graduate or lecturer object.
  """
  
  def clean_person(self):
    data = self.cleaned_data["person"]
    if data.category == "grad":
      if data.student:
        if not data.student.grad:
          text = _("this person is not a valid graduate")
          raise ValidationError(text)
        return data
      else:
        text = _("this person is not a valid graduate")
        raise ValidationError(text)
        
    elif data.category == "Lect":
      if not data.lecturer:
        text = _("This person is not a valid lecturer")
        raise ValidationError(text)
      return data

    else:
      text = _("person must be a graduate or lecturer")
      raise ValidationError(text)
      

class SessionAdminForm(forms.ModelForm):
  """
  ensure that the year field is between 1900 to the current year.
  """
  
  def clean_year(self):
    data = self.cleaned_data["year"]
    if data <= currentYear and data >= 1900:
      return date
    else:
      text = _("year can only be between 1900 to")
      warn = "%s %s" % (text, currentYear)
      raise ValidationError(warn)
      

class CurrentSessionAdminForm(forms.ModelForm):
  """
  ensure that only session with current year and current quater can be added to this table.
  """
  
  def clean(self):
    cleaned_data = super().clean()
    year = cleaned_data.get('session').year
    qtr = cleaned_data.get('session').qtr
    if year != currentYear and currentMonth not in quater[qtr]:
      text = _("cannot add session because it is not current")
      raise ValidationError(text)
    return clean_data
    

class OldSessionAdminForm(forms.ModelForm):
  """
  ensure that the session is not current.
  """
  
  def clean_session(self):
    data = self.clean_data['session'].year
    if data <= currentYear-1 and data >= 1900:
       return data
    else:
      text = _("only old session can be added")
      raise ValidationError(text)

