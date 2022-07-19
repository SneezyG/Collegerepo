from django.db import models
from datetime import date

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
  sexType = (
      ('M', 'male'),
      ('F', 'female')
      ('P', 'private')
    )
  personType= (
      ("Lect", "Lecturer"),
      ("Std", "Student")
    )
    
  ssn = models.CharField(max_length=11, primary_key=True, db_column="social security no")
  firstName = models.CharField(max_length=30)
  middleName = models.CharField(max_length= 30) 
  lastName = models.CharField(max_length=30)
  birthday = models.DateField()
  category = models.CharField(max_length=4,
      choices=personType)
  sex = models.CharField(max_length=1, choices=sexType)
  aptNo = models.IntegerField(db_column="apartment no")
  laneNo = models.IntegerField(db_column="lane no")
  street = models.CharField(max_length=30)
  city = models.CharField(max_length=30)
  state = models.CharField(max_length=30)
  zipcode = models.IntegerField()
  
 

  @property
  def fullName(self):
    "Returns the person's full name."
    fullname = '%s %s %s' % (self.firstName, self.middleName, self.lastName)
    return fullname.upper()
    
  @property
  def address(self):
    "Return the address of the person."
    address = 'no %s, lane %s, %s, %s, %s' % (self.aptNo, self.laneNo, self.street, self.city, self.state)
    return address.title()
    
    
    
class Lecturer(models.Model):
  rankType = (
      ('Ast', 'Assistance'),
      ('Asc', 'Associate'),
      ('Adj', 'Adjunct'),
      ('Res', 'Research'),
      ('Vst', 'Visiting')
    )
  person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="lecturer")
  rank = models.CharField(max_length=3,
       choices=rankType)
  salary = models.IntegerField(max_length=30, db_column="salary in $")
  officeAddress = models.CharField(max_length=50)
  officePhone = models.CharField(max_length=15)
  
  # over ride the save method
  def save(self, *args, **kwargs):
    if self.person.category == "Lect":
      # calling the real save method
      super().save(*args, **kwargs) 
    else:
      return "only lecturer can be added to this table"
   
   
   
class Student(models.Model):
  clsType = (
    ("Cls 1", "Freshman"),
    ("Cls 2", "Sophomore"),
    ("Cls 3", "Junior"),
    ("Cls 4", "Senior"),
    ("Cls 5", "Graduate")
   )
   person = models.OneToOneField(Person, on_delete=models.CASCADE, related_name="student")
   level = models.CharField(max_length=5, 
       choices=clsType)
   minor = models.ForeignKey("Department", on_delete=models.SET_NULL, nullable=True, db_column="minor department")
   major = models.ForeignKey("Department", on_delete=models.SET_NULL, nullable=True, db_column="major department")
   Reg = models.ManyToManyField("CurrentSession",
     db_column="Registered courses", related_name="students", nullable=True)
   trspt = models.ManyToManyField("OldSession", db_column="transcript", related_name="students", nullable=True)
   
  
  # over ride the defaultsave method
  def save(self, *args, **kwargs):
    if self.person.category == "Std":
      if self.minor != self.major:
        super().save(*args, **kwargs) 
      else:
        return "a student can't have same department as minor and major"
    else:
      return "only students can be added to this table"
       

class Grad_Student(models.Model):
  
  student = models.OneToOneField(Student, on_delete=models.CASCADE, 
      related_name="grad")
  degrees = models.ManyToManyField('Degree', 
      db_column='Previous Degree')
  advisor = models.ForeignKey(Lecturer, on_delete=models.SET_NULL, nullable=True,
       related_name="advisee")
  committee = models.ManyToManyField(Lecturer, db_column="thesis committee", nullable=True, 
      related_name="thesis student")
      
  # over ride the default save method
  def save(self, *args, **kwargs):
    if self.student.level == "Cls 5":
      # calling the real save method
      super().save(*args, **kwargs) 
    else:
      return "only graduate student can be added to this table"
  
  
  
  
class Degree(models.Model):
  degType = (
      ("Asc", "Associate degree"),
      ("Bch", "Bachelor's degree"),
      ("Mas", "Master's degree"),
      ("Doc", "Doctoral degree")
    )
  clgType = (
      ("Sci", "Science"),
      ("Eng", "Engineering"),
      ("Agric", "Agriculture"),
      ("Med", "Medicine")
      ("Econ", "Economic")
      ("Gns", "General studies")
    )
  college = models.CharField(max_length=5, choices=clgType)
  degree = models.CharField(max_length=3, 
        choices=degType)
  year = models.IntegerField(min_value=1900, max_value=currentYear-1, db_column="year(1990-yyyy)")
  
  # over ride the default save method
  def save(self, *args, **kwargs):
    if self.year <= currentYear-1 and self.year >= 1900:
      # calling the real save method
      super().save(*args, **kwargs) 
    else:
      return "year can only be between 1900 to %s year" % (currentYear-1)
  
  

class Researcher(models.Model):
  person = models.OneToOneField(Person, 
      on_delete= models.CASCADE)
  support = models.ManyToManyField("Support", 
         db_column="Grant support")
  
  # over ride the default save method
  def save(self, *args, **kwargs):
    if self.person.category == "Std":
      if self.person.student:
        if self.person.student.grad:
          super().save(*args, **kwargs)
        else:
          return "this person is not a valid graduate"
      else:
        return "this person is not a valid student"
        
    if self.person.category == "Lect":
      if self.person.lecturer:
        super().save(*args, **kwargs) 
      else:
        return "This person is not a valid lecturer"
        
        
class Grant(models.Model):
  no = models.IntegerField(primary_key=True, db_column="Grant no")
  title = models.CharField(max_length=30)
  agency = models.CharField(max_length=30)
  investigator = models.ForeignKey(Lecturer, 
      on_delete=models.CASCADE)
      
      

class Support(models.Model):
  grant = models.OneToOneField(Grant, on_delete=models.CASCADE)
  date = models.DateField(db_column="Starting Date")
  end = models.DateField(db_column="End Date")
  time = models.IntegerField(db_column="time spent in %")
  
  

class Department(models.Model):
  Name = models.CharField(max_length=30, primary_key=True, db_column="Department Name")
  dphone = models.CharField(max_length=30, db_column=" Office Telephone")
  office = models.IntegerField(db_column="Office no")
  lecturers = models.ManyToManyField(Lecturer, related_name="departments")
  HOD = models.OneToOneField(Lecturer, related_name="HOD of", on_delete=models.CASCADE)
  college = models.ForeignKey("College", on_delete=models.CASCADE, related_name="departments")
  
  
  
class College(models.Model):
  name = models.CharField(max_length=30, primary_key=True, db_column="College Name")
  dean = models.CharField(max_length=30, db_column="Dean Name", unique=True)
  office = models.IntegerField(db_column="Office no")
  
  
class Course(models.Model):
  no = models.IntegerField(primary_key=True, db_column="Course no")
  name = models.CharField(max_length=30, db_column="Course Name"  unique=True)
  Dept = models.ForeignKey(Department, on_delete=models.CASCADE, db_column=)
  des = models.TextField(db_column="Course Description")
  
  
class Session(models.Model):
     
  qtrType = (
      ("1", "First Quarter"),
      ("2", "Second Quarter"),
      ("3", "Third Quarter"),
      ("4", "Fourth Quarter")
    )
  no = models.IntegerField(primary_key=True, db_column="Section no")
  year = models.IntegerField(max_value=currentYear, min_value=1900)
  qtr = models.CharField(max_length=1, choices=qtrType, db_column="Quarter")
  course = models.ForeignKey(Course, on_delete=models.SET_NULL, nullable=True)
  teacher = models.ForeignKey(Researcher, on_delete=models.SET_NULL, nullable=True)
  
  # over ride the default save method
  def save(self, *args, **kwargs):
    if self.year <= currentYear and self.year >= 1900:
      # calling the real save method
      super().save(*args, **kwargs) 
    else:
      return "year can only be between 1900 to %s" % (currentYear)
      
     
class CurrentSession(models.Model):
   session = models.OneToOneField(Session, on_delete=models.CASCADE)
    
   # over ride the default save method
   def save(self, *args, **kwargs):
     year = self.session.year
     qtr = self.session.qtr
     if year == currentYear and currentMonth in quater[qtr]:
      super().save(*args, **kwargs) 
     else:
      return "cannot add old session to this table"
  
  
  
class OldSession(models.Model):
   gradeType = (
       ("A", "Distinction"),
       ("B", "Very good"),
       ("C", "Good"),
       ("D", "Poor"),
       ("E", "Pass"),
       ("F", "Fail")
     )
   session = models.ForeignKey(Session, on_delete=models.CASCADE)
   grade = models.CharField(max_length=1, choices=gradeType)
   
   # over ride the default save method
   def save(self, *args, **kwargs):
     year = self.session.year
     if year <= currentYear-1 and year >= 1900:
       super().save(*args, **kwargs) 
     else:
      return "only old session can be added"


  
  

  

    