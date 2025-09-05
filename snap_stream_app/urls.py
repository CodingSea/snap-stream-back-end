from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView
from .views import CustomTokenObtainPairView

urlpatterns = [
    path('users/', views.UserView.as_view(), name="users"),
    path('signup/', views.SignupView.as_view(), name="signup"),
    path('post/new/', views.PostView.as_view(), name="post-create"),
    path('search/', views.PostView.as_view(), name="search"),
    path('search/<int:pk>', views.SinglePostView.as_view(), name="search-details"),
]
