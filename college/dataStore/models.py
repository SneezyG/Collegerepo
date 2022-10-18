from django.db import models
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

# Create your models here.

class Person(models.Model):
  
  """
  Stores a single person data. 
  
  it is a generalization of :model:`dataStore.Faculty` and :model:`dataStore.Student`.
  """
  
  sexType = (
      ('M', _('male')),
      ('F', _('female')),
      ('P', _('private')),
    )
    
  ssn = models.CharField(max_length=11, primary_key=True, verbose_name=_('social security number'))
  firstName = models.CharField(max_length=30, verbose_name=_('first name'))
  middleName = models.CharField(max_length= 30,
  verbose_name=_('middle name')) 
  lastName = models.CharField(max_length=30, verbose_name=_('last name'))
  birthday = models.DateField(verbose_name=_('birthday'))
  sex = models.CharField(max_length=1, choices=sexType, verbose_name=_('sex'))
  aptNo = models.IntegerField(verbose_name=_('apartment number'))
  laneNo = models.IntegerField(verbose_name=_('lane number'))
  street = models.CharField(max_length=30, verbose_name=_('street'))
  city = models.CharField(max_length=30, verbose_name=_('city'))
  state = models.CharField(max_length=30, verbose_name=_('state'))
  zipcode = models.IntegerField(verbose_name=_('zipcode'))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def fullName(self):
    "Returns the person's full name."
    verbose_name=_('full name')
    fullname = '%s %s %s' % (self.firstName, self.middleName, self.lastName)
    return fullname.upper()
    
    
  def __str__(self):
    fullname = self.fullName()
    return fullname.title()
    
 
  def address(self):
    "Return the address of the person."
    verbose_name=_('address')
    address = 'no %s, lane %s, %s, %s, %s' % (self.aptNo, self.laneNo, self.street, self.city, self.state)
    return address.title()
    
  class Meta:
     verbose_name=_('Person')
    
    
   
   
    
class Faculty(Person):
  
  """
  Stores a single Faculty member data, 
  
  it is a specialization of :model:`dataStore.Person`.
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
  officeAddress = models.CharField(max_length=50, verbose_name=_('office address'))
  officePhone = models.CharField(max_length=15, verbose_name=_('office phone'))
  
  def __str__(self):
    fullname = '%s(%s)' % (self.fullName(), self.get_rank_display())
    return fullname.title()
  
      
  class Meta:
    verbose_name=_('Faculty')
  
   

   
class Student(Person):
  
   """
    Stores a single student data.
    
    It is a specialization of :model:`dataStore.Person`.

    It is related to :model:`dataStore.Department` through minor and major relationship(many to one).
    
    It is related to :model:`dataStore.CurrentSection` through registered courses relationship(many to many).

    It is related to :model:`dataStore.Section` through transcript relationship(many to many).
    
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
   Reg = models.ManyToManyField("CurrentSection", related_name="students", verbose_name=_('Registered_courses'))
   trspt = models.ManyToManyField("Section", related_name="students", verbose_name=_('transcript'))
   
   
   def __str__(self):
      fullname = '%s(%s)' % (self.fullName(), self.get_level_display())
      return fullname.title()
   
      
   class Meta:
     verbose_name=_('Student')
 
 
       

class Grad_Student(Student):
  
  """
    Stores a single graduate student data.
    
    It is a specialization of :model:`dataStore.Student`.
    
    It is related to :model:`dataStore.Faculty` through advisor(many to one) and thesis committee(many to many) relationships
  """
  
  degType = (
      ("Asc", _("Associate degree")),
      ("Bch", _("Bachelor's degree")),
      ("Mas", _("Master's degree")),
      ("Doc", _("Doctoral degree"))
    )
    
  clgType = (
      ("Sci", _("Science")),
      ("Eng", _("Engineering")),
      ("Agric", _("Agriculture")),
      ("Med", _("Medicine")),
      ("Econ", _("Economic")),
      ("Gns", _("General studies"))
    )
    
  college = models.CharField(max_length=5, choices=clgType, verbose_name=_('college'))
  degree = models.CharField(max_length=3, 
        choices=degType, verbose_name=_('degree'))
  year = models.IntegerField(verbose_name=_('year'))
  advisor = models.ForeignKey(Faculty, on_delete=models.SET_NULL, null=True, blank=True, related_name="advisee", verbose_name=_('advisor'))
  committee = models.ManyToManyField(Faculty, related_name="thesis_student", verbose_name=_('thesis committee'))
 
 
  def __str__(self):
      fullname = '%s(%s)' % (self.fullName(), self.get_degree_display())
      return fullname.title()
    
      
  class Meta:
     verbose_name=_('Graduate')
  
  
  
  
  

class Researcher(models.Model):
  
  """
  Store a single researcher data.
  
  It is the union of :model:`dataStore.Faculty` and :model:`dataStore.Grad_Student`.
  
  It is related to :model:`dataStore.Grant` through support relationship(many to many).

  """
  
  ssn = models.CharField(max_length=11, primary_key=True, verbose_name=_('social security number'))
  firstName = models.CharField(max_length=30, verbose_name=_('first name'))
  middleName = models.CharField(max_length= 30,
  verbose_name=_('middle name')) 
  lastName = models.CharField(max_length=30, verbose_name=_('last name'))
  support = models.ManyToManyField("Grant", verbose_name=_('support'))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def fullName(self):
    "Returns the researcher's full name."
    verbose_name=_('full name')
    fullname = '%s %s %s' % (self.firstName, self.middleName, self.lastName)
    return fullname.upper()
    
  def __str__(self):
    fullname = self.fullName()
    return fullname.title()
        
      
  class Meta:
    verbose_name=_('Researcher')
        
  
  
  
        
class Grant(models.Model):
  
  """
  This store a single grant data. 
  
  It is related to :model:`dataStore.Faculty` through investigator relationship(many to one).
  
  """
  
  title = models.CharField(max_length=30, verbose_name=_('title'))
  agency = models.CharField(max_length=30, verbose_name=_('agency'))
  investigator = models.ForeignKey(Faculty, 
      on_delete=models.CASCADE, verbose_name=_('investigator'))
  start = models.DateField(verbose_name=_('start date'))
  end = models.DateField(verbose_name=_('end date'))
  spend = models.IntegerField(verbose_name=_('%time spend'))
  time = models.DateTimeField(auto_now_add=True)
      
  def __str__(self):
    name = '%s(%s)' % (self.title, self.agency)
    return name.title()
    
  class Meta:
    verbose_name=_('Grant')
      
      




class Department(models.Model):
  
  """
  Store a single department data.
  
  It is related to :model:`dataStore.Faculty` through belong(many to many) and HOD(one to one) relationship.
  
  It is related to :model:`dataStore.College` through college relationship(many to one).
  
  """
  
  name = models.CharField(max_length=30, primary_key=True, verbose_name=_('name'))
  dphone = models.CharField(max_length=30, verbose_name=_('phone'))
  office = models.IntegerField(verbose_name=_('office number'))
  belongs = models.ManyToManyField(Faculty, related_name="departments", verbose_name=_('belongs'))
  HOD = models.OneToOneField(Faculty, related_name="HOD_of", on_delete=models.CASCADE, verbose_name=_('Head of department'))
  college = models.ForeignKey("College", on_delete=models.CASCADE, related_name="departments", verbose_name=_('college'))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    return self.name.title()
  
  class Meta:
    verbose_name=_('Department')
    
 
 
    
class College(models.Model):
  
  """
  Store a single college data.
  
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
  
  name = models.CharField(max_length=30, primary_key=True, choices=clgType, verbose_name=_('college'))
  dean = models.CharField(max_length=30, unique=True, verbose_name=_('dean'))
  office = models.IntegerField(verbose_name=_("office number"))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    text = "college of %s" % (self.get_name_display())
    return text
  
  class Meta:
    verbose_name=_('College')
    
    
  
  
class Course(models.Model):
  
  """
  
  Store a single course data.
  
  It is related to :model:`dataStore.Department` through department relationship(many to one).

  """
  
  code = models.CharField(max_length=30, primary_key=True, verbose_name=_('course code'))
  name = models.CharField(max_length=30, unique=True, verbose_name=_('name'))
  dept = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name=_('department'))
  des = models.TextField(verbose_name=_('description'))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    text = "%s(%s)" % (self.name, self.code)
    return text
  
  class Meta:
    verbose_name=_('Course')
    
    
 
  
class Section(models.Model):
  
  """
  Store a particular Section versions of courses.
  
  It is related to :model:`dataStore.Course` through course relationship(many to one).
  
  It is related to :model:`dataStore.Researcher` through teacher relationship(many to one).
  
  Every Section object have a year field that can only range from 1990 to currentyear.
   
  where current year = date.today().year.
  
  """
  
  qtrType = (
      ("1", _("First Quarter")),
      ("2", _("Second Quarter")),
      ("3", _("Third Quarter")),
      ("4", _("Fourth Quarter"))
    )
  
  gradeType = (
      ("1", _("Excellent")),
      ("2", _("Good")),
      ("3", _("Pass")),
      ("4", _("Fail"))
    )
    
  year = models.IntegerField(verbose_name=_('year'))
  qtr = models.CharField(max_length=1, choices=qtrType, verbose_name=_('quarter'))
  grade = models.CharField(max_length=1, choices=gradeType, null=True, blank=True, verbose_name=_('grade'))
  course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('course'))
  teacher = models.ForeignKey(Researcher, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_('teacher'))
  time = models.DateTimeField(auto_now_add=True)
  
  
  def __str__(self):
    sect = '%s (%s, %s)' % (self.course.name, self.get_qtr_display(), self.year)
    return sect

  def name(self):
    verbose_name=_('name')
    return self.course.name.title()
 
      
  class Meta:
    verbose_name=_('Section')
    
    
 
    
class CurrentSection(Section):
  
   """
   Store the current Section version of courses.
   
   It is a specialization of :model:`dataStore.Section`
   
   A Section object must have it year field as currentyear before it can be added to this table.
   
   A Section object must have it quarter field
     as currentQuarter of the year before it can be added to this table.
     
   Currentyear = data.today().year
   CurrentQuarter = date.today()month in selected Quarter.
   
   """
   
  
   class Meta:
     verbose_name=_('Current Section')
     
     

  

    