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
  
  it is a generalization of :model:`dataStore.Lecturer` and :model:`dataStore.Student`.
  
  There are two category of person(Lecturer and student)
  
  """
  
  sexType = (
      ('M', _('male')),
      ('F', _('female')),
      ('P', _('private')),
    )
  personType= (
      ("Lect", _("Lecturer")),
      ("Std", _("Student")),
      ("Grad", _("Graduate"))
    )

    
  ssn = models.CharField(max_length=11, primary_key=True, verbose_name=_('social security number'))
  firstName = models.CharField(max_length=30, verbose_name=_('first name'))
  middleName = models.CharField(max_length= 30,
  verbose_name=_('middle name')) 
  lastName = models.CharField(max_length=30, verbose_name=_('last name'))
  birthday = models.DateField(verbose_name=_('birthday'))
  category = models.CharField(max_length=4,
      choices=personType, verbose_name=_('category'))
  sex = models.CharField(max_length=1, choices=sexType, verbose_name=_('sex'))
  aptNo = models.IntegerField(verbose_name=_('apartment number'))
  laneNo = models.IntegerField(verbose_name=_('lane number'))
  street = models.CharField(max_length=30, verbose_name=_('street'))
  city = models.CharField(max_length=30, verbose_name=_('city'))
  state = models.CharField(max_length=30, verbose_name=_('state'))
  zipcode = models.IntegerField(verbose_name=_('zipcode'))
  
  
  def fullName(self):
    "Returns the person's full name."
    verbose_name=_('full name')
    fullname = '%s %s %s' % (self.firstName, self.middleName, self.lastName)
    return fullname.upper()
    
    
  def __str__(self):
    "Returns the person's full name."
    fullname = '%s %s %s(%s)' % (self.firstName, self.middleName, self.lastName, self.category)
    return fullname.title()
    
 
  def address(self):
    "Return the address of the person."
    verbose_name=_('address')
    address = 'no %s, lane %s, %s, %s, %s' % (self.aptNo, self.laneNo, self.street, self.city, self.state)
    return address.title()
    
  class Meta:
     verbose_name=_('Person')
    
    
    
class Lecturer(models.Model):
  
  """
  Stores a single lecturer data, 
  
  it is a specialization of :model:`dataStore.Person`.
  
  A person object must have it category as lecturer before it can be added to this table

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
    
    
  person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="lecturer", verbose_name=_('person'))
  rank = models.CharField(max_length=3,
       choices=rankType, verbose_name=_('rank'))
  salary = models.CharField(max_length=3, choices=salaryType, verbose_name=_('salary'))
  officeAddress = models.CharField(max_length=50, verbose_name=_('office address'))
  officePhone = models.CharField(max_length=15, verbose_name=_('office phone'))
  
  def fullName(self):
    "Returns the person's full name."
    verbose_name=_('full name')
    name = self.person
    fullname = '%s %s %s' % (name.firstName, name.middleName, name.lastName)
    return fullname.upper()
 
 
  def __str__(self):
    name = self.person
    fullname = '%s %s %s' % (name.firstName, name.middleName, name.lastName)
    return fullname.title()
  
  
  # over ride the save method 
  #@property
  def save(self, *args, **kwargs):
    if self.person.category == "Lect":
      # calling the real save method
      super().save(*args, **kwargs) 
    else:
      return "only lecturer can be added to this table"
      
  class Meta:
    verbose_name=_('Lecturer')
   

   
class Student(models.Model):
   """
    Stores a single student data.
    
    It is a specialization of :model:`dataStore.Person`.
    
    A person object must have it category as stude nt or graduate before it can be added to this table

    It is related to :model:`dataStore.Department` through minor and major relationship(many to one).
    
    It is related to :model:`dataStore.CurrentSession` through registered courses relationship(many to many).

    It is related to :model:`dataStore.OldSession` through transcript relationship(many to many).
    
    A student can't have a department as a minor and major at the same time.
    
   """
   
   clsType = (
    ("Cls 1", _("Freshman")),
    ("Cls 2", _("Sophomore")),
    ("Cls 3", _("Junior")),
    ("Cls 4", _("Senior")),
    ("Cls 5", _("Graduate"))
   )
   
   person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="student", verbose_name=_('person'))
   level = models.CharField(max_length=5, 
       choices=clsType, verbose_name=_('level'))
   minor = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, related_name="minor_students", verbose_name=_('minor'))
   major = models.ForeignKey("Department", on_delete=models.SET_NULL, null=True, related_name="major_students", verbose_name=_('major'))
   Reg = models.ManyToManyField("CurrentSession", related_name="students", verbose_name=_('Registered_courses'))
   trspt = models.ManyToManyField("OldSession", related_name="students", verbose_name=_('transcript'))
   
   
   def fullName(self):
      "Returns the person's full name."
      name = self.person
      verbose_name=_('full name')
      fullname = '%s %s %s' % (name.firstName, name.middleName, name.lastName)
      return fullname.upper()
   
   def __str__(self):
      name = self.person
      fullname = '%s %s %s(%s)' % (name.firstName, name.middleName, name.lastName, self.level)
      return fullname.title()
   
     
   # over ride the defaultsave method
   def save(self, *args, **kwargs):
    catg = self.person.category
    if catg == "Std" or catg == "grad":
      if catg == "grad" and self.level != "Cls 5":
        return "graduate must belong to level 5"
      elif catg == "std" and self.level == "Cls 5":
        return "student cannot belong to level 5"
      elif self.minor != self.major:
        super().save(*args, **kwargs) 
      else:
        return "a student can't have same department as minor and major"
    else:
      return "only students and graduates can be added to this table"
      
   class Meta:
     verbose_name=_('Student')
 
 
       

class Grad_Student(models.Model):
  
  """
    Stores a single graduate student data.
    
    It is a specialization of :model:`dataStore.Student`.
    
    Only class 5 student(graduate) can be added to this table.
    
    It is related to :model:`dataStore.Degree` through Previous degree relationship(many to many).
    
    It is related to :model:`dataStore.Lecturer` through advisor(many to one) and thesis committee(many to many) relationships

  """
  
  student = models.OneToOneField(Student, on_delete=models.CASCADE, 
      related_name="grad", verbose_name=_('Student'))
  degrees = models.ManyToManyField('Degree', verbose_name=_('degree'))
  advisor = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, null=True,
       related_name="advisee", verbose_name=_('advisor'))
  committee = models.ManyToManyField(Lecturer, related_name="thesis_student", verbose_name=_('committee'))
  
  
  
  def __str__(self):
    name = self.student.person
    fullname = '%s %s %s' % (name.firstName, name.middleName, name.lastName)
    return fullname.title()
    
    
  def fullName(self):
    "Returns the person's full name."
    verbose_name=_('full name')
    name = self.student.person
    fullname = '%s %s %s' % (name.firstName, name.middleName, name.lastName)
    return fullname.upper()
      
  # over ride the default save method
  def save(self, *args, **kwargs):
    if self.student.level == "Cls 5":
      # calling the real save method
      super().save(*args, **kwargs) 
    else:
      return "only graduate student can be added to this table"
      
  class Meta:
     verbose_name=_('Graduate')
  
  
  
  
class Degree(models.Model):
  
  """
  Store a single degree item for previous and old sessions.
  
  Every degree object have a year field that can only range from 1990 to previous year.
  
  Previous year = currentyear -1,
  where currentyear = date.today().year.
  
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
  
  def __str__(self):
    deg = '%s(%s)' % (self.degree, self.college)
    return deg
  
  # over ride the default save method
  def save(self, *args, **kwargs):
    if self.year <= currentYear-1 and self.year >= 1900:
      # calling the real save method
      super().save(*args, **kwargs) 
    else:
      return "year can only be between 1900 to %s year" % (currentYear-1)
  
  class Meta:
    verbose_name=_('Degree')
  
  

class Researcher(models.Model):
  
  """
  Store a single researcher data.
  
  It is the union of :model:`dataStore.lecturer` and :model:`dataStore.Grad_Student`.
  
  Every Researcher object have a person object which it was created with(one to one relationship)
  
  Only person_lecturer and person_student_grad_std can be added to this table.
  
  It is related to :model:`dataStore.Support` through Grant-support relationship(many to many).

  """
  
  person = models.OneToOneField(Person, 
      on_delete= models.CASCADE, verbose_name=_('person'))
  support = models.ManyToManyField("Support", verbose_name=_('support'))
         
  def __str__(self):
    name = self.person
    fullname = '%s %s %s(%s)' % (name.firstName, name.middleName, name.lastName)
    return fullname.title()
    
  def fullName(self):
     "Returns the person's full name."
     verbose_name=_('full name')
     name = self.person
     fullname = '%s %s %s' % (name.firstName, name.middleName, name.lastName)
     return fullname.upper()
    
  
  # over ride the default save method
  def save(self, *args, **kwargs):
    if self.person.category == "grad":
      if self.person.student:
        if self.person.student.grad:
          super().save(*args, **kwargs)
        else:
          return "this person is not a valid graduate"
      else:
        return "this person is not a valid graduate"
        
    elif self.person.category == "Lect":
      if self.person.lecturer:
        super().save(*args, **kwargs) 
      else:
        return "This person is not a valid lecturer"
        
    else:
      return "person must be a graduate or lecturer"
      
  class Meta:
    verbose_name=_('Researcher')
        
  
        
class Grant(models.Model):
  
  """
  This store a single grant data. 
  
  It is related to :model:`dataStore.Lecturer` through investigator relationship(many to one).
  
  """
  
  no = models.IntegerField(primary_key=True, verbose_name=_('number'))
  title = models.CharField(max_length=30, verbose_name=_('title'))
  agency = models.CharField(max_length=30, verbose_name=_('agency'))
  investigator = models.ForeignKey(Lecturer, 
      on_delete=models.CASCADE, verbose_name=_('investigator'))
      
  def __str__(self):
    name = '%s(%s)' % (self.title, self.agency)
    return name.title()
    
  class Meta:
    verbose_name=_('Grant')
      
      


class Support(models.Model):
  
  """
  This store a single support data.
  
  it is related to :model:`dataStore.Grant` through grant relationship(one to one).
  
  """
  
  grant = models.OneToOneField(Grant, on_delete=models.CASCADE, verbose_name=_('grant'))
  date = models.DateField(verbose_name=_('date'))
  end = models.DateField(verbose_name=_('end'))
  time = models.IntegerField(verbose_name=_('time'))
  
  def __str__(self):
    name = '%s, %s to %s' % (self.grant.agency, self.date, self.end)
    return name
    
  def agency(self):
    "return the agency awarding the grant"
    verbose_name=_('agency')
    return self.grant.agency.capitalize()
  
  class Meta:
    verbose_name=_('Support')
    



class Department(models.Model):
  
  """
  Store a single department data.
  
  It is related to :model:`dataStore.Lecturer` through lecturers(many to many) and HOD(one t one) relationship.
  
  It is related to :model:`dataStore.College` through college relationship(many to one).
  
  """
  
  Name = models.CharField(max_length=30, primary_key=True,verbose_name=_('name'))
  dphone = models.CharField(max_length=30, verbose_name=_('phone'))
  office = models.IntegerField(verbose_name=_('office number'))
  lecturers = models.ManyToManyField(Lecturer, related_name="departments", verbose_name=_('lecturer'))
  HOD = models.OneToOneField(Lecturer, related_name="HOD_of", on_delete=models.CASCADE, verbose_name=_('Head of department'))
  college = models.ForeignKey("College", on_delete=models.CASCADE, related_name="departments", verbose_name=_('college'))
  
  def __str__(self):
    return self.Name
  
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
  
  name = models.CharField(max_length=30, choices=clgType, verbose_name=_('name'), unique=True)
  dean = models.CharField(max_length=30, unique=True, verbose_name=_('dean'))
  office = models.IntegerField(verbose_name=_("office number"))
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name=_('College')
    
    
  
  
class Course(models.Model):
  
  """
  
  Store a single course data.
  
  It is related to :model:`dataStore.Department` through department relationship(many to one).

  """
  
  no = models.IntegerField(primary_key=True, verbose_name=_('number'))
  name = models.CharField(max_length=30, unique=True, verbose_name=_('name'))
  Dept = models.ForeignKey(Department, on_delete=models.CASCADE, verbose_name=_('department'))
  des = models.TextField(verbose_name=_('description'))
  
  def __str__(self):
    return self.name
  
  class Meta:
    verbose_name=_('Course')
    
    
 
  
class Session(models.Model):
  
  """
  Store a particular session versions of courses.
  
  It is related to :model:`dataStore.Course` through course relationship(many to one).
  
  It is related to :model:`dataStore.Researcher` through teacher relationship(many to one).
  
  Every session object have a year field that can only range from 1990 to currentyear.
   
  where current year = date.today().year.
  
  """
  
  qtrType = (
      ("1", _("First Quarter")),
      ("2", _("Second Quarter")),
      ("3", _("Third Quarter")),
      ("4", _("Fourth Quarter"))
    )
  no = models.IntegerField(primary_key=True, verbose_name=_('number'))
  year = models.IntegerField(verbose_name=_('year'))
  qtr = models.CharField(max_length=1, choices=qtrType, verbose_name=_('quarter'))
  course = models.ForeignKey(Course, on_delete=models.SET_NULL, null=True, verbose_name=_('course'))
  teacher = models.ForeignKey(Researcher, on_delete=models.SET_NULL, null=True, verbose_name=_('teacher'))
  
  def __str__(self):
    sect = '%s (%s, %s)' % (self.course.name, self.qtr, self.year)
    return sect

  def name(self):
    verbose_name=_('name')
    return course.name.capitalize()
  
  # over ride the default save method
  def save(self, *args, **kwargs):
    if self.year <= currentYear and self.year >= 1900:
      # calling the real save method
      super().save(*args, **kwargs) 
    else:
      return "year can only be between 1900 to %s" % (currentYear)
      
  class Meta:
    verbose_name=_('Session')
    
    
 
    
class CurrentSession(models.Model):
  
   """
   Store the current session version of courses.
   
   It is a specialization of :model:`dataStore.Session`
   
   A session object must have it year field as currentyear before it can be added to this table.
   
   A session object must have it quarter field
     as currentQuarter of the year before it can be added to this table.
     
   Currentyear = data.today().year
   CurrentQuarter = date.today()month in selected Quarter.
   
   """
  
   session = models.OneToOneField(Session, on_delete=models.CASCADE, verbose_name=_('session'))
   
   
   def __str__(self):
      sect = '%s (%s, %s)' % (self.session.course.name, self.session.qtr, self.session.year)
      return sect

   def course(self):
     verbose_name=_('course')
     return self.session.course.name.capitalize()
     
   def teacher(self):
     verbose_name=_('teacher')
     return self.session.course.teacher.capitalize()
    
   # over ride the default save method
   def save(self, *args, **kwargs):
     year = self.session.year
     qtr = self.session.qtr
     if year == currentYear and currentMonth in quater[qtr]:
      super().save(*args, **kwargs) 
     else:
      return "cannot add session to this table"
  
   class Meta:
     verbose_name=_('Current Session')
     
     
 
  
class OldSession(models.Model):
  
   """
   Store the old session versions of courses. 
   
   It is a specialization of :model:`dataStore.Session`

   Every session object have a year field that can only range from 1990 to previousyear.
   
   previousyear = currentyear-1
   currentyear = data.today().year
   
   """
   
   gradeType = (
       ("A", _("Distinction")),
       ("B", _("Very good")),
       ("C", _("Good")),
       ("D", _("Poor")),
       ("E", _("Pass")),
       ("F", _("Fail"))
     )
   session = models.ForeignKey(Session, on_delete=models.CASCADE, verbose_name=_('session'))
   grade = models.CharField(max_length=1, choices=gradeType, verbose_name=_('grade'))
   
   def course(self):
     verbose_name=_('course')
     return self.session.course.name.capitalize()
     
   def teacher(self):
     verbose_name=_('teacher')
     return self.session.course.teacher.capitalize()
   
   def year(self):
     verbose_name=_('year')
     return self.session.qtr()
     
   def quarter():
     verbose_name=_('quarter')
     return self.session.qtr()
   
   def __str__(self):
      sect = '%s (%s, %s)' % (self.session.course.name, self.session.qtr, self.session.year)
      return sect
   
   # over ride the default save method
   def save(self, *args, **kwargs):
     year = self.session.year
     if year <= currentYear-1 and year >= 1900:
       super().save(*args, **kwargs) 
     else:
      return "only old session can be added"

   class Meta:
     verbose_name=_('Old Session')
  

  

    