from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Login(User):
    pass

class Profile(models.Model):
    plain_pass = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    address = models.CharField(max_length=500, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    pincode = models.CharField(max_length=200, null=True)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'profile'

class School(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    school_name = models.CharField(max_length=200)
    role = models.CharField(max_length=200)
    learners = models.CharField(max_length=200)
    mobile = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    class Meta:
        db_table = 'school'

class Medium(models.Model):
    medium_name =  models.CharField(max_length=50)
    is_synced = models.IntegerField(null=True, default=0)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'medium'

    def __str__(self):
        return self.medium_name

class Section(models.Model):
    section_name = models.CharField(max_length=50)
    is_synced = models.IntegerField(null=True, default=0)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'section'

class Class(models.Model):
    class_name = models.CharField(max_length=100)
    medium = models.ForeignKey(Medium, null=True, on_delete=models.CASCADE)
    is_synced = models.IntegerField(null=True, default=0)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'class'

class ClassSection(models.Model):
    school_class = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'class_section'

class Parent(models.Model):
    mother_first_name =  models.CharField(max_length=100)
    mother_last_name = models.CharField(max_length=100, null=True)
    mother_mobile = models.CharField(max_length=200, null=True)
    mother_email = models.CharField(max_length=200, null=True)
    father_first_name =  models.CharField(max_length=100)
    father_last_name = models.CharField(max_length=100, null=True)
    father_mobile = models.CharField(max_length=200, null=True)
    father_email = models.CharField(max_length=200, null=True)
    
    class Meta:
        db_table = 'parent'

class Categories(models.Model):
    category_name = models.CharField(max_length=100)
    is_synced = models.IntegerField(null=True, default=0)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'categories'

class Student(models.Model):
    admission_no =models.CharField(max_length=200)
    roll_no = models.IntegerField()
    school_class = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    section = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=200)
    gender = models.CharField(max_length=40)
    dob = models.DateField()
    admission_data = models.DateField()
    address =models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=100)
    parent = models.ForeignKey(Parent, null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    category = models.ForeignKey(Categories, null=True, on_delete=models.CASCADE)
    is_synced = models.IntegerField(null=True, default=0)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user')

    class Meta:
        db_table = 'student'

class Department(models.Model):
    department_name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, null= True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'department'

class Designation(models.Model):
    designation_name = models.CharField(max_length=200)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'designation'

class Teacher(models.Model):
    staff_no = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    department = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    designation = models.ForeignKey(Designation, null=True, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    qualification = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    creator = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'teacher'

class APIs(models.Model):
    api_name = models.CharField(max_length=100)
    protocol = models.CharField(max_length=50, null=True)
    base_url = models.CharField(max_length=200, null=True)
    api_url = models.CharField(max_length=500, null=True)
    api_method = models.CharField(max_length=50, null=True)
    product_type = models.CharField(max_length=50, null=True)

    class Meta:
        db_table = 'apis'

class SessionManager(models.Model):
    token = models.CharField(max_length=1000)
    productType = models.CharField(max_length=100)
    user = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'session_manager'