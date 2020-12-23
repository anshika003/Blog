from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class post(models.Model):
    sno =models.AutoField(primary_key=True)

    title=models.CharField(max_length=50)
    content=models.TextField()
    author=models.TextField(max_length=100)
    slug=models.CharField(max_length=100)
    views = models.IntegerField(default=0)
    timeStamp = models.DateTimeField( blank=True)
    

    def __str__(self):   
        return  self.title +' by '+ self.author
    

class BlogComment(models.Model):

    sno = models.AutoField(primary_key=True)
    comment = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    Post = models.ForeignKey(post, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    timestamp = models.DateTimeField(default=now)

    def __str__(self):
        return self.comment[0:8] + "...." + "by " + self.user.username
    