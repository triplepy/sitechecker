from django.shortcuts import render
from django.db.utils import IntegrityError

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
        
            Site.objects.create(
                    user=user, url=url)

                
        return render(request, 'checker/home.html', '')
    
    else:
        form = CheckerForm()
        return render(request, 'checker/home.html', {'form': form})


