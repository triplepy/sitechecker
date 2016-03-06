from django.shortcuts import render

from .models import User, Site
from .forms import CheckerForm


def home(request):
    if request.method == 'POST':
        form = CheckerForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            url = form.cleaned_data['siteurl']
            user, user_is_created \
                = User.objects.get_or_create(nickname=nickname)

            define_url = Site.url_type(url)
            site, site_is_created \
                = Site.objects.get_or_create(user=user, url=define_url)
            site.send_register_mail(request.get_host())
        return render(request, 'checker/home.html', {'site': site})
    else:
        form = CheckerForm()
        return render(request, 'checker/home.html', {'form': form})


def verify(request, nickname, url, uuid):
    user = User.objects.get(nickname=nickname)
    site = Site.objects.get(url=url, user=user)
    if site.verify(uuid):
        return render(request, 'checker/message.html', {"message": "Verify success"})

    else:
        return render(request, 'checker/message.html', {"message": "Verify failure"})


def delete(request):
    if request.method == 'POST':
        form = CheckerForm(request.POST)
        if form.is_valid():
            nickname = form.cleaned_data['nickname']
            url = form.cleaned_data['siteurl']
            try:
                user = User.objects.get(nickname=nickname)
            except User.DoesNotExist:
                return render(request, 'checker/message.html', {"message": "Delete failure, User does not exist"})

            try:
                define_url = Site.url_type(url)
                site = Site.objects.get(url=define_url, user=user)
                site.delete()
            except Site.DoesNotExist:
                return render(request, 'checker/message.html', {"message": "Delete failure, Site does not exist"})
            return render(request, 'checker/message.html', {'message': "Delete success"})
