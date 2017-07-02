from django.shortcuts import render
from django.template import RequestContext
from payments.models import User
from main.models import MarketingItem, StatusReport


def index(request):
    uid = request.session.get('user')
    if not uid:
        market_items = MarketingItem.objects.all()
        return render(
            request, 'main/index.html',
            {'marketing_items': market_items}
            )
    else:
        status = StatusReport.objects.all().order_by('-when')[:20]
        return render(
            request, 'main/user.html',
            context = {'user': User.objects.get(pk=uid), 'reports': status},
        )

def report(request):
    if request.method == "POST":
        status = request.POST.get("status", "")
        #update the database with the status
        if status:
            uid = request.session.get('user')
            user = User.objects.get(pk=uid)
            StatusReport(user=user, status=status).save()
        #always return something
        return index(request)