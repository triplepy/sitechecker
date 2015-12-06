from django.shortcuts import render
from .models import User, Site
from .forms import CheckerForm


def home(request):
    if request.method == 'POST':
        form = CheckerForm(request.POST)
        if form.is_valid():
            user = User.objects.create(nickname=form['nickname'])
            Site.objects.create(user=user, url=form['siteurl'])
        return render(request, 'checker/home.html', '')
    else:
        form = CheckerForm()
        return render(request, 'checker/home.html', {'form': form})


