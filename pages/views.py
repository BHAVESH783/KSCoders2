from django.shortcuts import render
from .models import Pages


# Create your views here.
def page(r, page):
    p = Pages.objects.filter(name=page)
    if p:
        text = p[0].read()
    else:
        text = "<h1>PAGE NOT FOUND</h1>"
    return render(r, "page/page.html", {'content': text})