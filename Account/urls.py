from django.contrib import admin
from django.urls import include, path

from Account import views

urlpatterns = [
    path("register/", views.registerUser, name="Profile-Register"),
    ### Users - Admin Rights ###
    path("", views.getUsersAdmin, name="Admin-Users"),
    path("<int:pk>/", views.getUserDetailAdmin, name="Admin-User-Detail"),
    path("update/<int:pk>/", views.updateUser, name="Admin-User-update"),
    path("delete/<int:pk>/", views.deleteUser, name="Admin-User-delete"),
    ### User - Profile Rights ###
    path("login/", views.MyTokenObtainPairView.as_view(), name="Login"),
    path("profile/", views.GetUserProfile.as_view(), name="Profile-Details"),
    path("profile/update/", views.updateUserProfile, name="Profile-Update"),
    path("userByName", views.UserViewSetByName.as_view(), name="userByName"),
]
