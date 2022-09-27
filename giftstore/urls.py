"""giftstore URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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
from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static
# from writer.views import *

urlpatterns = [
    # path('talk/', include('talk.urls')),
    path('admin/', admin.site.urls),
    path('', views.index, name='home'),
    path('signup/', views.signup, name='signup'),
    path('resend/', views.otpresend, name='resend'),
    path('upstore/', views.SignupInit),
    path('signin/', views.signin),
    path('forgot/', views.forgot),
    path('verify/', views.verify),
    path('login/', views.inlog),
    path('logout/', views.logout),
    path('profile/', include('user.urls')),
    path('signEmail', views.signEmail, name="Email"),
    path('getOTPmail', views.recieveEotp, name='recieveOTPE'),
    path('address', views.address, name='address'),
    path('displayaddress/<str:addname>/', views.displayaddress, name='displayaddress'),
    path('contact/', views.contact, name='contactUs'),
    path('contact/response/', views.contactresponse, name='contactUsresponse'),
    path('makenew/', views.makenew),
    path('makenewsubmit/', views.makenewsubmit),
    path('pages/', include('pages.urls')),
    path('post/<str:name>/', views.getPopst),
    path("search/", views.search),
    path("resume/", include('resume.urls'))
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
