from django.urls import path
from consumers import views


urlpatterns = [
    path('account/', views.create_user, name='account'),
    path('account/verify_otp/', views.verify_otp, name='verify_otp'),
    path('account/verify_otp/signup/', views.signup_form, name='signup_form'),
    path('account/verify_otp/signup/login', views.login, name='login'),
    path('logout/', views.logout, name="logout")
]
