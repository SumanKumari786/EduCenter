"""Project1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf.urls import url
from django.contrib.auth import views as auth_views
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from MyApp import views
from MyApp.views import PostListView
from Project1 import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("contact/", views.contact, name="contact"),
    path("about/", views.aboutus, name="about"),
    path("compiler/", views.compiler, name="compiler"),
    path("galary/", views.galary, name="galary"),
    path("", views.index, name="index"),

    # Blog search view
    path('search/', views.search, name='search'),


     #question views
    path('home/', views.home, name='home'),
    path('create/', views.create, name='create'),
    path('chooseans/<ques_id>/', views.chooseans, name='chooseans'),
    path('results/<ques_id>/', views.results, name='results'),

    # Change password
    path('changepass/', views.changePass, name='changepass'),

     # Update profile Views
    path('view_profile/', views.view_profile, name='view_profile'),
    path('update_profile/', views.update_profile, name='update_profile'),


    # password reset views
    path('password-reset/',
         auth_views.PasswordResetView.as_view(template_name='MyApp/password_reset_form.html'),
         name='password_reset'),
    path('password-reset/done/',
         auth_views.PasswordResetDoneView.as_view(template_name='MyApp/password_reset_done.html'),
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>',
         auth_views.PasswordResetConfirmView.as_view(template_name='MyApp/password_reset_confirm.html'),
         name='password_reset_confirm'),
    path('password-reset-complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name='MyApp/password_reset_complete.html'),
         name='password_reset_complete'),

    path('our-courses/', views.course, name="our-courses"),
    path('htmlcourse/', views.html, name="htmlcourse"),
    path('htmldetails/', views.htmldetails, name="htmldetails"),
    path('csscourse/', views.css, name="csscourse"),
    path('cssdetails/', views.cssdetails, name="cssdetails"),
    path('jscourse/', views.js, name="jscourse"),
    path('bootcourse/', views.boot, name="bootcourse"),
    path('pycourse/', views.python, name="pycourse"),
    path('djancourse/', views.django, name="djancourse"),

    path('MyApp/', include('MyApp.urls')),

    path('blog/', PostListView.as_view(), name='blog'),

    path('favourite_post_list/', views.post_favourite_list, name='favourite_post_list'),
    path('favourite/<id>', views.favourite_post, name='favourite_post'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

