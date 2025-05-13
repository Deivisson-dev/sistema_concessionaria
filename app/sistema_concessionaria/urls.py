from django.contrib import admin
from django.urls import path
from users import views
from users.views import home_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home/', home_view, name='home'),
    path('registro/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]
