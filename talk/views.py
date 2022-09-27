# chat/views.py
from django.shortcuts import render


def index(request):
    return render(request, 'talk/index.html', {})


def room(request, room_name):
    return render(request, 'talk/room.html', {
        'room_name': room_name
    })
