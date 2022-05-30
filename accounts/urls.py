from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

#Views almacena funciones que regresan ciertas vistas
#urls se encarga de regresar cierta view dado cierto argumento en la URL
urlpatterns = [
    path('', views.home, name = "home"),
    path('register/', views.register, name = "register"),
    path('login/', views.loginPage, name = "login"),
    path('logout/', views.logoutUser, name = "logout"),
    
    path('products/', views.products, name = "products"),
    path('customer/<str:pk>/', views.customer, name = "customer"),
    
    path('about-us/', views.aboutme, name = "about"),
    path('primarygoal/', views.primarygoal, name = "primary"),
    path('contact-us/', views.contactme, name = "contact"),
    
    path('create_order/<str:pk>/', views.createOrder, name= "create_order"),
    path('update_order/<str:pk>/', views.updateOrder, name= "update_order"),
    path('delete_order/<str:pk>/', views.deleteOrder, name= "delete_order"),
    
    path('error/', views.error401, name = "error"),
    
    path('user-page/', views.userPage, name = "user-page"),
    path('account_setting/', views.userSettings, name = 'account'),
    
    
    #From django documentation default views
     path('reset_password/',
     auth_views.PasswordResetView.as_view(template_name="accounts/password_reset.html"),
     name="reset_password"),

    path('reset_password_sent/', 
        auth_views.PasswordResetDoneView.as_view(template_name="accounts/password_reset_sent.html"), 
        name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(template_name="accounts/password_reset_form.html"), 
     name="password_reset_confirm"),

    path('reset_password_complete/', 
        auth_views.PasswordResetCompleteView.as_view(template_name="accounts/password_reset_done.html"), 
        name="password_reset_complete"),
]
