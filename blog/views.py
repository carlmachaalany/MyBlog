from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import (TemplateView, ListView, DetailView, CreateView, UpdateView, DetailView, DeleteView)
from blog.models import Post, Comment
from blog.forms import PostForm, CommentForm
from django.urls import reverse_lazy
# With CBV we can import both these classes to mix in loginrequired with our CBV classes here
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

class AboutView(TemplateView):
    template_name = 'about.html'

class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    # I'm doing a query on my model (this is an overriden method from ListView)
    # This is to say how you should list the post objects
    def get_queryset(self):
        # get Post objects and filter them to the conditions:
        # published date must be less than or equal to (__lte) now and order them where the most recent post
        # is at the top and not the oldest (the '-' in '-published_date' does that)
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    model = Post

# This and all other classes that inherit LoginRequiredLogin require you to login before working with the CBV
class PostCreateView(LoginRequiredMixin, CreateView):
    # login_url is the path we are going to go if the user is not logged in
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin, UpdateView):
    # login_url is the path we are going to go if the user is not logged in
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin, DeleteView):
    model = Post
    success_url = reverse_lazy('post_list')

class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    context_object_name = 'posts'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('create_date')

####################################
####################################

@login_required
def post_publish(request,pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('post_detail', pk=pk)


@login_required
def add_comment_to_post(request, pk):

    post = get_object_or_404(Post, pk=pk)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('post_detail', pk = post.pk)
    else:
        form = CommentForm()

    return render(request, 'blog/comment_form.html', {'form':form})

@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post_detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # save the post in a variable so that you remember its pk
    # because after deleting the comment you want to still have access
    # to the pk of the post to say pk = post_pk
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail', pk=post_pk)
