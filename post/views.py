from django.shortcuts import render,redirect
from .import forms
from .import models
from django.contrib.auth.decorators import login_required
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic import DeleteView,DetailView
from django.utils.decorators import method_decorator
# Create your views here.
@login_required
def add_post(request):
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            return redirect('homepage')
    else:   
        post_form = forms.PostForm()
    return render(request,'add_post.html', {'form':post_form})
# Add post using class base view

@method_decorator(login_required, name='dispatch')
class AddPostCreateView(CreateView):
    model = models.Posts
    form_class = forms.PostForm
    template_name = 'add_post.html'
    success_url = reverse_lazy('add_post')
    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

@method_decorator(login_required, name='dispatch')
class EditPostView(UpdateView):
    model = models.Posts
    form_class = forms.PostForm
    template_name = 'add_post.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('profile')

@method_decorator(login_required, name='dispatch')
class DeletePostVeiw(DeleteView):
    model = models.Posts
    template_name = 'delete.html'
    success_url = reverse_lazy('profile')
    pk_url_kwarg = 'id'


class DetailPostViews(DetailView):
    model = models.Posts
    pk_url_kwarg = 'id'
    template_name = 'post_details.html'

    def post(self,request, *args, **kwargs):
        comment_form = forms.CommentForm(data = self.request.POST)
        posts = self.get_object()
        if comment_form.is_valid():
            new_comment = comment_form.save(commit = False)
            new_comment.posts = posts
            new_comment.save()
        return self.get(request, *args, **kwargs)

    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        posts = self.object
        comments = posts.comments.all()
        comment_form = forms.CommentForm()
        context['comments'] = comments
        context['comment_form'] = comment_form
        return context







@login_required
def edit_post(request,id):
    post = models.Posts.objects.get(pk =id)
    post_form = forms.PostForm(instance=post)
    print(post.title)
    if request.method == 'POST':
        post_form = forms.PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.instance.author = request.user
            post_form.save()
            return redirect('homepage')
    return render(request,'add_post.html', {'form':post_form})

@login_required
def delete_post(request,id):
    post = models.Posts.objects.get(pk =id)
    post.delete()
    return redirect('homepage')
   