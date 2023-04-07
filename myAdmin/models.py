from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class AdminBase(models.Model):
    # class Meta:
    #     abstract = True
    pass

class Login(User):
    pass

class Class(AdminBase):
    class_name = models.CharField(max_length=100)
    section_id = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'class'

class Section(AdminBase):
    section_name = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, null=True, on_delete=models.CASCADE)

    class Meta:
        db_table = 'section'

