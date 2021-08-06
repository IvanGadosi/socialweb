from django.urls import path
from . import views

urlpatterns = [
    path('posts/<str:order>/', views.PostView.as_view(), name='post-list'),
    path('post/<int:pk>/', views.post_detail_view, name='post-detail'),
    path('create/', views.post_create_view, name='post-create'),
    path('delete/<int:pk>/', views.post_delete_view, name='post-delete'),
    path('update/<int:pk>/', views.post_update_view, name='post-update'),

    path('vote/plus/post/<str:pk>/', views.vote_plus, name='vote-plus'),
    path('vote/minus/post/<str:pk>/', views.vote_minus, name='vote-minus'),
]
