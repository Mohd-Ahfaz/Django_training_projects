from django.shortcuts import render

# Create your views here.
def Home(Request):
    return render(Request, 'Home.html')