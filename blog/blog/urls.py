from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, \
    BlogUpdateView, BlogDeleteView, signup, login, logout, password_reset_request, \
    add_comment_to_post, comment_approve, comment_remove

# app_name = 'blog'

urlpatterns = [
    path('home', BlogListView.as_view(), name='home'),
    
    path('post/<int:pk>/', BlogDetailView.as_view(), name='post_detail'),
    path('post/new/', BlogCreateView.as_view(), name='post_new'),
    path('post/<int:pk>/edit', BlogUpdateView.as_view(), name='post_edit'),
    path('post/<int:pk>/delete/', BlogDeleteView.as_view(), name='post_delete'),

    path("signup", signup, name="signup"),
    path("login", login, name="login"),
    path("logout", logout, name="logout"),

    path("password_reset", password_reset_request, name="password_reset"),

    path('post/<int:pk>/comment/', add_comment_to_post, name='add_comment_to_post'),
    path('comment/<int:pk>/approve/', comment_approve, name='comment_approve'),
    path('comment/<int:pk>/remove/', comment_remove, name='comment_remove'),
]
