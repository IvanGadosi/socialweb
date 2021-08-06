from django.urls import path
from . import views


urlpatterns = [
    path('category-list/', views.category_list_view, name='category-list'),
    path('category/<str:pk>/', views.category_detail_view, name='category-detail'),
]
