from django.urls import path
from . import views


urlpatterns = [
    path('registration/', views.create_user_view, name='user-registration'),
    path('login/', views.CustomLoginView.as_view(), name='user-login'),
    path('logout/', views.logout_view, name='user-logout'),
    path('users/<str:pk>/', views.user_detail_view, name='user-detail'),
    path('users/edit/<str:pk>/', views.edit_user_view, name='user-edit'),
    path('users/delete/<str:pk>/', views.user_delete_view, name='user-delete'),
]
