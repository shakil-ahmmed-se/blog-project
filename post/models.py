from django.db import models
from categories.models import Category
from django.contrib.auth.models import User
# Create your models here.
class Posts(models.Model):
    title = models.CharField(max_length= 50)
    content = models.TextField()
    category = models.ManyToManyField(Category) #ekta categorir onk gulla post thakte parbe abar ekta post er onk gulla category thakte pare
    author = models.ForeignKey(User,on_delete= models.CASCADE)
    image = models.FileField(upload_to='post/media/uploads/', blank=True, null= True)
    def __str__(self):
        return f'{self.title}'

class Comment(models.Model):
    posts = models.ForeignKey(Posts, on_delete= models.CASCADE,related_name='comments')
    name = models.CharField(max_length = 30)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f'Comment by {self.name}'