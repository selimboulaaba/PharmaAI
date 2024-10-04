from django.contrib.auth.models import User

def user_info(request):
    if request.user.is_authenticated:
        return {'currentUser': request.user.username}
    return {}