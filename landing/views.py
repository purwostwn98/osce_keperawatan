from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'landing/index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
    else: 
        return render(request, 'landing/login.html')
