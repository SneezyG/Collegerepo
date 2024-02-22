
"""
All form class are only for admin custom validation, nothing more, nothing less.
"""


from django import forms
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


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
     