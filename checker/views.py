from django.shortcuts import render

def home(request):
    if request.method == 'POST':
       user =  User.create(nickname=request['nickname'])
       Site.create(user=user, url=request['siteurl'])
       
    return render(request,'checker/home.html', '')


