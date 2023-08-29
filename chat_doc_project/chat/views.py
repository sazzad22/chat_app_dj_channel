from django.shortcuts import render
from .models import Group, Chat

def index(request):
    return render(request, "chat/index.html")

def index2(request, group_name):
    print('frm chat.view Group Name : ',group_name)
    group = Group.objects.filter(name = group_name).first()
    chats = []
    if group:
        chats = Chat.objects.filter(group = group)
    else:
        group = Group(name = group_name)
        group.save()
    return render(request, "chat/index2.html",{'group_name':group_name,'chats':chats})


def room(request, room_name):
    return render(request, "chat/room.html", {"room_name": room_name})
