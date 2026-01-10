from django.urls import path
from .views import (
    UserLoginView,
    UserLogoutView,
    DashboardView,
    UserCreateView,
    BlockUserView,
    DeleteUserView,
)

urlpatterns = [
    path("", UserLoginView.as_view(), name="login"), 
    path("logout/", UserLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("users/create/", UserCreateView.as_view(), name="user-create"),
     path("users/<int:pk>/block/", BlockUserView.as_view(), name="user-block"),
    path("users/<int:pk>/delete/", DeleteUserView.as_view(), name="user-delete"),
]
