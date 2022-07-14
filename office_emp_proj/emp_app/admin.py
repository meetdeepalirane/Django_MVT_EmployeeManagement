from django.contrib import admin
from . models import Department,Role,Employee,Feedback_Model,Employee_image,Registration
# Register your models here.
admin.site.register(Department)
admin.site.register(Role)
admin.site.register(Employee)
admin.site.register(Feedback_Model)
admin.site.register(Employee_image)
admin.site.register(Registration)