from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
import uuid
import os
# Create your models here.

class Course(models.Model):
    coursename= models.CharField(max_length=100, blank=True, null=True)
    description=models.CharField(max_length=500, blank=True, null=True)
    course_ka_photo = models.ImageField(default='media/lol.jpg', blank=True, null=True)
    def __str__(self):
        return self.coursename

class Student(models.Model):

    def get_upload_to(instance, filename):
        upload_to = 'user_avatars'
        ext = filename.split('.')[-1]
        if instance.pk:
            filename = '{}.{}'.format(instance.pk, ext)
        else:
            filename = '{}.{}'.format(uuid.uuid4().hex, ext)
        return upload_to + '/' + filename
    username=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(1000000000000)], blank=True, null=True,unique=True)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    course=models.ForeignKey(Course,on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(upload_to=get_upload_to, default='user_avatars/default-avatar.jpg', blank=False, null=False)

    def __str__(self):
        return str(self.username)



class Subject(models.Model):
    subjectname=models.CharField(max_length=50,blank=True,null=True)
    course=models.ForeignKey(Course,on_delete=models.CASCADE)
    def __str__(self):
        return self.subjectname

class Student_attendance(models.Model):
    student=models.ForeignKey(Student, on_delete=models.CASCADE)
    attendance=models.IntegerField(validators=[MinValueValidator(0),MaxValueValidator(100)], blank=True, null=True)
    def __str__(self):
        return str(self.attendance)


class Follow(models.Model):
    follower = models.ForeignKey(Student, related_name="person_following")
    followed = models.ForeignKey(Student, related_name="person_followed")
    time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.follower) + "-" + str(self.followed)

	