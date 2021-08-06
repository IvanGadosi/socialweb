from django.shortcuts import render
from django.db.models import Count, Avg

from posts.models import Post, Comment
from categories.models import Category
from accounts.models import CustomUser

def statistics_view(request):
    best_users=CustomUser.objects.all().annotate(num_posts=Count('post')).order_by('-num_posts')[:5]
    most_comment_posts=Post.objects.all().annotate(num_comments=Count('comment')).order_by('-num_comments')[:8]
    avrg_post_rating=Post.objects.all().aggregate(Avg('rating'))
    posts_count=Post.objects.all().count()

    category_activity=Category.objects.all().annotate(num_posts=Count('post')).order_by('-num_posts')[:5]
    labels_category = []
    data_category = []
    for ctgry in category_activity:
        labels_category.append(ctgry.category_name)
        data_category.append(ctgry.num_posts)
    context = {
        "best_users": best_users,
        "most_comment_posts": most_comment_posts,
        "avrg_post_rating": avrg_post_rating,
        "posts_count": posts_count,
        "category_activity": category_activity,
        "labels_category": labels_category,
        "data_category": data_category,
    }
    return render(request, "statistics.html", context)