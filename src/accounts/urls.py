from django.urls import path
from . import views

app_name = "accounts"

urlpatterns = [
    path("register/", views.register_account, name="register_account"),
    path('login/',views.login_account,name='login_account'),
    path('active/<uidb64>/<token>/',views.active_account,name='active_account'),
    path('logout/',views.logout_account,name='logout_account'),
    path('forget/',views.forget_password_account,name='forget_password_account'),
    path('reset/<uidb64>/<token>/',views.reset_password_account,name='reset_password_account'),
    path('send_link_forget_password_account',views.send_link_forget_password_account,name='send_link_forget_password_account'),
    path('final_reset/',views.final_reset_password,name='final_reset_password'),
    
    path('profile/',views.profile_account,name='profile_account'),
    
    ]
