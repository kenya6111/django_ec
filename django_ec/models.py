from django.db import models

# Create your models here.
class items(models.Model):
    name = models.CharField(max_length=100)
    star = models.IntegerField(null=True, blank=True, default=1)
    price = models.IntegerField(null=True, blank=True, default=1)
    image = models.ImageField(upload_to='')
    is_sale = models.BooleanField(default=False)
    update = models.DateField(),
    # content = models.TextField()
    # author = models.CharField(max_length=100)
    # readText = models.TextField(null=True, blank=True, default='a')
    def __str__(self):
         return self.name