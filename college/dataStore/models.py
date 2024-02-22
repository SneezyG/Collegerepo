from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.

class Person(models.Model):
  
  """
  Stores person data. 
  
  it is a generalization of :model:`dataStore.Lecturer` and :model:`dataStore.Student`.
  """
  
  sexType = (
      ('M', _('male')),
      ('F', _('female')),
      ('P', _('private')),
    )
    
  first_name = models.CharField(max_length=30, verbose_name=_('first name'))
  middle_name = models.CharField(max_length= 30,
  verbose_name=_('middle name')) 
  last_name = models.CharField(max_length=30, verbose_name=_('last name'))
  birthday = models.DateField(verbose_name=_('birthday'))
  sex = models.CharField(max_length=1, choices=sexType, verbose_name=_('sex'))
  apt_no = models.IntegerField(verbose_name=_('apartment number'))
  lane_no = models.IntegerField(verbose_name=_('lane number'))
  street = models.CharField(max_length=30, verbose_name=_('street'))
  city = models.CharField(max_length=30, verbose_name=_('city'))
  state = models.CharField(max_length=30, verbose_name=_('state'))
  zipcode = models.IntegerField(verbose_name=_('zipcode'))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def fullName(self):
    "Returns the person's full name."
    verbose_name=_('full name')
    fullname = '%s %s %s' % (self.first_name, self.middle_name, self.last_name)
    return fullname.upper()
    
    
  def __str__(self):
    fullname = self.fullName()
    return fullname.title()
    
 
  def address(self):
    "Return the address of the person."
    verbose_name=_('address')
    address = 'no %s, lane %s, %s, %s, %s' % (self.apt_no, self.lane_no, self.street, self.city, self.state)
    return address.title()
    
  class Meta:
     verbose_name=_('Person')
    
    
   
   
    
class Lecturer(Person):
  
  """
  Stores Lecturers data, 
  
  it is a specialization of :model:`dataStore.Person`.
  
  It is related to :model:`dataStore.Department` through department relationship(many to one).
  """
  
  rankType = (
      ('Ast', _('Assistance')),
      ('Asc', _('Associate')),
      ('Adj', _('Adjunct')),
      ('Res', _('Research')),
      ('Vst', _('Visiting'))
    )
    
  salaryType = (
      ('A', _('Below $30,000')),
      ('B', _('$30,000 - $60,000')),
      ('C', _('$61,000 - $90,000')),
      ('D', _('$90,000 - $120,000')),
      ('E', _('Above $120,000'))
   )
    
    
  rank = models.CharField(max_length=3,
       choices=rankType, verbose_name=_('rank'))
  salary = models.CharField(max_length=3, choices=salaryType, verbose_name=_('salary'))
  office_address = models.CharField(max_length=50, verbose_name=_('office address'))
  office_phone = models.CharField(max_length=15, verbose_name=_('office phone'))
  department = models.ForeignKey("Department",  related_name="lecturers", verbose_name=_('department'), on_delete=models.SET_NULL, null=True, blank=True,)
  
  def __str__(self):
    fullname = '%s(%s)' % (self.fullName(), self.get_rank_display())
    return fullname.title()
  
      
  class Meta:
    verbose_name=_('Lecturer')
  
   

   
class Student(Person):
  
   """
    Stores students data.
    
    It is a specialization of :model:`dataStore.Person`.

    It is related to :model:`dataStore.Department` through minor and major relationship(many to one).
    
    A student can't have same department as a minor and major at the same time.
    
   """
   
   clsType = (
    ("Cls 1", _("Freshman")),
    ("Cls 2", _("Sophomore")),
    ("Cls 3", _("Junior")),
    ("Cls 4", _("Senior")),
    ("Cls 5", _("Graduate"))
   )
   
   level = models.CharField(max_length=5, 
       choices=clsType, verbose_name=_('Class'))
   minor = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True, related_name="minor_students", verbose_name=_('minor'))
   major = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, blank=True, related_name="major_students", verbose_name=_('major'))
   
   
   def __str__(self):
      fullname = '%s(%s)' % (self.fullName(), self.get_level_display())
      return fullname.title()
   
      
   class Meta:
     verbose_name=_('Student')
 
 
       



class Department(models.Model):
  
  """
  Store departments data.
  
  It is related to :model:`dataStore.Faculty` through faculty relationship(many to one).
  
  """
  
  name = models.CharField(max_length=30, primary_key=True, verbose_name=_('name'))
  phone_no = models.CharField(max_length=30, verbose_name=_('phone'))
  office_no = models.IntegerField(verbose_name=_('office number'))
  faculty = models.ForeignKey("Faculty", on_delete=models.CASCADE, related_name="departments", verbose_name=_('faculty'))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    return self.name.title()
  
  class Meta:
    verbose_name=_('Department')
    
 
 
    
class Faculty(models.Model):
  
  """
  Store faculties data.
  
  It have a unique field "dean of the college".
  """
  
  clgType = (
      ("Sci", _("Science")),
      ("Eng", _("Engineering")),
      ("Agric", _("Agriculture")),
      ("Med", _("Medicine")),
      ("Econ", _("Economic")),
      ("Gns", _("General studies"))
    )
  
  name = models.CharField(max_length=30, primary_key=True, choices=clgType, verbose_name=_('name'))
  dean = models.CharField(max_length=30, unique=True, verbose_name=_('dean'))
  phone_no = models.CharField(max_length=30, verbose_name=_('phone'))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    text = "faculty of %s" % (self.get_name_display())
    return text
  
  class Meta:
    verbose_name=_('Faculty')
  

    