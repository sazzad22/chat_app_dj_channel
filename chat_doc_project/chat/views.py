from django.shortcuts import render


def index(request):
    return render(request, "chat/index.html")

def index2(request, group_name):
    return render(request, "chat/index2.html",{'group_name':group_name})


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
