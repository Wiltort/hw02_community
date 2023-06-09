"""social_network_study_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import include, path
from django.contrib.flatpages import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #flatpages
    path('about/', include('django.contrib.flatpages.urls')),
    #импорт правил из приложения постс
    path("", include("posts.urls")),
    #импорт правил из приложения админ
    path("auth/", include("Users.urls")),
    path("auth/", include("django.contrib.auth.urls")),
]
urlpatterns +=[
    path('about-us/',views.flatpage, {'url': '/about-us/'}, name ='about'),
    path('terms/', views.flatpage, {'url': '/terms/'}, name = 'terms'),
    path('about-author/', views.flatpage, {'url': '/about-author/'}, name = 'about-author'),
    path('about-spec/', views.flatpage, {'url': '/about-spec/'}, name = 'spec'),
]