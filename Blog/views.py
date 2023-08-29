from django.shortcuts import render

def home(request):
    return render(request, "home.html")

def solution(request):
    return render(request, "solution.html")

def code(request):
    return render(request, 'code.html')

def demo(request):
    return render(request, "demo.html")

def portfolio(request):
    return render(request, "portfolio.html")

def contribution(request):
    return render(request, "contribution.html")

def login(request):
    return render(request, "partial/login.html")


def landing(request):
    return render(request, "landing.html")