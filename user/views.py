from django.shortcuts import render
from .models import ContactUs


# Create your views here.
def profile(r):
    return render(r, 'user/profile.html')
