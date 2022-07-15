
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_user, name='login_user'),
    path('logout', views.logout_user, name='logout_user'),
    path('profile', views.profile, name='profile'),
    path('signup', views.sign_up, name='signup'),
    path('new-task', views.new_task, name='new-task'),

]
