from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AdminBase(models.Model):
    # class Meta:
    #     abstract = True
    pass

class Login(User):
    pass

class Section(AdminBase):
    section_name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'section'

class Class(AdminBase):
    class_name = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'class'

class ClassSection(AdminBase):
    class_id = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    section_id = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'class_section'

class Parent(AdminBase):
    mother_first_name =  models.CharField(max_length=100)
    mother_last_name = models.CharField(max_length=100, null=True)
    mother_mobile = models.CharField(max_length=200, null=True)
    father_first_name =  models.CharField(max_length=100)
    father_last_name = models.CharField(max_length=100, null=True)
    father_mobile = models.CharField(max_length=200, null=True)
    
    class Meta:
        db_table = 'parent'

class Student(AdminBase):
    admission_no =models.CharField(max_length=200)
    roll_no = models.IntegerField()
    class_id = models.ForeignKey(Class, null=True, on_delete=models.CASCADE)
    section_id = models.ForeignKey(Section, null=True, on_delete=models.CASCADE)
    academic_year = models.CharField(max_length=200)
    gender = models.CharField(max_length=40)
    dob = models.DateField()
    admission_data = models.DateField()
    address =models.CharField(max_length=200, null=True)
    mobile = models.CharField(max_length=100)
    parent_id = models.ForeignKey(Parent, null=True, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, null=True, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name='user')

    class Meta:
        db_table = 'student'

class Department(AdminBase):
    department_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, null= True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'department'

class Designation(AdminBase):
    designation_name = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'designation'

class Teacher(AdminBase):
    staff_no = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    department_id = models.ForeignKey(Department, null=True, on_delete=models.CASCADE)
    designation_id = models.ForeignKey(Designation, null=True, on_delete=models.CASCADE)
    gender = models.CharField(max_length=100)
    dob = models.DateField()
    qualification = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'teacher'