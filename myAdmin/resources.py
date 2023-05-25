from import_export import resources
from myAdmin.models import Student

class StudentResource(resources.ModelResource):
    class Meta:
        model = Student()