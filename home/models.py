from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    is_manager = models.BooleanField(default=False)
    name = models.CharField(default='name',null=True,max_length=255)
    phone = models.CharField(null=True,blank=True,max_length=20)
    
    # Add any other fields as necessary
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['name', 'email', 'phone']
    
    def __str__(self):
        return self.username
    





class Package(models.Model):
   

    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    source = models.CharField(max_length=100)
    start_date = models.DateField()
    duration = models.PositiveIntegerField()
    manager = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name


class Accommodation(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)

    def __str__(self):
        return self.name




class Booking(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    accommodation = models.ForeignKey(Accommodation, on_delete=models.CASCADE)
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.user.username} - {self.package.name}"
