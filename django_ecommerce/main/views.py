from django.shortcuts import render
from payments.models import User

def index(request):
    uid = request.session.get('user')
    if uid is None:
        return render(request, 'main/index.html')
    else:
        return render(
            request,
            'main/user.html',
            {'user':User.objects.get(pk=uid)}
        )
