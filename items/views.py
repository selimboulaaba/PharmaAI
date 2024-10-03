from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from home.models import UserProfile

# Create your views here.

@login_required
def index(request):
    items = []

    return render(request, 'items/index.html', {
        'user_name': request.user.first_name + " " + request.user.last_name,
        'items': items
        })