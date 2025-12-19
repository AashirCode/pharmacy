from django.db import models

# Create your models here.

class Medicines(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10 , decimal_places=2)
    image = models.ImageField(upload_to='media/',null=True)
    
    def __str__(self):
        return self.name