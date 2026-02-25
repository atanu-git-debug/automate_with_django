from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class CompressImage(models.Model):
    # [(10, '10%'), (20, '20%'), (30, '30%'), (40, '40%'), (50, '50%'), (60, '60%'), (70, '70%'), (80, '80%'), (90, '90%') , (100, '100%')]
    QUALITY_CHOICES = [(i, f'{i}%') for i in range(10, 110, 10)]
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    original_image = models.ImageField(upload_to='original_images/')
    quality = models.IntegerField(choices=QUALITY_CHOICES,default=80)
    compressed_image = models.ImageField(upload_to='compressed_images/')
    compressed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username