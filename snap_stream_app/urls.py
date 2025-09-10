from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('user/', views.UserView.as_view(), name="users"),
    path('user/<int:id>', views.SingleUserView.as_view(), name="user"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('post/new/', views.PostView.as_view(), name="post-create"),
    path('search/', views.PostView.as_view(), name="search"),
    path('search/<int:id>/', views.SinglePostView.as_view(), name="search-details"),
    path('post/<int:id>/', views.SinglePostView.as_view(), name="post-delete"),
    path('profile/<int:id>/', views.ProfileView.as_view()),
    path('post/<int:userId>/<int:postId>/like/', views.LikePostView.as_view(), name="post-like"),
    path('search/find/', views.SearchPostsView.as_view(), name="search-text"),
    path('user/follow/<int:userId>/', views.FollowView.as_view(), name="profile-follow"),
    path('home/<int:id>/', views.HomeView.as_view(), name="home"),
    path('post/<int:userId>/comment/', views.CommentView.as_view(), name="comment-post"),
    path('post/<int:postId>/comment-list/', views.CommentView.as_view(), name="list-post"),
]
