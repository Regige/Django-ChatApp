from django.shortcuts import render
from django.http.response import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.core import serializers

from chat.models import Message
from chat.models import Chat


# Create your views here.

@login_required(login_url='/login/')
def index(request):
    print(request.method)
    if request.method == 'POST':
        print("Request method is post")
        print(request.POST['textmessage'])
        
        testChat = Chat.objects.get(id=1)        
        new_message = Message.objects.create(text=request.POST['textmessage'], chat=testChat, author=request.user, receiver=request.user)
        serialized_obj = serializers.serialize('json', [new_message])
        return JsonResponse(serialized_obj[1:-1], safe=False)
    chatMessages = Message.objects.filter(chat__id=1)
    return render(request, 'chat/index.html', {'username': 'Regina', 'messages': chatMessages})



def login_view(request):
    redirect = request.GET.get('next', '/chat/')

    if request.method == 'POST':
        user = authenticate(username=request.POST.get('username'), password=request.POST.get('password'))
        if user:
            login(request, user)
            return HttpResponseRedirect(request.POST.get('redirect'))
        else:
            return render(request, 'auth/login.html', {'wrongPassword': True, 'redirect': redirect})
        
    return render(request, 'auth/login.html', {'redirect': redirect})



def register_new_user(request):
    if request.method == 'POST':
        user = User.objects.create_user(username=request.POST.get('username'), email=request.POST.get('email'), password=request.POST.get('password'))
        return HttpResponseRedirect('/login/')

    return render(request, 'register/register.html')