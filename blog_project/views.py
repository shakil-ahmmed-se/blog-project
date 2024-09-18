from django.shortcuts import render, redirect
from post.models import Posts
from categories.models import Category

def  home(request,category_slug = None):
    data = Posts.objects.all()
    if category_slug is not None:
        category = Category.objects.get(slug = category_slug)
        data = Posts.objects.filter(category = category)
    categories = Category.objects.all()
    # print(data)
    return render(request, 'home.html',{'data':data,'category':categories})