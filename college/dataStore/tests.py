from django.test import TestCase
from .models import Person, Lecturer, Student, Grad_Student, Degree, Researcher, Grant, Support, Department, College, Course, Session, CurrentSession, OldSession

import datetime
birthday = datetime.datetime(1997, 6, 30)

class ModelTestCase(TestCase):
  def setUp(self):
    
    """
    create person objects.
    """
    personA = Person.objects.create(ssn="111222333", firstName="Ismail", middleName="Ahmad", lastName="Gbolahan", birthday=birthday, category="Lect", sex="M", aptNo=12, laneNo=3, street="hassan bello", city="ibadan", state="oyo", zipcode=2022)
    
    personB = Person.objects.create(ssn="111555333", firstName="Ismail", middleName="Ahmad", lastName="Gbolahan", birthday=birthday, category="Std", sex="M", aptNo=12, laneNo=3, street="hassan bello", city="ibadan", state="oyo", zipcode=2022)
    
    personC = Person.objects.create(ssn="111444333", firstName="Ismail", middleName="Ahmad", lastName="Gbolahan", birthday=birthday, category="Grad", sex="M", aptNo=12, laneNo=3, street="hassan bello", city="ibadan", state="oyo", zipcode=2022)
    
    

    
    
  def test_lecturer_table(self):
    
    personA = Person.objects.get(ssn="111222333")
    personC = Person.objects.get(ssn="111444333")
    
    lecturerA = Lecturer.objects.create(person=personA, rank="Ast", salary="D", officeAddress="futa obanla", officePhone="09094080107").save()
    
    lecturerB = Lecturer.objects.create(person=personC, rank="Vst", salary="D", officeAddress="futa obanla", officePhone="09094080107").save()
    
    text = "only lecturer can be added to this table"
    
    self.assertNotEqual(lecturerA, text)
    self.assertEqual(lecturerB, text)
    