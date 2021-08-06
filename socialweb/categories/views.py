from django.shortcuts import render, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib.auth.decorators import login_required

from .models import Category
from posts.models import Post
from .forms import CategoryForm


@login_required
def category_list_view(request):
    category_list=Category.objects.all().order_by('category_name')
    form = CategoryForm()
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("post-list", "-date_created")
    context = {
        "form": form,
        "category_list": category_list
    }
    return render(request, "category_list.html", context)


def category_detail_view(request, pk):
    category=pk
    post_list = Post.objects.filter(category=pk)
    paginator = Paginator(post_list, 6)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)
    context = {
        "category": category,
        "posts": posts,
        "page": page
    }
    return render(request, "category_detail.html", context)
