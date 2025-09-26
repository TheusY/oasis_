from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),       # login
    path("register/", views.register, name="register"),
    path("logout/", views.logout_view, name="logout"),
    path("home/", views.home, name="home"),    # página após login
]

