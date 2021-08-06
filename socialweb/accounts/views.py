from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
import os
from django.contrib.auth.views import LoginView
from django.contrib.auth import logout
from django.db.models import Avg
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from .models import CustomUser
from posts.models import Post
from .forms import CustomUserCreateForm, UpdateUserProfileForm


def create_user_view(request):
    form=CustomUserCreateForm()
    if request.method=="POST":
        form = CustomUserCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("post-list", "-date_created")
    context = {
        "form": form
    }
    return render(request, "register.html", context)


class CustomLoginView(LoginView):
    template_name = 'login.html'


@login_required
def logout_view(request):
    logout(request)
    return redirect("post-list", "-date_created")


@login_required
def edit_user_view(request, pk):
    user = CustomUser.objects.get(username=pk)
    if user == request.user:
        form = UpdateUserProfileForm(instance=user)
        if request.method == "POST":
            if request.FILES and user.user_image:
                os.remove(user.user_image.path)
            form = UpdateUserProfileForm(request.POST, request.FILES, instance=user)
            if form.is_valid():
                form.save()
                return redirect("user-detail", "user.pk")
        context = {
            "form": form,
            "user": user
        }
        return render(request, "update_user.html", context)
    else:
        return redirect("post-list", "-date_created")


def user_detail_view(request, pk):
    post_list = Post.objects.filter(creator=pk)
    avg_user_post_rating=Post.objects.filter(creator=pk).aggregate(Avg('rating'))
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    user=CustomUser.objects.get(username=pk)
    context = {
        "posts": posts,
        "user": user,
        "page": page,
        "avg_user_post_rating": avg_user_post_rating
    }
    return render(request, "user_detail.html", context)


@login_required
def user_delete_view(request, pk):
    user = CustomUser.objects.get(username=pk)
    if user == request.user:
        user.delete()
    return redirect("post-list", "-date_created")
