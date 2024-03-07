from django.contrib import admin
from django.urls import path, include
from blog.views import  BlogCreateView, BlogDetailView, BlogListView, ProfileDetailView, AboutView, PagesView, SignUpView, LoginView, ProfileView, IndexView

from django_comments import urls as comments_urls

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('admin/', admin.site.urls),
    path('comments/', include(comments_urls)),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/profile/', ProfileView.as_view(), name='profile'),
    path('blogs/', BlogListView.as_view(), name='blog_list'),
    path('blogs/<int:pk>/', BlogDetailView.as_view(), name='blog_detail'), 
    path('blogs/create/', BlogCreateView.as_view(), name='create_blog'),
    path('about/', AboutView.as_view(), name='about'),
    path('accounts/profile/<int:pk>/', ProfileDetailView.as_view(), name='profile_detail'),

]
