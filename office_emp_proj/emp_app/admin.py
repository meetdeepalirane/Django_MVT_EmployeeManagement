from django.contrib import admin
from . models import Department,Role,Employee,Feedback_Model,EmployeeImage,Registration
# Register your models here.
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Feedback_Model)
admin.site.register(EmployeeImage)
admin.site.register(Registration)