from django.shortcuts import render, reverse, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.views.generic import ListView

from .models import Post, Voter, Comment
from accounts.models import CustomUser
from .forms import PostForm, CommentForm


class PostView(ListView):
    model=Post
    paginate_by = 10
    template_name = 'posts.html'

    def get_context_data(self, **kwargs):
        context = super(PostView, self).get_context_data(**kwargs) 
        post_list = Post.objects.all().order_by(self.kwargs['order'])
        paginator = Paginator(post_list, self.paginate_by)

        page = self.request.GET.get('page')

        try:
            posts = paginator.page(page)
        except PageNotAnInteger:
            posts = paginator.page(1)
        except EmptyPage:
            posts = paginator.page(paginator.num_pages)
            
        context['posts'] = posts
        return context


def post_detail_view(request, pk):
    post = Post.objects.get(post_id=pk)
    comments = Comment.objects.filter(comment_post_id=pk)
    form = CommentForm(initial={"comment_user": request.user, "comment_post": pk})
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post-list", "-date_created")
    context = {
        "post": post,
        "form": form,
        "comments": comments,
    }
    return render(request, "detail_post.html", context)


@login_required
def post_create_view(request):
    form = PostForm(initial={"creator": request.user})
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("post-list", "-date_created")
    context = {
        "form": form
    }
    return render(request, "create_post.html", context)


@login_required
def post_update_view(request, pk):
    post = Post.objects.get(post_id=pk)
    if request.user == post.creator:
        form = PostForm(instance=post)
        if request.method == "POST":
            if request.FILES and post_image:
                os.remove(post.post_image.path)
            form = PostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect("post-list", "-date_created")
        context = {
            "form": form,
            "post": post
        }
        return render(request, "update_post.html", context)
    else:
        return redirect("post-list", "-date_created")


@login_required
def post_delete_view(request, pk):
    post = Post.objects.get(post_id=pk)
    if request.user == post.creator:
        post.delete()
    return redirect("post-list", "-date_created")


@login_required
def vote_plus(request, pk):
    post = Post.objects.get(post_id=pk)
    if not Voter.objects.filter(voter_post_id=pk, voter_user=request.user).exists():
        post.rating+=1
        post.save()
        v = Voter(voter_user=request.user, voter_post_id=pk)
        v.save()
    return redirect("post-list", "-date_created")


@login_required
def vote_minus(request, pk):
    post = Post.objects.get(post_id=pk)
    if not Voter.objects.filter(voter_post_id=pk, voter_user=request.user).exists():
        post.rating-=1
        post.save()
        v = Voter(voter_user=request.user, voter_post_id=pk)
        v.save()
    return redirect("post-list", "-date_created")


def view_404(request, exception=None):
    return redirect("post-list", "-date_created")