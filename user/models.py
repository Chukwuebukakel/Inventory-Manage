from django.db import models
from django.contrib.auth.models import User
#from django.db.models.signals import post_save
from dashboard.models import Branch




# Create your models here.


class Profile(models.Model):
    staff = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    phone = models.CharField(max_length=20, null=True)
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.ImageField(default='avatar.jpg', upload_to='Profile_Images')
    

    def __str__(self):
        return f"{self.staff.username} - {self.branch.name if self.branch else 'No Branch'}"
    



