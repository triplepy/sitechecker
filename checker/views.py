import checker
from django.shortcuts import render

from .models import User, Site
from .forms import CheckerForm


def home(request):
    if request.method == 'POST':
        form = CheckerForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            url = form.cleaned_data['siteurl']
            try:
                user = User.objects.get(nickname=nickname)
            except User.DoesNotExist:
                user = User.objects.create(nickname=nickname)

            try:
                Site.objects.get(user=user, url=url)
            except Site.DoesNotExist:
                site = Site.objects.create(user=user, url=url)
                site.send_register_mail()
        return render(request, 'checker/home.html', '')

    else:
        form = CheckerForm()
        return render(request, 'checker/home.html', {'form': form})

def verify(request, nickname, url, uuid):
    user = User.objects.get(nickname=nickname)
    site = Site.obects.get(url=url,user=user)
    if site.verify(uuid):
        return render(request, 'checker/verify.html', {message : "success" })

    else:
        return render(request, 'checker/verify.html', {message: "failure"
 
    
