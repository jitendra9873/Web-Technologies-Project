from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Student)
admin.site.register(Course)
admin.site.register(Subject)
admin.site.register(Student_attendance)
admin.site.register(Follow)