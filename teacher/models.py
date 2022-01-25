from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Teacher(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    address=models.CharField(max_length=40)
    contact=models.CharField(max_length=20,null=False)
    profile_pic= models.ImageField(upload_to='teacher/')
    status= models.BooleanField(default=False)
    salary=models.PositiveIntegerField(null=True)

